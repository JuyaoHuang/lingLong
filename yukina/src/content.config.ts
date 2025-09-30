import { glob } from "astro/loaders";
import { defineCollection, z } from "astro:content";


const posts = defineCollection({
  loader: glob({
    pattern: "**/*.md",
    base:"src/contents/posts",
  }),
  // post 目录下
  schema: z.object({
    title: z.string(), // 标题必须是字符串
    published: z.date(),
    draft: z.boolean().optional(),//optional 可选字段
    description: z.string().optional(),
    cover: z.string().optional(),// 文章封面图片
    tags: z.array(z.string()).optional(),
    // category: z.string().optional(),
    first_level_category: z.string(),//一级标题
    second_level_category:z.string(),//二级标题
    author: z.string().optional(),
    sourceLink: z.string().optional(),
    licenseName: z.string().optional(),
    licenseUrl: z.string().optional(),
    readingMetadata: z
      .object({
        time: z.number(),
        wordCount: z.number(),
      })
      .optional(),
  }),
});

const specs = defineCollection({
  loader: glob({
    pattern: "**/*.md",
    base: "src/contents/specs",
  }),
});

export const collections = { posts, specs };
