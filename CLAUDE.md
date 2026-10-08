# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Personal freelance site for Arthur Morisson, built with [Hugo](https://gohugo.io/). The site's purpose is lead generation for freelance missions: every decision should serve conversion over blogging.

**Audience**: small businesses, tradespeople and sole traders who do not understand the technical side, or do not want to. Write visible copy in the customer's words, never the trade's. "Mon site n'apparaît plus sur Google", not "SEO". Keep technical vocabulary to the collapsed block on the home page, the keywords and the JSON-LD, where only machines read it.

**Typography of the copy**: no em dashes, no emoji. Use colons, commas or periods. Do not add decorative side borders to blocks you create.

## Commands

- `hugo server -D` — local dev server, drafts included.
- `hugo --gc --minify` — production build into `public/`, same command Netlify runs.
- `hugo new blog/<slug>.md` — new post from `archetypes/blog.md`.

No submodule step: the site has no external theme any more.

## Architecture

- **The theme was internalised**, on 8 October 2026. `layouts/` and `static/` started as a copy of [hugo-profile](https://github.com/gurusabarish/hugo-profile) (MIT) and are now the site's own code. There is no `theme:` key in `hugo.yaml` and no `themes/` directory. Edit the templates directly; there is nothing to override any more. Upstream updates are no longer pulled, which is deliberate: six near-complete copies of theme files had accumulated, and one of them silently reloaded FontAwesome on every content page.
- **What was deliberately not copied from the theme**: `static/fontawesome-6/` (9.5 MB for six icons) and `static/viewer/` with `layouts/_default/gallery.html`, which depended on it. Icons are rendered by `static/css/icons.css`, which masks the handful of SVGs in `static/svg/icons/`. Adding an icon means copying its SVG there and adding a rule; the file says so.
- **Single-file config**: everything about the home page lives in `hugo.yaml` `params` (hero, about, experience, projects, contact). There is no `content/_index.md`.
- **`params.customScripts` is the inline-JS bucket**, rendered before `</body>` by `layouts/partials/scripts.html` on every page, without template execution, so values cannot be injected from params there. It holds the consent banner and GA4, the phone reassembly script, and the background particle canvas. Mind that you share the block when editing one of them.
- **Netlify pinning**: `netlify.toml` pins `HUGO_VERSION` to the local one (extended, required for SCSS). Bump both in the same commit or production silently falls back and breaks.

## Conventions that cost time to rediscover

- **All CSS is bundled in `layouts/partials/head.html`**, from `assets/css/`, concatenated then minified and fingerprinted into one request. `assets/css/zz-custom.css` holds our own rules and must stay last in the list so it wins without `!important`; the `zz` prefix protects that order. Note that a class selector still loses to an ID selector from the theme even with `!important` on both, which is why some rules carry a `#section` prefix.
- **Bootstrap is compiled from source**, `assets/scss/bootstrap-custom.scss`, importing only the modules the markup uses and trimming the utilities map. Hugo extended ships libsass, so there is no npm and no bundler. The file lists what was left out and why. Watch out for one thing: the navbar template can render a dropdown if a menu entry is given children, and the dropdown module is not imported.
- **`hugo --minify` does not touch `static/`**, it copies those files verbatim. Anything that should be minified belongs in `assets/`.
- **The phone number is never written in plain HTML.** It lives in `params.contact.phone`; `layouts/partials/contact-phone.html` encodes it at build time and the script in `customScripts` rebuilds it. Mode `wa` renders a WhatsApp link, mode `legal` a `tel:` link for the legal notices.
- **Images in markdown go through `layouts/_default/_markup/render-image.html`**, which adds lazy loading, width and height, and a blurred placeholder read from `data/lqip.yaml`. The regeneration script sits in that file's header comment.
- **Dates are printed only for blog posts**, by a section test in `layouts/_default/single.html`.
- **Netlify Forms needs the `<form>` in the static HTML**, so check it survives in `public/` after any change to `layouts/partials/contact-form.html`.
- **Verify in a browser, not only in the build.** Several defects found here passed the build and failed on screen: unreadable particle text, white-on-teal buttons, a lost hanging indent, a 403 on a client site. Playwright is available.

## Commit & PR conventions

- **Never add `Co-Authored-By: Claude …` trailers** to commit messages or pull request descriptions. The author wants a clean `git blame`. Drop the line entirely rather than swapping the identity.
