"""
MorphEm feature extraction, wrapped as a Bilayers CLI entrypoint.

Model contract (from the CaicedoLab/MorphEm card):
  - Input is SINGLE-CHANNEL, ALREADY-SEGMENTED cell imagery. MorphEm does not
    find cells. It does not segment. It only makes feature vectors.
  - Multi-channel data is handled by "Bag of Channels": run each channel on its
    own, then concatenate the per-channel embeddings.
  - Each channel embedding is the ViT-Small CLS token (384 numbers).

Input contract this wrapper enforces:
  - One file = one object. Every object has --num_channels channels.
  - --concatenated=False: each file is already a stack. A 2D file is one
    channel (num_channels must be 1); a 3D file is (C,H,W) or (H,W,C).
  - --concatenated=True: each file is a horizontal CHAMMI-75 strip shaped
    (H, W*C). It is split along the width into C planes of width W/C.
  - Every object yields exactly num_channels planes, so the output table is
    rectangular: O objects x (num_channels * 384).
"""

import argparse
import glob
import os

import numpy as np
import torch
import torch.nn as nn
from torchvision import transforms as v2
from transformers import AutoModel

import tifffile
from PIL import Image
import pandas as pd


CLS_DIM = 384                                                       # ViT-Small CLS token width
IMG_EXTS = (".png", ".jpg", ".jpeg", ".tif", ".tiff", ".npy")       # specified in the config.yaml


# --- Preprocessing transforms (from the MorphEm model card) ---

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

def _to_chw(arr: np.ndarray, path: str, num_channels: int) -> np.ndarray:
    """Return a float32 array shaped (C, H, W) from any 2D or 3D input array.
    num_channels is required to tell us which axis of a 3D array is channels,
    """
    arr = arr.astype(np.float32)
    if arr.ndim == 2:
        return arr[None, ...]
    if arr.ndim == 3:
        if arr.shape[0] == num_channels:         # already C, H, W
            return arr
        if arr.shape[2] == num_channels:         # H, W, C  ->  C, H, W
            return np.transpose(arr, (2, 0, 1))
        raise ValueError(
            f"{os.path.basename(path)}: no axis matches num_channels "
            f"{num_channels} in array shape {arr.shape}."
        )
    raise ValueError(f"Unsupported array shape {arr.shape} in {path}")


def load_image(path: str, num_channels: int) -> np.ndarray:
    """Load any supported file, return as float32 (C, H, W)
    -> expected input for MorphEm model."""

    lower = path.lower()
    if lower.endswith(".npy"):
        arr = np.load(path)
        return _to_chw(arr, path, num_channels)
    if lower.endswith((".tif", ".tiff")):
        return _to_chw(tifffile.imread(path), path, num_channels)

    # PNG / JPG via PIL.
    arr = np.array(Image.open(path)).astype(np.float32)
    if arr.ndim == 3:
        # Drop an alpha channel if present.
        if arr.shape[2] == 4:
            arr = arr[:, :, :3]
        # Grayscale saved as RGB: identical planes collapse to one channel.
        if arr.shape[2] > 1 and np.all(arr[:, :, 0:1] == arr):
            arr = arr[:, :, 0]
    return _to_chw(arr, path, num_channels)


# --- One file -> one object's channel planes ---

def load_object(path: str, num_channels: int, concatenated: bool):
    """Return a list of num_channels single-channel (H, W) planes."""
    if concatenated:
        # a horizontal CHAMMI-75 strip: one 2D image (H, W*C) split into C planes.
        chw = load_image(path, num_channels=1)   # (1, H, W*C)
        if chw.shape[0] != 1:
            raise SystemExit(
                f"{os.path.basename(path)}: --concatenated expects a single "
                f"2D strip but got {chw.shape[0]} array channels."
            )
        _, h, w = chw.shape
        if w % num_channels != 0:
            raise SystemExit(
                f"{os.path.basename(path)}: width {w} is not divisible by "
                f"num_channels {num_channels}; cannot split the strip."
            )
        step = w // num_channels
        return [chw[0, :, i * step:(i + 1) * step] for i in range(num_channels)]

    # already-stacked file
    chw = load_image(path, num_channels)   # (C, H, W)
    return [chw[k] for k in range(num_channels)]


