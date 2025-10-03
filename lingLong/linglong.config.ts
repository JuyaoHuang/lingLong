import I18nKeys from "./src/locales/keys";
import type { Configuration } from "./src/types/config";

const LingLongConfig: Configuration = {
  title: "",
  subTitle: "",
  brandTitle: "Alen's website",

  description: "",

  site: "https://linglong-blog.top",// 网站 URL

  locale: "en", // set for website language and date format
  // 页面 URL 配置
  navigators: [
    {
      nameKey: I18nKeys.nav_bar_home,
      href: "/",
    },
    {
      nameKey: I18nKeys.nav_bar_archive,
      href: "/archive",
    },
    {
      nameKey: I18nKeys.nav_bar_about,
      href: "/about",
    },
    {
      nameKey: I18nKeys.nav_bar_github,
      href: "https://github.com/JuyaoHuang",
    },
    {
      nameKey: I18nKeys.nav_bar_friends,
      href: "/friends",
    },
  ],
  username: "わかば むつみ",
  sign: "とある科学のみさか みこと",
  avatarUrl:"/muzimi.png",
  socialLinks: [
    {
      icon: "line-md:github-loop",
      link: "https://github.com/JuyaoHuang",
    },
    {
      icon: "mingcute:bilibili-line",
      link: "https://space.bilibili.com/506080737",
    },
    // {
    //   icon: "mingcute:netease-music-line",
    //   link: "https://music.163.com/#/user/home?id=125291648",
    // },
  ],
  // 具体查看：lingLong\src\components\SideBar.astro: .slice(0, LingLongConfig.maxSidebarCategoryChip + 1)
  // It is recommended to set it to a common multiple of 2 and 3
  maxSidebarCategoryChip: 6, 
  maxSidebarTagChip: 9,
  maxFooterCategoryChip: 6,
  maxFooterTagChip: 24,

  banners: [
    "/images/1.png",
    "/images/2.jpg",
    "/images/3.png",
    "/images/4.png",
    "/images/5.jpg",
    "/images/6.jpg",
    "/images/7.png",
    "/images/8.png",
    "/images/9.png",
    "/images/10.jpg",
    "/images/11.jpg",
    "/images/12.png",
  ],
  
  slugMode: "RAW", // 'RAW' | 'HASH' - 切换到RAW模式，URL直接使用分类名

  license: {
    name: "CC BY-NC-SA 4.0",
    url: "https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode.en",
  },

  // WIP functions
  bannerStyle: "loop", // 'loop' | 'static' | 'hidden'
};

export default LingLongConfig;
