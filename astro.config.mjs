import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";
import netlify from "@astrojs/netlify";
import starlightThemeNova from "starlight-theme-nova";

// https://astro.build/config
export default defineConfig({
  integrations: [
    starlight({
      plugins: [starlightThemeNova()],
      title: "GpgFrontend",
      description: "A Free, Easy-to-Use, Cross-Platform OpenPGP Crypto Tool.",
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
          autogenerate: {
            directory: "overview",
          },
        },
        {
          label: "Brief Guides",
          autogenerate: {
            directory: "guides",
          },
        },
        {
          label: "Advanced Features",
          autogenerate: {
            directory: "advanced",
          },
        },
        {
          label: "Appendix",
          autogenerate: {
            directory: "appendix",
          },
        },
        {
          label: "Extra",
          autogenerate: {
            directory: "extra",
          },
        },
      ],
      customCss: ["./src/styles/custom.css"],
    }),
  ],
  output: "server",
  adapter: netlify(),
});