# --- Main ---

def main():
    parser = argparse.ArgumentParser(description="MorphEm feature extraction")
    parser.add_argument("-i", "--input_folder", required=True,
                        help="Folder of pre-segmented cell images, one file per object")
    parser.add_argument("-o", "--output_folder", required=True,
                        help="Where to write the feature CSV and NPY")
    parser.add_argument("-b", "--batch_size", type=int, default=32,
                        help="Single channels processed per forward pass")
    parser.add_argument("-c", "--num_channels", type=int, default=1,
                        help="Number of channels per object")
    parser.add_argument("--concatenated", action="store_true",
                        help="Input files are horizontal (H, W*C) multi-channel strips")
    parser.add_argument("--output_format", choices=("pkl", "csv"), default="pkl",
                        help="Format of the feature table written to the output folder")
    args = parser.parse_args()

    if args.num_channels < 1:
        raise SystemExit("--num_channels must be >= 1")

    os.makedirs(args.output_folder, exist_ok=True)

    # TODO: Add GPU support
    device = "cpu"

    # find all supported images in the input folder, recursively.
    paths = sorted(
        p for p in glob.glob(os.path.join(args.input_folder, "**", "*"), recursive=True)
        if p.lower().endswith(IMG_EXTS)
    )
    if not paths:
        raise SystemExit(f"No supported images found in {args.input_folder}")

    # One file = one object, each split into exactly num_channels planes.
    gids = [os.path.splitext(os.path.basename(p))[0] for p in paths]                        # global id of each object
    objects = [load_object(p, args.num_channels, args.concatenated) for p in paths]

    # run the model (from the MorphEm model card)
    # model exist locally, so local_files_only=True to avoid downloading from the internet
    model = AutoModel.from_pretrained("/morphem_inference/model_cache", trust_remote_code=True, local_files_only=True)
    model.to(device).eval()

    transform = v2.Compose([
        SaturationNoiseInjector(),
        PerImageNormalize(),
        v2.Resize(size=(224, 224), antialias=True),
    ])

    # Bag of Channels: one channel at a time, objects processed in batch_size chunks.
    # each forward pass sees (B, 1, 224, 224) -> per channel we build an (O, 384) array.
    per_channel = []   # per_channel[c] is (O, 384)
    with torch.no_grad():
        for c in range(args.num_channels):
            planes = [transform(torch.from_numpy(obj[c]).float().unsqueeze(0)) for obj in objects]
            feats = []
            for start in range(0, len(planes), args.batch_size):
                batch = torch.stack(planes[start:start + args.batch_size], dim=0).to(device)  # (B,1,224,224)
                out = model.forward_features(batch)
                feats.append(out["x_norm_clstoken"].cpu().numpy())    # (B, 384)
            per_channel.append(np.concatenate(feats, axis=0))          # (O, 384)

    # concatenate channels per object: (O, num_channels * 384).
    features = np.concatenate(per_channel, axis=1)

    # save the feature table (one row per object) in the requested format.
    df = pd.DataFrame(features, columns=[f"f{i}" for i in range(features.shape[1])])
    df.insert(0, "object_id", gids)

    out_path = os.path.join(args.output_folder, f"morphem_features.{args.output_format}")
    if args.output_format == "csv":
        df.to_csv(out_path, index=False)
    else:  # pkl
        df.to_pickle(out_path)

    print(f"Objects: {len(gids)}, channels each: {args.num_channels}, "
          f"features: {features.shape[1]} ({args.num_channels} x {CLS_DIM})")
    print(f"  {out_path}")


if __name__ == "__main__":
    main()
