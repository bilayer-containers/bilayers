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
4. **The expected outputs appear.** In Gradio they're listed under **Download Output**
   with a **Download All (zip)** button; in Streamlit, under **Download results**; in
   Jupyter, in the output folder you set.

## Getting your images in

How you provide images depends on the interface:

| Interface | How inputs get in | Volume mount needed? |
| --- | --- | --- |
| Gradio | Upload in the browser | No |
| Streamlit | Upload in the browser | No |
| Jupyter | Mount a folder, or upload in the notebook if nothing is mounted | Recommended for more than a few images |

For Jupyter, the **host** side of the mount can be any folder, but the **container** side
must be the path the config declares for that input (usually `/bilayers/input_images`):

```bash
docker run --rm -p 7878:7878 \
  -v /any/host/path/my_images:/bilayers/input_images \
  <image>
```

When the notebook finds files in that folder, it shows **Using Mounted Directory** and
switches off uploading. If you see an upload button instead, the mount didn't land on the
right path.

To keep the results on your computer after the container stops, also mount a folder at
the output path shown in the interface (for example `-v /any/host/path/out:/bilayers/output_images`).
Gradio and Streamlit let you download results in the browser, so this is optional for them.

## If outputs don't appear

- **Jupyter:** check that the notebook says **Using Mounted Directory**. If it doesn't, the
  container-side path of your mount is wrong.
- **Gradio / Streamlit:** check that the upload finished before you clicked Run.
- Some tools only write certain results when a "save" checkbox is on. Check the
  interface's options.
- Read the error message. The interfaces show the tool's own error output when a run
  fails, which usually names the problem.
- If you think it's a bug, report it on [GitHub](https://github.com/bilayer-containers/bilayers/issues).
  Jupyter's **Report Issue** button fills in the error for you.

<!-- TODO: add interface-specific screenshots and a worked example (e.g. gaussian_smoothing
     with Gradio: pull, run, upload, expected output files). -->

