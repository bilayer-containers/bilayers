---
title: Talks & Tutorials
authors:
  - name: Cimini Lab
    affiliations:
      - Broad Institute of MIT and Harvard
---

Videos, slides, and posters about Bilayers, newest first within each section. If you've given a talk or made a tutorial about Bilayers, add it here (see [the end of this page](#add-yours)).

## Video tutorials

### Introduction to Bilayers

*Introduction to Bilayers – a container specification for whole-community support*

```{iframe} https://www.youtube.com/embed/X-7HTI1ZGUc
:width: 100%

[Watch on YouTube](https://www.youtube.com/watch?v=X-7HTI1ZGUc)
```

An overview of what Bilayers is, why it exists, and how a config turns into an interface. It's a good place to start before reading the [User Guide](../user_guide/user_guide.md) or [wrapping your own tool](../developer_guide/wrap_algorithm.md).

## Slides and presentations

| Title | Event | Date | Link |
| --- | --- | --- | --- |
| Bilayers – an easy way to make your favorite deep learning tool more user-friendly (Beth Cimini) | SLAS 2025, San Diego, CA | January 2025 | [Slides (PDF) on Zenodo](https://doi.org/10.5281/zenodo.14751700) |

## Posters

| Title | Event | Date | Link |
| --- | --- | --- | --- |
| Bilayers – an easy way to make your favorite deep learning tool more user-friendly (Rajavi Shah, Nodar Gogoberidze, Beth Cimini) | I2K 2024, Milan, Italy (Poster Session #1, board 23) | October 2024 | [Abstract](https://events.humantechnopole.it/event/1/contributions/94/) |

(cite-bilayers)=
## Cite Bilayers

Each `bilayers` release is archived on Zenodo. To cite the software:

- **Any version:** [doi.org/10.5281/zenodo.17652333](https://doi.org/10.5281/zenodo.17652333). This DOI always resolves to the latest release.
- **A specific release:** use that release's own DOI from its Zenodo page (for example `v1.0.0rc1`: [10.5281/zenodo.17652334](https://doi.org/10.5281/zenodo.17652334)).

`CITATION.cff` in the [`bilayers` repository](https://github.com/bilayer-containers/bilayers) has the full author list; GitHub's **Cite this repository** button uses it. When you publish results made with a Bilayers tool, also cite the tool itself; every generated interface lists the citations from its config.

## Other links

- [Bilayers on DockerHub](https://hub.docker.com/u/bilayer): all published images
- [GitHub Discussions](https://github.com/orgs/bilayer-containers/discussions): questions, ideas, and the running lists of tools and interfaces planned next
- [Bilayers Config Generator](https://bilayer-containers.github.io/bilayers-config-generator/): fill out a `config.yaml` with a form
- [Cimini Lab software page](https://ciminilab.github.io/WeMakeStuff): Bilayers alongside the lab's other tools

(add-yours)=
## Add yours

Open a pull request against [`bilayers`](https://github.com/bilayer-containers/bilayers) that adds a row to the right table in `docs/resources/talks_tutorials.md`. Include the title, the event, the month, and a stable link: a DOI (Zenodo works well for slides and posters) or a YouTube link for videos. To embed a video like the one above, copy the `{iframe}` block and swap in the video's ID (`https://www.youtube.com/embed/<id>`).
