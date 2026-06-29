import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";
import netlify from "@astrojs/netlify";
import starlightThemeNova from "starlight-theme-nova";
import sitemap from "@astrojs/sitemap";
import starlightLinksValidator from "starlight-links-validator";

// https://astro.build/config
export default defineConfig({
  site: "https://gpgfrontend.bktus.com",
  integrations: [
    starlight({
      plugins: [starlightThemeNova(), starlightLinksValidator()],
      title: "GpgFrontend",
      description: "A Free, Easy-to-Use, Cross-Platform OpenPGP Crypto Tool.",
      lastUpdated: true,
      head: [
        {
          tag: "meta",
          attrs: { property: "og:type", content: "website" },
        },
        {
          tag: "meta",
          attrs: { property: "og:site_name", content: "GpgFrontend" },
        },
        {
          tag: "meta",
          attrs: {
            property: "og:url",
            content: "https://gpgfrontend.bktus.com",
          },
        },
        {
          tag: "meta",
          attrs: { name: "twitter:card", content: "summary_large_image" },
        },
        {
          tag: "meta",
          attrs: {
            property: "og:image",
            content: "https://gpgfrontend.bktus.com/images/og-default.png",
          },
        },
        {
          tag: "meta",
          attrs: { property: "og:image:width", content: "1200" },
        },
        {
          tag: "meta",
          attrs: { property: "og:image:height", content: "630" },
        },
        {
          tag: "meta",
          attrs: {
            property: "og:image:alt",
            content: "GpgFrontend, a free, cross-platform OpenPGP crypto tool.",
          },
        },
        {
          tag: "meta",
          attrs: {
            name: "twitter:image",
            content: "https://gpgfrontend.bktus.com/images/og-default.png",
          },
        },
      ],
      logo: {
        src: "./src/assets/logo.svg",
      },
      favicon: "/images/favicon.ico",
      social: [
        {
          icon: "github",
          label: "GitHub",
          href: "https://github.com/saturneric/GpgFrontend",
        },
      ],
      editLink: {
        baseUrl: "https://github.com/saturneric/GpgFrontend-Manual/edit/main/",
      },
      sidebar: [
        {
          label: "Overview",
          items: [{ autogenerate: { directory: "overview" } }],
        },
        {
          label: "Brief Guides",
          items: [{ autogenerate: { directory: "guides" } }],
        },
        {
          label: "Advanced Features",
          items: [{ autogenerate: { directory: "advanced" } }],
        },
        {
          label: "Appendix",
          items: [{ autogenerate: { directory: "appendix" } }],
        },
        {
          label: "Extra",
          items: [{ autogenerate: { directory: "extra" } }],
        },
      ],
      customCss: ["./src/styles/custom.css"],
      expressiveCode: {
        themes: ["github-dark", "github-light"],
        styleOverrides: { codeFontSize: "0.9rem" },
        defaultProps: {
          showLineNumbers: true,
          wrap: true,
        },
      },
    }),
    sitemap(),
  ],
  output: "static",
  adapter: netlify(),
});
