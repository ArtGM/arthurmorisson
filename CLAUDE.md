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
- **`params.customScripts` is the inline-JS bucket**: the theme renders this block before `</body>`. It currently holds (a) the Matomo snippet (tracker at `analytics.lambofcode.com`, site id `3`) and (b) the hero particle background + hero-heading particle-text effect. When editing one, mind that you're sharing the block with the others. Do **not** re-introduce a `layouts/_default/baseof.html` override for analytics — the `customScripts` hook is enough.
- **`layouts/` override is minimal**: only `layouts/partials/head/extensions.html` is overridden, to inject canonical, robots, keywords and the home-page schema.org JSON-LD graph (Person + ProfessionalService + WebSite). The theme already wires the internal `opengraph.html` and `twitter_cards.html` partials, so basic OG/Twitter come from `params.title` / `params.description` / `params.images` — no override needed for them.
- **Disabled sections that are now enabled**: `experience` and `projects` are now `enable: true` with TODO placeholders. `education` and `achievements` stay disabled. When filling the placeholders, also flip the matching `navbar.menus.disable*` flag if you turn a section back off.
- **Netlify pinning**: `netlify.toml` pins `HUGO_VERSION` to the local one (extended). The theme requires extended Hugo (SCSS), so if you bump the local Hugo version, update `netlify.toml` in the same commit or production will silently fall back to Netlify's old default and break the build.
- **Custom Malt social icon**: `static/svg/icons/malt.svg` is referenced from `params.hero.socialLinks.customIcons` because hugo-profile's FontAwesome set doesn't ship a Malt icon.
- **Avatar**: `static/images/moi-square.jpg` (1536×1536). Used both as hero image (with `roundImage: true`) and as the about-section image.
- **Disabled sections**: `experience`, `education`, `projects`, `achievements` are set to `enable: false` until Arthur has real content to put there. Their navbar menu items are also disabled via `params.navbar.menus.disable*`. When enabling a section, flip both flags together.

## Commit & PR conventions

- **Never add `Co-Authored-By: Claude …` trailers** to commit messages or pull request descriptions. The author wants a clean `git blame` without Claude attribution noise. This overrides the default Claude Code commit template — drop the `Co-Authored-By` line entirely, don't just swap the identity.
