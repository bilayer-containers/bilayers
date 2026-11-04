---
title: User Testing
authors:
  - name: Cimini Lab
    affiliations:
      - Broad Institute of MIT and Harvard
---

You're running a pre-built Bilayers image and want to confirm it actually works. This
page is about *verifying a run*, not writing automated tests.

## What "working" looks like

1. **The interface launches.** The app/notebook/plugin loads without errors.
2. **Inputs are accepted.** Mount or upload your images to the location the interface
   expects (see [Run a Bilayers Image](../tool_user/steps_to_run.md)).
3. **The run completes** with no error dialog or traceback.
4. **The expected outputs appear** — the result files the algorithm's catalog entry
   says it produces.

## Mounting inputs to the right place

Container-based interfaces read inputs from a fixed path inside the container (for
example `/bilayers/input_images`). The **host** side of a volume mount can be any
folder, but the **container** side must match what the config declares:

```bash
# Gradio/Jupyter listen on 7878, Streamlit on 8501
docker run --rm -p <port>:<port> \
  -v /any/host/path/my_images:/bilayers/input_images \
  -v /any/host/path/out:/bilayers/output_images \
  <image>
```

If you mount to a different container path, the tool won't find your data.

## If outputs don't appear

- Confirm you mounted inputs to the **exact** container path the config expects.
- Confirm any "save output" options the tool exposes are actually enabled — some tools
  only write results when a save flag/checkbox is on.
- Check the run log for a message from the underlying tool.

:::{note}
This page is a starting point — expand with interface-specific screenshots and a
worked example once the catalog pages are populated.
:::
