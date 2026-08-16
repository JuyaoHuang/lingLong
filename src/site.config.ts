import type { CardListData, Config, IntegrationUserConfig, ThemeUserConfig } from 'astro-pure/types'

export const theme: ThemeUserConfig = {
  // [Basic]
  /** Title for your website. Will be used in metadata and as browser tab title. */
  title: 'Atri Website',
  /** Will be used in index page & copyright declaration */
  author: 'Juyao Huang',
  /** Description metadata for your website. Can be used in page metadata. */
  description: '事以密成，语以泄败，是故话不可多言，福不可多晒。',
  /** The default favicon for your site which should be a path to an image in the `public/` directory. */
  favicon: '/favicon/favicon.svg',
  /** The default social card image for your site which should be a path to an image in the `public/` directory. */
  socialCard: '/images/social-card.png',
  /** Specify the default language for this site. */
  locale: {
    lang: 'en-US',
    attrs: 'en_US',
    // Date locale
    dateLocale: 'en-US',
    dateOptions: {
      day: 'numeric',
      month: 'short',
      year: 'numeric'
    }
  },
  /** Set a logo image to show in the homepage. */
  logo: {
    src: '/src/assets/avatar.jpg',
    alt: 'Avatar'
  },

  titleDelimiter: '•',
  prerender: true, // pagefind search is not supported with prerendering disabled
  npmCDN: 'https://cdn.jsdelivr.net/npm',

  // Still in test
  head: [
    /* Telegram channel */
    // {
    //   tag: 'meta',
    //   attrs: { name: 'telegram:channel', content: '@cworld0_cn' },
    //   content: ''
    // }
  ],
  customCss: [],

  /** Homepage background mode: 'gradient' for solid color gradient, 'image' for background image 
      homepageBackground: 'image' as 'gradient' | 'image'
      切换 'image' ↔ 'gradient' 即可。背景图片清晰度可在 src/pages/index.astro 的 .homepage-bg CSS 中调整 mask-image 的
      rgba alpha 值（当前 0.4，增大则更清晰，减小则更淡）
  */
  homepageBackground: 'image',

  /** Configure the header of your site. */
  header: {
    menu: [
      { title: 'Blog', link: '/blog' },
      // { title: 'Docs', link: '/docs' },
      { title: 'Projects', link: '/projects' },
      { title: 'Links', link: '/links' },
      { title: 'About', link: '/about' },
      { title: 'Todo', link: '/todo' }
    ]
  },

  /** Configure the footer of your site. */
  footer: {
    // Year format
    year: `© ${new Date().getFullYear()}`,
    // year: `© 2019 - ${new Date().getFullYear()}`,
    links: [
      // Registration link
      {
        title: '萌ICP备20266001号',
        link: 'https://icp.gov.moe/?keyword=20266001',
        style: 'text-sm' // Uno/TW CSS class
      },
      // Privacy Policy link
      // {
      //   title: 'Site Policy',
      //   link: '/terms',
      //   pos: 2 // position set to 2 will be appended to copyright line
      // github: 'https://github.com/JuyaoHuang/lingLong'}
    ],
    /** Enable displaying a “Astro & Pure theme powered” link in your site’s footer. */
    credits: false,
    /** Optional details about the social media accounts for this site. */
    social: {}
  },

  // [Content]
  content: {
    /** External links configuration */
    externalLinks: {
      content: ' ↗',
      /** Properties for the external links element */
      properties: {
        style: 'user-select:none'
      }
    },
    /** Blog page size for pagination (optional) */
    blogPageSize: 8,
    // Currently support weibo, x, bluesky
    // share: ['weibo', 'x', 'bluesky']
  }
}

