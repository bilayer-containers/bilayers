"""
MorphEm feature extraction, wrapped as a Bilayers CLI entrypoint.

Model contract (from the CaicedoLab/MorphEm card):
  - Input is SINGLE-CHANNEL, ALREADY-SEGMENTED cell imagery. MorphEm does not
    find cells. It does not segment. It only makes feature vectors.
  - Multi-channel data is handled by "Bag of Channels": run each channel on its
    own, then concatenate the per-channel embeddings.
  - Each channel embedding is the ViT-Small CLS token (384 numbers).

Input contract this wrapper enforces (kept deliberately simple):
  - One file = one channel, grayscale, one segmented object.
  - Group channels of the same object by filename: <id>_<index>.<ext>
      cell1_0.png, cell1_1.png, cell1_2.png  ->  object "cell1", 3 channels
    Channels are ordered by <index>. A file with no numeric suffix is treated
    as a standalone 1-channel object.
  - Stacked arrays are also accepted as a self-contained object:
      .npy or multi-page .tif shaped (C,H,W) or (H,W,C)  ->  one object, C channels.
  - Concatenated / tiled images (e.g. raw HPA strips) are NOT auto-split.
    Split them first with the official CHAMMI-75 splitter. A warning is printed
    if a single-channel file looks tiled.

Every object in a run must have the SAME channel count, so the output table is
rectangular. Mixed counts raise a clear error.
"""

import argparse
import glob
import os
import re

import numpy as np
import torch
import torch.nn as nn
from torchvision import transforms as v2
from transformers import AutoModel

import tifffile
from PIL import Image


CLS_DIM = 384                      # ViT-Small CLS token width
IMG_EXTS = (".png", ".jpg", ".jpeg", ".tif", ".tiff", ".npy")
SUFFIX_RE = re.compile(r"^(.*)_(\d+)$")   # matches <id>_<index>


# --- Preprocessing transforms (verbatim from the MorphEm model card) ---

class SaturationNoiseInjector(nn.Module):
    """Replace fully saturated pixels (value 255) with random high noise."""
    def __init__(self, low=200, high=255):
        super().__init__()
        self.low = low
        self.high = high

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        channel = x[0].clone()
        noise = torch.empty_like(channel).uniform_(self.low, self.high)
        mask = (channel == 255).float()
        noise_masked = noise * mask
        channel[channel == 255] = 0
        channel = channel + noise_masked
        x[0] = channel
        return x


