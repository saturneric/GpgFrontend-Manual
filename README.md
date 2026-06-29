# GpgFrontend User Manual

This repository holds the source for the GpgFrontend user manual, published at
**https://www.gpgfrontend.bktus.com/**.

The site is built with [Astro](https://astro.build/) and the
[Starlight](https://starlight.astro.build/) docs theme. You write pages in
Markdown, and the site takes care of the layout, navigation, and search.

You do not need to be a programmer to help. If you can edit a text file, you can
improve this manual.

## What you need

- **Node.js 22.12 or newer.** The version is pinned in [`.nvmrc`](.nvmrc). Check
  yours with `node --version`.
- A package manager. The examples below use `yarn`, but `npm` works the same way
  (`npm install`, `npm run dev`, and so on).

If you use [nvm](https://github.com/nvm-sh/nvm), run `nvm use` in the project
folder to switch to the right Node version.

## Run the site on your computer

```bash
yarn install     # install dependencies, only needed the first time
yarn dev         # start the local preview server
```

Then open the address it prints (usually http://localhost:4321). The page
reloads on its own each time you save a file, so you can see your changes right
away.

## Where the pages live

All manual pages are in `src/content/docs/`, grouped into folders that match the
sidebar:

| Folder      | Sidebar group     | What goes here                         |
| ----------- | ----------------- | -------------------------------------- |
| `overview/` | Overview          | Intro, downloads, getting started, FAQ |
| `guides/`   | Brief Guides      | Step-by-step how-to pages              |
| `advanced/` | Advanced Features | Deeper topics for power users          |
| `appendix/` | Appendix          | Reference material, dev setup          |
| `extra/`    | Extra             | Background notes and comparisons       |

The sidebar fills itself from these folders, so adding a file is enough to make
it appear. There is no separate list to update.

Other useful locations:

- `src/assets/` holds the logo and other site images used by the layout.
- `public/` holds files served as-is, such as `favicon.ico` and `robots.txt`.
- `astro.config.mjs` holds site settings, the sidebar order, and SEO tags.

## Edit a page

Open any file in `src/content/docs/` and change the text. Each page starts with
a short block of settings called frontmatter, written between two `---` lines:

```markdown
---
title: Generate Key Pair
description: "A short summary used for search results and link previews."
sidebar:
  order: 3
---

Your page content starts here, written in Markdown.
```

- **`title`** is required. It shows at the top of the page and in the sidebar.
- **`description`** is used for search and social link previews. Keep it to one
  clear sentence.
- **`sidebar.order`** sets the position inside its group. Lower numbers come
  first. Leave it out and the page sorts by title.

## Add a new page

1. Create a file in the right folder, for example
   `src/content/docs/guides/my-topic.md`.
2. Add the frontmatter block shown above, at least a `title`.
3. Write your content below it.
4. Save. The page appears in the sidebar on its own.

Use clear, simple file names with words joined by hyphens, such as
`generate-key.md`. The file name becomes part of the page address.

## Markdown and MDX

Most pages use plain Markdown (`.md`). Some pages need extra building blocks like
tabs or cards, and those use MDX (`.mdx`). MDX is Markdown plus components you
import at the top of the file:

```mdx
import { Tabs, TabItem, Aside } from "@astrojs/starlight/components";

<Tabs>
  <TabItem label="Windows">Windows steps here.</TabItem>
  <TabItem label="macOS">macOS steps here.</TabItem>
</Tabs>
```

A few tips that save trouble:

- For callout boxes, use the `<Aside>` component inside MDX rather than the
  `:::note` text style. The `:::` style can clash with components like tabs and
  break the build. Both look the same on the page.
- You can keep using `:::note`, `:::tip`, and `:::caution` in plain `.md` files,
  where there are no components to clash with.

See the [Starlight component guide](https://starlight.astro.build/guides/components/)
for the full list.

## Images

Page images are hosted on an external CDN and linked by full address:

```markdown
![](https://image.cdn.bktus.com/i/path/to/image.webp)
```

This keeps the repository small. Upload your image to the CDN first, then paste
its address.

## Links

Use absolute paths for links between manual pages, ending with a slash:

```markdown
See the [Getting Started Guide](/overview/getting-started/).
```

The build checks every internal link. If a link points to a page that does not
exist, the build fails and tells you which link is wrong, so broken links never
reach the live site.

## Check your work before sharing

```bash
yarn build       # build the full site the way it ships
```

This catches broken links, bad frontmatter, and MDX mistakes. If it finishes
without errors, your changes are safe to submit.

You can also click the **Edit page** link at the bottom of any published page to
jump straight to its source on GitHub.

## How it gets published

You do not run these yourself, but for reference:

- **Netlify** builds and hosts the site from the `main` branch. Settings are in
  [`netlify.toml`](netlify.toml).
- A **Docker** image is also built for self-hosting, using the
  [`Dockerfile`](Dockerfile) and [`nginx.conf`](nginx.conf).

Both run `yarn build` (or `npm run build`), the same command you run locally.

## Contributing

1. Make your edits on a branch.
2. Run `yarn build` and confirm it passes.
3. Open a pull request against `main`.

Thank you for helping improve the GpgFrontend manual.
