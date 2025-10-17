import I18nKeys from "./src/locales/keys";
import type { Configuration } from "./src/types/config";

const LingLongConfig: Configuration = {
  title: "",
  subTitle: "",
  brandTitle: "Atri site",

  description: "",

  site: "https://juayohuang.top",// 网站 URL

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
  sign: "私の唯一の命は私にかかっている",///我这仅此一次的人生只取决我
  avatarUrl:"/Atri.png",
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
    // "/images/2.png",
    "/images/3.png",
    "/images/4.png",
    "/images/5.jpg",
    "/images/6.jpg",
    // "/images/7.png",
    "/images/8.jpg",
    "/images/9.png",
    "/images/10.jpg",
    "/images/11.png",
    "/images/13.png",
    "/images/14.png",
    "/images/15.png",
    "/images/16.jpg",
    "/images/17.jpg",
    "/images/18.png",
    // 卡提西亚
    // "/images/kati/20.jpg",
    // "/images/kati/21.jpg",
    // "/images/kati/22.jpg",
    // "/images/kati/23.jpg",
    // "/images/kati/24.jpg",
    // "/images/kati/25.jpg",
    // "/images/kati/26.jpg",
    // "/images/kati/27.jpg",
    // "/images/kati/28.jpg",
    // "/images/kati/29.jpg",
    // "/images/kati/30.jpg",
    // "/images/kati/31.jpg",
    // 卡提end
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