class PerImageNormalize(nn.Module):
    """Normalize each image on its own (instance norm), no dataset stats needed."""
    def __init__(self, eps=1e-7):
        super().__init__()
        self.instance_norm = nn.InstanceNorm2d(
            num_features=1, affine=False, track_running_stats=False, eps=eps
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if x.dim() == 3:
            x = x.unsqueeze(0)
        x = self.instance_norm(x)
        if x.shape[0] == 1:
            x = x.squeeze(0)
        return x


# --- Image loading ---

def _to_chw(arr: np.ndarray, path: str) -> np.ndarray:
    """Return a float32 array shaped (C, H, W) from a 2D or 3D array."""
    arr = arr.astype(np.float32)
    if arr.ndim == 2:
        return arr[None, ...]
    if arr.ndim == 3:
        # Decide which axis holds channels. Channels are few (<= 8), pixels many.
        first, last = arr.shape[0], arr.shape[2]
        if last <= 8 and first > 8:          # H, W, C  ->  C, H, W
            return np.transpose(arr, (2, 0, 1))
        if first <= 8 and last > 8:          # already C, H, W
            return arr
        # Ambiguous: assume the smaller axis is channels.
        if last <= first:
            return np.transpose(arr, (2, 0, 1))
        return arr
    raise ValueError(f"Unsupported array shape {arr.shape} in {path}")


def _maybe_warn_tiled(chw: np.ndarray, path: str) -> None:
    """Warn if a single-channel image looks like a horizontally tiled strip."""
    if chw.shape[0] != 1:
        return
    h, w = chw.shape[1], chw.shape[2]
    if h and w % h == 0 and (w // h) in (2, 3, 4, 5):
        print(f"WARNING: {os.path.basename(path)} is {w}x{h}, width is {w // h}x "
              f"the height. It may be a concatenated multi-channel strip. "
              f"If so, split it into channels first.")


def load_image(path: str) -> np.ndarray:
    """Load any supported file and return it as float32 (C, H, W)."""
    lower = path.lower()
    if lower.endswith(".npy"):
        arr = np.load(path)
        return _to_chw(arr, path)
    if lower.endswith((".tif", ".tiff")):
        return _to_chw(tifffile.imread(path), path)

    # PNG / JPG via PIL.
    arr = np.array(Image.open(path)).astype(np.float32)
    if arr.ndim == 3:
        # Drop an alpha channel if present.
        if arr.shape[2] == 4:
            arr = arr[:, :, :3]
        # Grayscale saved as RGB: identical planes collapse to one channel.
        if arr.shape[2] > 1 and np.all(arr[:, :, 0:1] == arr):
            arr = arr[:, :, 0]
    return _to_chw(arr, path)


# --- Grouping files into objects ---

def build_objects(paths):
    """Return an ordered dict: object_id -> list of single-channel (H, W) planes."""
    groups = {}   # gid -> {channel_index: plane}
    for path in paths:
        chw = load_image(path)
        _maybe_warn_tiled(chw, path)
        stem = os.path.splitext(os.path.basename(path))[0]
        c = chw.shape[0]

        if c == 1:
            m = SUFFIX_RE.match(stem)
            if m:
                gid, idx = m.group(1), int(m.group(2))
            else:
                gid, idx = stem, 0
            groups.setdefault(gid, {})[idx] = chw[0]
        else:
            # Self-contained multi-channel file: its own object, array order.
            d = groups.setdefault(stem, {})
            for k in range(c):
                d[k] = chw[k]

    ordered = {}
    for gid in sorted(groups):
        idxs = sorted(groups[gid])
        if idxs != list(range(len(idxs))):
            print(f"WARNING: object '{gid}' has non-contiguous channel indices "
                  f"{idxs}; using this order anyway.")
        ordered[gid] = [groups[gid][i] for i in idxs]
    return ordered


# --- Main ---

def main():
    parser = argparse.ArgumentParser(description="MorphEm feature extraction")
    parser.add_argument("-i", "--input_folder", required=True,
                        help="Folder of pre-segmented single-channel images")
    parser.add_argument("-o", "--output_folder", required=True,
                        help="Where to write the feature CSV and NPY")
    parser.add_argument("-b", "--batch_size", type=int, default=32,
                        help="Single channels processed per forward pass")
    args = parser.parse_args()

    os.makedirs(args.output_folder, exist_ok=True)

    # TODO: Add GPU support once CUDA containers exist.
    device = "cpu"

    paths = sorted(
        p for p in glob.glob(os.path.join(args.input_folder, "**", "*"), recursive=True)
        if p.lower().endswith(IMG_EXTS)
    )
    if not paths:
        raise SystemExit(f"No supported images found in {args.input_folder}")

    objects = build_objects(paths)
    gids = list(objects.keys())

    counts = {len(v) for v in objects.values()}
    if len(counts) > 1:
        detail = ", ".join(f"{g}:{len(objects[g])}ch" for g in gids)
        raise SystemExit(
            "All objects must have the same channel count to form one table.\n"
            f"Found mixed counts -> {detail}\n"
            "Fix the inputs so every object has the same number of channels."
        )
    num_channels = counts.pop()

    # trust_remote_code=True: we already have the model code locally
    model = AutoModel.from_pretrained("/morphem_inference/model_cache", trust_remote_code=True, local_files_only=True)
    model.to(device).eval()

    # Applied per single channel, so x[0] is that channel (matches the card).
    transform = v2.Compose([
        SaturationNoiseInjector(),
        PerImageNormalize(),
        v2.Resize(size=(224, 224), antialias=True),
    ])

    # Flatten to one work item per channel, remembering where each belongs.
    work = []   # (object_pos, channel_pos, transformed_tensor)
    for gp, gid in enumerate(gids):
        for cp, plane in enumerate(objects[gid]):
            t = transform(torch.from_numpy(plane).float().unsqueeze(0))  # (1,224,224)
            work.append((gp, cp, t))

    # Batched Bag-of-Channels inference.
    embeds = [[None] * num_channels for _ in gids]
    with torch.no_grad():
        for start in range(0, len(work), args.batch_size):
            chunk = work[start:start + args.batch_size]
            batch = torch.stack([w[2] for w in chunk], dim=0).to(device)  # (B,1,224,224)
            out = model.forward_features(batch)
            cls = out["x_norm_clstoken"].cpu().numpy()                    # (B,384)
            for (gp, cp, _), vec in zip(chunk, cls):
                embeds[gp][cp] = vec

    # Concatenate channels per object: (N, num_channels * 384).
    features = np.stack(
        [np.concatenate(embeds[gp], axis=0) for gp in range(len(gids))], axis=0
    )

    npy_path = os.path.join(args.output_folder, "morphem_features.npy")
    np.save(npy_path, features)

    csv_path = os.path.join(args.output_folder, "morphem_features.csv")
    header = ",".join(["object_id"] + [f"f{i}" for i in range(features.shape[1])])
    with open(csv_path, "w") as f:
        f.write(header + "\n")
        for gid, row in zip(gids, features):
            f.write(gid + "," + ",".join(map(str, row.tolist())) + "\n")

    print(f"Objects: {len(gids)}, channels each: {num_channels}, "
          f"features: {features.shape[1]} ({num_channels} x {CLS_DIM})")
    print(f"  {csv_path}")
    print(f"  {npy_path}")


if __name__ == "__main__":
    main()
