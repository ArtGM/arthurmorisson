# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Personal freelance site for Arthur Morisson (fullstack web developer), built with [Hugo](https://gohugo.io/) using the [hugo-profile](https://github.com/gurusabarish/hugo-profile) theme. The site's purpose is lead generation for freelance missions — every design decision should serve conversion over blogging.

## Commands

- `hugo server -D` — run the local dev server (includes drafts).
- `hugo` — build the static site into `public/`.
- `hugo new <section>/<slug>.md` — scaffold a content file from `archetypes/default.md` (new pages start with `draft: true`).
- `git submodule update --init --recursive` — required after clone, to pull the hugo-profile theme.

## Architecture

- **Theme via git submodule**: `themes/hugo-profile` is a submodule (see `.gitmodules`). Treat its files as read-only — override by mirroring the path under the repo root's `layouts/` or `static/`. The theme's own example config lives at `themes/hugo-profile/exampleSite/hugo.yaml` — use it as the source of truth for available params.
- **Single-file config**: everything lives in `hugo.yaml`. Unlike a typical theme-specific `config`, hugo-profile drives the *entire home page* from `params` (hero, about, experience, education, projects, achievements, contact). To edit the home page, edit `hugo.yaml` — don't look for a `content/_index.md`.
- **Matomo via `customScripts`**: the Matomo snippet (tracker at `analytics.lambofcode.com`, site id `3`) is injected via `params.customScripts` in `hugo.yaml`. The theme renders it before `</body>` — no template override needed. Do **not** re-introduce a `layouts/_default/baseof.html` override for analytics.
- **Custom Malt social icon**: `static/svg/icons/malt.svg` is referenced from `params.hero.socialLinks.customIcons` because hugo-profile's FontAwesome set doesn't ship a Malt icon.
- **Avatar**: `static/images/moi-square.jpg` (1536×1536). Used both as hero image (with `roundImage: true`) and as the about-section image.
- **Disabled sections**: `experience`, `education`, `projects`, `achievements` are set to `enable: false` until Arthur has real content to put there. Their navbar menu items are also disabled via `params.navbar.menus.disable*`. When enabling a section, flip both flags together.