export const integ: IntegrationUserConfig = {
  // [Links]
  // https://astro-pure.js.org/docs/integrations/links
  links: {
    // Friend logbook
    // 友链日志 - 显示在友链页面的动态
    logbook: [
      { date: '2026-01-15', content: '我们可以成为朋友么🤗' },
    ],
    // Yourself link info
    // 你的站点信息 - 供他人添加友链时参考
    applyTip: [
      { name: 'Name', val: theme.title },
      { name: 'Desc', val: theme.description || 'Null' },
      { name: 'Link', val: 'https://www.juyaohuang.com' },
      { name: 'Avatar', val: 'https://www.juyaohuang.com' }
    ],
    // Cache avatars in `public/avatars/` to improve user experience.
    // 是否缓存友链头像到本地
    cacheAvatar: false
  },
  // [Search]
  pagefind: true,
  // Add a random quote to the footer (default on homepage footer)
  // See: https://astro-pure.js.org/docs/integrations/advanced#web-content-render
  // [Quote]
  quote: {
    // - Hitokoto
    // https://developer.hitokoto.cn/sentence/#%E8%AF%B7%E6%B1%82%E5%9C%B0%E5%9D%80
    server: 'https://v1.hitokoto.cn/?c=i&c=d',
    target: `(data) => (data.hitokoto || 'Error')`
    // - Quoteable
    // https://github.com/lukePeavey/quotable
    // server: 'http://api.quotable.io/quotes/random?maxLength=60',
    // target: `(data) => data[0].content || 'Error'`
    // - DummyJSON
    // server: 'https://dummyjson.com/quotes/random',
    // target: `(data) => (data.quote.length > 80 ? \`\${data.quote.slice(0, 80)}...\` : data.quote || 'Error')`
  },
  // [Typography]
  // https://unocss.dev/presets/typography
  // 配置文章内容的排版样式
  // 修改 blockquoteStyle 改变引用块字体样式
  // 修改 inlineCodeBlockStyle 改变行内代码显示风格
  typography: {
    class: 'prose text-base', // UnoCSS 类名
    // The style of blockquote font `normal` / `italic` (default to italic in typography)
    // 引用块样式: '正常' / '斜体'
    blockquoteStyle: 'italic',
    // The style of inline code block `code` / `modern` (default to code in typography)
    // 行内代码样式: 'code' / 'modern'
    inlineCodeBlockStyle: 'modern'
  },
  // [Lightbox]
  // A lightbox library that can add zoom effect
  // https://astro-pure.js.org/docs/integrations/others#medium-zoom
  // 为图片添加点击放大效果
  // 设置 enable: false 禁用图片放大功能
  // 修改 selector 改变哪些图片可以放大
  mediumZoom: {
    enable: true, // disable it will not load the whole library
    selector: '.prose .zoomable',
    options: {
      className: 'zoomable'
    }
  },
  // Comment system
  // 为文章添加评论功能
  // 使用方法:
  // 1. 部署自己的 Waline 服务器（参考 Waline 官方文档）
  // 2. 修改 server 为你的服务器地址
  // 3. 根据需要调整 additionalConfigs 配置
  // https://github.com/JuyaoHuang/lingLong/blob/main/public/favicon/android-chrome-512x512.png
  waline: {
    enable: true, // 启用/禁用
    // Server service link
    // Waline 服务器地址
    server: 'https://waline.juyaohuang.com/',
    // Show meta info for comments
    // 是否显示评论元信息
    showMeta: false,
    // Refer https://waline.js.org/en/guide/features/emoji.html
    // 表情包
    emoji: ['bmoji', 'weibo','tw-emoji'],
    // Refer https://waline.js.org/en/reference/client/props.html
    additionalConfigs: {
      // search: false,
      pageview: true, // 页面浏览量统计
      comment: true, // 评论功能
      locale: {
        reaction0: 'Like',
        placeholder: 'Welcome to comment. (Email to receive replies. Login is unnecessary)'
      },
      imageUploader: false // 图片上传功能
    }
  }
}

export const terms: CardListData = {
  title: 'Terms content',
  list: [
    {
      title: 'Privacy Policy',
      link: '/terms/privacy-policy'
    },
    {
      title: 'Terms and Conditions',
      link: '/terms/terms-and-conditions'
    },
    {
      title: 'Copyright',
      link: '/terms/copyright'
    },
    {
      title: 'Disclaimer',
      link: '/terms/disclaimer'
    }
  ]
}

const config = { ...theme, integ } as Config
export default config
