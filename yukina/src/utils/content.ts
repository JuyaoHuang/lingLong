import { getCollection } from "astro:content";
import { IdToSlug } from "./hash";

// ================== 二级分类系统改进总结 ==================
//
// 本文件实现了从单级分类到二级分类系统的重要改进：
//
// 【改进前】：
// - 文章只有一个 category 字段
// - 分类结构：主页 -> 分类列表 -> 文章列表（时间线形式）
//
// 【改进后】：
// - 文章有 first_level_category 和 second_level_category 两个字段
// - 分类结构：主页 -> 一级分类列表 -> 二级分类列表 -> 文章列表（卡片形式）
// - 支持更精细的内容分类，如：编程合集/Python、AI前沿/深度学习
//
// 【主要变化】：
// 1. 新增 postCard 接口 - 支持完整的卡片展示数据
// 2. 新增 secondCategory 接口 - 管理二级分类信息
// 3. 更新 fisrtCategory 接口 - 专门处理一级分类
// 4. 新增 getSecondCategories() 方法 - 获取所有二级分类
// 5. 更新 getFirstCategories() 方法 - 专门处理一级分类
//
// 【路由结构】：
// /categories/                           -> 显示所有一级分类（ChipLayout）
// /categories/[first_category]/          -> 显示该一级分类下的二级分类列表
// /categories/[first_category]/[second_category]/ -> 显示该二级分类下的文章卡片
// =========================================================

// 从Astro的内容集合（Content Collections）中获取所有的博客文章。
// 对这些文章进行筛选（例如，在生产环境中过滤掉草稿）、排序（按日期）、分组（按年份、按标签、按分类）。
// 将原始的文章数据，处理成特定页面需要的、结构化的数据格式（例如，一个按年份组织的归档列表）。

/**
 * Represents an archive item with a title, slug, date, and optional tags.
 * Archive: 代表一个简化的文章对象。注意，它只包含了 title, id, date, tags 这几个核心信息。
 * 它不包含文章的完整内容(body)，因此非常适合用在列表、归档等不需要显示全文的场景，可以减小数据处理量。
 */
export interface Archive {
  title: string;
  id: string;
  date: Date;
  tags?: string[];
}

/*
  修改：新增用于二级分类板块的文章对象接口
  与原来的Archive接口不同，这个接口包含了完整的PostCard所需数据
  用于在二级分类页面以卡片形式展示文章
*/
export interface postCard{
  id: string;
  title: string;
  published: Date;
  category?:string;  // 保留兼容性，但新系统不使用
  first_level_category?: string;  // 【新增】一级分类
  second_level_category?: string; // 【新增】二级分类
  tags?: string[];
  description?: string;
  image?: string;
  readingMetadata?: { time: number; wordCount: number };
}

/**
 * 修改：新增二级分类对象接口
 * 包含分类名，完整的分类路径URL，和该分类下的文章数组
 * 用于构建二级分类页面的路由和数据
 */
export interface secondCategory{
  name:string;        // 二级分类名称，如 "Python", "Vue"
  slug:string;        // 完整路径，如 "/categories/编程合集/python"
  posts:postCard[];   // 该分类下的所有文章
}

/**
 * Represents a tag used to categorize content.
 */
export interface Tag {
  name: string;
  slug: string;
  posts: Archive[];
}

/**
 * 修改：更新一级分类接口名称和注释
 * 原来叫 Category，现在改为 fisrtCategory 以区分一级和二级分类
 * 包含一级分类名、URL路径和该分类下的所有文章（简化版Archive对象）
 */
export interface fisrtCategory {
  name: string;      // 一级分类名称，如 "编程合集", "AI前沿"
  slug: string;      // 一级分类URL路径，如 "/categories/编程合集"
  posts: Archive[];  // 该分类下的所有文章（简化版，用于归档显示）
}

