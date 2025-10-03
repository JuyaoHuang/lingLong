import { defineConfig } from "astro/config";

import icon from "astro-icon";
import sitemap from "@astrojs/sitemap";
import tailwind from "@astrojs/tailwind";
import svelte from "@astrojs/svelte";
import swup from "@swup/astro";

import rehypeSlug from "rehype-slug";
import rehypeKatex from "rehype-katex";
import rehypeAutolinkHeadings from "rehype-autolink-headings";
import remarkMath from "remark-math";

import LingLongConfig from "./linglong.config";

import pagefind from "astro-pagefind";
import removeConsole from "vite-plugin-remove-console";

// https://astro.build/config
export default defineConfig({
  site: LingLongConfig.site,
  integrations: [
    tailwind(),
    svelte(),
    icon(),
    swup({
      theme: false,
      containers: ["main", "footer", ".banner-inner"],
      smoothScrolling: true,
      progress: true,
      cache: true,
      preload: true,
      updateHead: true,
      updateBodyClass: false,
      globalInstance: true,
    }),
    sitemap(),
    pagefind(),
  ],
  vite: {
    plugins: [
      // 只在生产构建时移除 console
      removeConsole({
        external: ['error', 'warn'], // 保留 console.error 和 console.warn
      }),
    ],
  },
  markdown: {
    shikiConfig: {
      theme: "github-dark-default",
    },
    remarkPlugins: [remarkMath],
    rehypePlugins: [
      rehypeSlug,
      rehypeKatex,
      [
        rehypeAutolinkHeadings,
        {
          behavior: "prepend",
        },
      ],
    ],
  },
});
