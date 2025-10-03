<script lang="ts">
  /**
   ******************************************************************************
   ******************************************************************************
   Deprecated                 Deprecated                                Deprecated
   ******************************************************************************
            弃用                        弃用                              弃用
  */
  import { onMount, onDestroy} from 'svelte';

  // 接收Astro内置的headings数组，包含depth、text、slug
  export let headings: Array<{
    depth: number;
    text: string;
    slug: string;
  }> = [];

  let isVisible = false;
  let activeId = '';
  let observer: IntersectionObserver;

  onMount(() => {
    // 只有当存在标题时才显示TOC
    if (!headings || headings.length === 0) {
      return;
    }

    isVisible = true;

    // 使用现代的Intersection Observer API监听标题
    // 当标题进入视口顶部时高亮对应的TOC项
    observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting && entry.boundingClientRect.top <= 100) {
            activeId = entry.target.id;
          }
        });
      },
      {
        // 触发阈值：标题顶部距离视口顶部100px时触发
        rootMargin: '-100px 0px -80% 0px',
        threshold: 0
      }
    );

    // 观察所有标题元素
    headings.forEach(({ slug }) => {
      const element = document.getElementById(slug);
      if (element) {
        observer.observe(element);
      }
    });

    return () => {
      // 清理观察器
      if (observer) {
        observer.disconnect();
      }
    };
  });

  // 平滑跳转到指定标题
  const scrollToHeading = (slug: string) => {
    const element = document.getElementById(slug);
    if (element) {
      element.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  };
</script>

{#if isVisible && headings.length > 0}
  <nav
    class="floating-toc"
    role="navigation"
    aria-label="文章目录"
  >
    <div class="toc-header">
      <h3>目录</h3>
    </div>

    <div class="toc-content">
      <ul class="toc-list">
        {#each headings as heading}
          <li
            class="toc-item"
            class:active={activeId === heading.slug}
            style="margin-left: {(heading.depth - 1) * 12}px"
          >
            <button
              class="toc-link"
              class:active={activeId === heading.slug}
              on:click={() => scrollToHeading(heading.slug)}
              title={heading.text}
            >
              {heading.text}
            </button>
          </li>
        {/each}
      </ul>
    </div>
  </nav>
{/if}

<style>
  /* 浮动TOC的主容器 - 确保真正的固定浮动 */
  .floating-toc {
    position: fixed !important;  /* 强制固定定位 */
    top: 20%;
    left: 0.5rem;
    width: 280px;
    max-height: 60vh;
    /* background: rgba(215,222,206,0.6);
     */
    background: #ddede3;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(0, 0, 0, 0.1);
    border-radius: 12px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    z-index: 9999 !important;    /* 提高层级，确保在最上层 */
    overflow: hidden;
    transition: all 0.3s ease;
    /* 确保不受父容器影响 */
    transform: translateZ(0);
    will-change: transform;
  }

  /* 深色模式支持 */
  @media (prefers-color-scheme: dark) {
    .floating-toc {
      background: rgba(30, 30, 30, 0.95);
      border: 1px solid rgba(255, 255, 255, 0.1);
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
  }

  /* TOC标题部分 */
  .toc-header {
    padding: 1rem 1.25rem 0.75rem;
    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
    background: rgba(0, 0, 0, 0.02);
  }

  @media (prefers-color-scheme: dark) {
    .toc-header {
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      background: rgba(255, 255, 255, 0.02);
    }
  }

  .toc-header h3 {
    margin: 0;
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text-color, #333);
    text-align: center;
  }

  /* TOC内容区域 */
  .toc-content {
    padding: 0.5rem 0;
    max-height: calc(60vh - 60px);
    overflow-y: auto;
  }

  /* 自定义滚动条样式 */
  .toc-content::-webkit-scrollbar {
    width: 4px;
  }

  .toc-content::-webkit-scrollbar-track {
    background: transparent;
  }

  .toc-content::-webkit-scrollbar-thumb {
    background: rgba(0, 0, 0, 0.2);
    border-radius: 2px;
  }

  /* TOC列表样式 */
  .toc-list {
    list-style: none;
    margin: 0;
    padding: 0;
  }

  .toc-item {
    margin: 0;
    padding: 0;
  }

  /* TOC链接按钮样式 */
  .toc-link {
    display: block;
    width: 100%;
    padding: 0.5rem 1.25rem;
    background: none;
    border: none;
    text-align: left;
    font-size: 0.85rem;
    line-height: 1.4;
    color: var(--text-color, #666);
    cursor: pointer;
    transition: all 0.2s ease;
    border-left: 3px solid transparent;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  /* 悬停效果 */
  .toc-link:hover {
    background: rgba(0, 0, 0, 0.05);
    color: var(--primary-color, #0066cc);
  }

  @media (prefers-color-scheme: dark) {
    .toc-link:hover {
      background: rgba(255, 255, 255, 0.05);
      color: var(--primary-color, #66aaff);
    }
  }

  /* 激活状态样式 */
  .toc-link.active {
    background: rgba(0, 102, 204, 0.1);
    color: var(--primary-color, #0066cc);
    border-left-color: var(--primary-color, #0066cc);
    font-weight: 500;
  }

  @media (prefers-color-scheme: dark) {
    .toc-link.active {
      background: rgba(102, 170, 255, 0.1);
      color: var(--primary-color, #66aaff);
      border-left-color: var(--primary-color, #66aaff);
    }
  }

  /* 响应式设计：中等屏幕隐藏 */
  @media (max-width: 1200px) {
    .floating-toc {
      display: none;
    }
  }

  /* 小屏幕设备隐藏 */
  @media (max-width: 768px) {
    .floating-toc {
      display: none;
    }
  }
</style>