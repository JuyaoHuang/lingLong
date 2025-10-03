---
title: cssStyleSummary
published: 2025-09-26
description: CSS常见样式
tags: [CSS]
first_level_category: 'blog理解文档'
second_level_category: 'blog'
author: Alen
draft: false
---
# CSS 常见样式总结
## 将图片作背景

### 以Banner.astro为例

#### 前情提要

我不满意该轮播图片在页面下滑时消失，想让其铺满我网页的整个背景，再调整文字卡片等的透明程度，得到我想要的页面效果。

---

当然对一个纯技术博客来说有点浪费时间

---

#### 操作步骤

1. 查询 Banner 的CSS样式：

   1. 打开 Banner.astro

   2. 查看文件，得到渲染的 h5 页面 `class=banner`

   3. 查询 CSS 中 `.banner` 关键字

   4. 定位到

      ```css
      .banner {
      @apply relative h-[calc(var(--banner-height)*3/4)] opacity-100 lg:h-[var(--banner-height)];
      } 
      ```

2. **修改为沉底样式**

   ```css
   .banner {
   /*
   fixed:   将元素相对于浏览器窗口进行定位，并脱离文档流。
   top-0:   固定在顶部。
   left-0:  固定在左侧。
   -z-10:   将这个元素的堆叠顺序（层级）设置为负数，把它压到其他所有内容的下面。
   */
   @apply fixed top-0 left-0 -z-10 h-[calc(var(--banner-height)*3/4)] w-full opacity-100 lg:h-[var(--banner-height)];
   }
   ```

   1. **relative -> fixed**: 这是最关键的一步。relative 只是相对定位，元素依然占据着文档空间，会把下面的文章推开。fixed 则让它完全脱离文档流，像一张海报一样贴在浏览器窗口的背景上，不再影响任何其他组件的位置。
   2. 添加 top-0 left-0: 确保这张“海报”从窗口的左上角开始贴
   3. `z-index` 控制元素的堆叠顺序。一个负值可以确保它被渲染在默认层级（z-index: 0）的所有内容的后面。
   4. 添加 `w-full`: 确保 Banner 始终是满宽的

3. 对页面主容器 `main-container` 进行 CSS样式 修改

   1. 定位到 `MainLayout.astro` 文件，查看 html 部分

   2. 观察到 

      ```html
      <div class="main-container my-10">
      ```

   3. 将 `class` 修改为

      ```html
      class="mt-[calc(var(--banner-height)*3/4)] lg:mt-[var(--banner-height)]"
      ```

      - `mt-[calc(var(--banner-height)\*3/4)]`: 给 <main> 标签添加了一个 margin-top。在移动端，这个边距的高度是 var(--banner-height) 的 3/4。
      - `lg:mt-[var(--banner-height)]`: 在桌面端 (lg及以上)，这个边距的高度是完整的 var(--banner-height)。

​	这个 margin-top 的值**完全复制**了 Banner 组件里 height 的值。这样就完美地确保了文章内容 main 的顶部，正好衔接在作为背景的 Banner 的底部，无论在哪个屏幕尺寸下都能精确对齐。

​	完成这两步修改后，Banner 和 Waves 作为固定背景，文章内容则可以顺畅地从它上面滚动过去。
