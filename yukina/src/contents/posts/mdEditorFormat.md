---
title: MD编写示例文件 
published: 2025-01-20
description: MD编写示例文件
tags: [Markdown, example]
first_level_category: 'blog理解文档'
second_level_category: 'blog' 
author: Alen
# sourceLink: "https://github.com/emn178/markdown"
draft: false
---
# md 文档编写示例
## 必填项
示例中 `title` , `published` , `description` 字段根据文件: `yukina\src\content.config.ts` 规则必须填写，具体规则为:

```js
const posts = defineCollection({
  loader: glob({
    pattern: "**/*.md",
    base: "src/contents/posts",
  }),
  // 使用 Zod 库来定义 Frontmatter 的 schema (结构)
  schema: z.object({
    title: z.string(), // 标题必须是字符串
    published: z.date(),// 发布日期必须是日期类型
    draft: z.boolean().optional(),//可选字段(.optional())，如果存在，必须是布尔值 (true 或 false)
    description: z.string().optional(),// 可选的字符串字段
    cover: z.string().optional(),
    tags: z.array(z.string()).optional(),//可选字段，如果存在，必须是一个字符串数组（如 tags: ["技术", "生活"]）。
    category: z.string().optional(),
    author: z.string().optional(),
    sourceLink: z.string().optional(),
    licenseName: z.string().optional(),
    licenseUrl: z.string().optional(),
  }),
});

```

```js
const specs = defineCollection({
  loader: glob({
    pattern: "**/*.md",
    base: "src/contents/specs",
  }),
});
// 它和 post 相比没有 schema 字段。
// loader 部分告诉 Astro 去 src/contents/specs 文件夹下查找所有 Markdown 文件。
// 缺少 schema 意味着 specs 集合里的 Markdown 文件可以有任意的 Frontmatter，
// 也可以没有任何 Frontmatter。Astro 不会对其进行任何格式或类型检查。
// 这提供了最大的灵活性，但同时也牺牲了类型安全。
// 导出所有集合
```

### 核心功能总结

1. **posts 集合**：
   - 专门用来管理博客文章。
   - 它从 src/contents/posts 文件夹中加载所有 Markdown 文件。
   - 它对每篇文章的元数据（Frontmatter）有**严格的格式要求**。如果文章的元数据不符合规定（例如缺少 title），Astro 在构建时会报错。
2. **specs 集合**：
   - 用来管理另一种类型的内容，可能是“说明书”、“规范”或“笔记”。
   - 它从 src/contents/specs 文件夹中加载所有 Markdown 文件。
   - 它对元数据**没有格式要求**，可以随意填写。

### 核心语法

使用`optional()`对模型的字段进行限制

### 注意事项

---

头部表单每一个选项填写格式为

字段:[空格]名字

titie: name

中间是有一个空格的，否则报错

---