/**
 * Retrieves and sorts blog posts by their published date.
 *
 * This function fetches all blog posts from the "posts" collection, filters out drafts if in production mode,
 * and sorts them in descending order by their published date. It also adds `nextSlug`, `nextTitle`, `prevSlug`,
 * and `prevTitle` properties to each post for navigation purposes.
 *
 * @returns A promise that resolves to an array of sorted blog posts with navigation properties.
 */
export async function GetSortedPosts() {
  const allBlogPosts = await getCollection("posts", ({ data }) => {
    return import.meta.env.PROD ? data.draft !== true : true;
  });
  const sorted = allBlogPosts.sort((a, b) => {
    const dateA = new Date(a.data.published);
    const dateB = new Date(b.data.published);
    return dateA > dateB ? -1 : 1;
  });

  for (let i = 1; i < sorted.length; i++) {
    (sorted[i].data as any).nextSlug = (sorted[i - 1] as any).slug;
    (sorted[i].data as any).nextTitle = sorted[i - 1].data.title;
  }
  for (let i = 0; i < sorted.length - 1; i++) {
    (sorted[i].data as any).prevSlug = (sorted[i + 1] as any).slug;
    (sorted[i].data as any).prevTitle = sorted[i + 1].data.title;
  }

  return sorted;
}

/**
 * Retrieves and organizes blog post archives.
 * 检索并组织博客文章档案。
 * This function fetches all blog posts from the "posts" collection, filters them based on the environment
 * (excluding drafts in production), and organizes them into a map of archives grouped by year.
 * Each archive entry contains the post's title, slug, publication date, and tags.
 * The archives are sorted in descending order by year and by date within each year.
 * 此函数从“posts”集合中获取所有博客文章，并根据环境进行筛选
 * （不包括生产环境中的草稿），然后将它们整理成按年份分组的存档图。
 * 每个存档条目包含文章的标题、slug、发布日期和标签。
 * 存档按年份和年份内的日期降序排列。
 * @returns A promise that resolves to a map of archives grouped by year.
 */
export async function GetArchives() {
  const allBlogPosts = await getCollection("posts", ({ data }) => {
    return import.meta.env.PROD ? data.draft !== true : true;
  });

  const archives = new Map<number, Archive[]>();

  for (const post of allBlogPosts) {
    const date = new Date(post.data.published);
    const year = date.getFullYear();
    if (!archives.has(year)) {
      archives.set(year, []);
    }
    archives.get(year)!.push({
      title: post.data.title,
      id: `/posts/${IdToSlug(post.id)}`,
      date: date,
      tags: post.data.tags,
    });
  }

  const sortedArchives = new Map(
    [...archives.entries()].sort((a, b) => b[0] - a[0]),
  );
  sortedArchives.forEach((value) => {
    value.sort((a, b) => (
      a.date > b.date ? -1 : 1
    ));
  });

  return sortedArchives;
}

/**
 * Retrieves all tags from blog posts.
 *
 * This function fetches all blog posts from the "posts" collection and extracts tags from each post.
 * It then organizes the tags into a map where each tag is associated with its metadata and the posts that have that tag.
 *
 * 
 *  执行流程:
      获取并过滤所有文章。
      创建一个 Map 对象 tags，用于存储 标签slug -> Tag对象 的关系。
      遍历所有文章，再遍历每篇文章的 tags 数组。
      对于每个标签，如果它没在 tags Map里出现过，就创建一个新的Tag对象。
      将当前文章处理成一个**Archive对象**，推入这个标签对应的 posts 数组中。
    输出: 一个 Map 对象。键是标签的slug(string)，值是包含该标签下所有文章的**Tag对象**。
 * @returns A promise that resolves to a map of tags. Each key is a tag slug, and the value is an object containing the tag's name, slug, and associated posts.
 */
