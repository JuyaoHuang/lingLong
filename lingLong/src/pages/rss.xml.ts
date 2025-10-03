import rss from "@astrojs/rss";
import { getCollection } from "astro:content";
import LingLongConfig from "../../linglong.config";
import { IdToSlug } from "../utils/hash";

export async function GET(context: { site: string }) {
  // 过滤掉草稿文章
  const posts = await getCollection("posts", ({ data }) => {
    return import.meta.env.PROD ? data.draft !== true : true;
  });

  return rss({
    title: LingLongConfig.brandTitle || LingLongConfig.title,
    description: LingLongConfig.description || "Blog RSS Feed",
    site: context.site,
    items: posts.map((post) => ({
      title: post.data.title,
      description: post.data.description,
      pubDate: post.data.published,
      link: `/posts/${IdToSlug(post.id)}`,
    })),
  });
}