export async function GetTags() {
  const allBlogPosts = await getCollection("posts", ({ data }) => {
    return import.meta.env.PROD ? data.draft !== true : true;
  });

  const tags = new Map<string, Tag>();
  allBlogPosts.forEach((post) => {
    post.data.tags?.forEach((tag: string) => {
      const tagSlug = IdToSlug(tag);
      if (!tags.has(tagSlug)) {
        tags.set(tagSlug, {
          name: tag,
          slug: `/tags/${tagSlug}`,
          posts: [],
        });
      }
      tags.get(tagSlug)!.posts.push({
        title: post.data.title,
        id: `/posts/${IdToSlug(post.id)}`,
        date: new Date(post.data.published),
        tags: post.data.tags,
      });
    });
  });

  return tags;
}

/**
 * 修改：获取所有一级分类的方法
 * 原来的 GetCategories 方法，现在专门处理 first_level_category 字段
 * 返回一个Map，键为一级分类的slug，值为包含该分类信息和文章列表的对象
 * 用途：生成一级分类列表页 (/categories/index.astro) 和特定一级分类页面
 */
export async function getFirstCategories() {
  const allBlogPosts = await getCollection("posts", ({ data }) => {
    return import.meta.env.PROD ? data.draft !== true : true;
  });

  const categories = new Map<string, fisrtCategory>();

  allBlogPosts.forEach((post) => {
    if (!post.data.first_level_category) return;

    const categorySlug = IdToSlug(post.data.first_level_category);

    if (!categories.has(categorySlug)) {
      categories.set(categorySlug, {
        name: post.data.first_level_category,
        slug: `/categories/${categorySlug}`,
        posts: [],
      });
    }
    // 对象下的 posts 数组内部的值
    categories.get(categorySlug)!.posts.push({
      title: post.data.title,
      id: `/posts/${IdToSlug(post.id)}`,
      date: new Date(post.data.published),
      tags: post.data.tags,
    });
  });

  return categories;
}


/**
 * 修改：新增获取二级分类的方法
 * 处理每篇文章的 first_level_category 和 second_level_category 字段
 * 构建完整的二级分类路径：/categories/一级分类/二级分类
 * 返回的文章数据为完整的 postCard 格式，支持卡片式展示
 *
 * @returns 一个Map，键为完整的二级分类路径，值为包含该分类信息和文章列表的对象
 * 用途：生成二级分类页面 (/categories/[first_category]/[second_category].astro)
 */
export async function getSecondCategories() {
  const allBlogPosts = await getCollection("posts", ({ data }) => {
    return import.meta.env.PROD ? data.draft !== true : true;
  });

  const categories = new Map<string, secondCategory>();

  allBlogPosts.forEach((post) => {
    if (!post.data.second_level_category || !post.data.first_level_category) return;

    const categorySlug = `/categories/${IdToSlug(post.data.first_level_category)}/${IdToSlug(post.data.second_level_category)}`;
    // 构建对象
    if (!categories.has(categorySlug)) {
      categories.set(categorySlug, {
        name: post.data.second_level_category,
        slug: categorySlug,
        posts: [],
      });
    }
    // 对象下的 posts 数组内部的值
    categories.get(categorySlug)!.posts.push({
      title: post.data.title,
      id: post.id, // 【修复】传递原始文档ID，让PostCard组件自己处理URL生成
      published: new Date(post.data.published),
      tags: post.data.tags,
      readingMetadata:post.data.readingMetadata,
      description:post.data.description,
      image:post.data.cover,
      // 【新增】传递分类信息给PostCard组件显示
      first_level_category: post.data.first_level_category,
      second_level_category: post.data.second_level_category,
    });
  });

  // 【新增】对每个分类下的文章按发布日期降序排序（最新的在前）
  categories.forEach((category) => {
    category.posts.sort((a, b) => {
      const dateA = new Date(a.published);
      const dateB = new Date(b.published);
      return dateA > dateB ? -1 : 1; // 降序排序，最新的在前
    });
  });

  return categories;
}
// export interface postCard{
//   id: string;
//   title: string;
//   published: Date;
//   category?:string;
//   tags?: string[];
//   description?: string;
//   image?: string;
//   readingMetadata: { time: number; wordCount: number };
// }
