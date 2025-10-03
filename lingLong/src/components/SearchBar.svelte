<script lang="ts">
  import { onMount } from "svelte";
  import { OverlayScrollbars } from "overlayscrollbars";
  import Icon from "@iconify/svelte";

  import I18nKeys from "../locales/keys";
  import { i18n } from "../locales/translation";

// 站内实时搜索框组件。当用户在搜索框中输入文字时，
// 它会即时地、无需刷新页面地从一个名为 Pagefind 的搜索引擎获取结果，并以一个平滑、动态的下拉面板展示出来。


  let searchKeyword = "";
  let searchResult: any[] = [];

  let resultPannel: HTMLDivElement;
  let searchBar: HTMLDivElement;

  let search = (keyword: string) => {};

  onMount(async () => {
    // setup overlay scrollbars
    OverlayScrollbars(resultPannel, {
      scrollbars: {
        theme: "scrollbar-base scrollbar-auto py-1",
        autoHide: "move",
      },
    });

    /**
     * Asynchronously performs a search based on the provided keyword.
     * If in development mode, extracts a subset of mock results for demonstration.
     * Otherwise, fetches results from the Pagefind search engine and populates the array.
     * Toggles the visibility and height of the results panel based on the outcome.
     * 根据提供的关键字异步执行搜索。
     * 如果处于开发模式，则提取模拟结果的子集进行演示。
     * 否则，从 Pagefind 搜索引擎获取结果并填充数组。
     * 根据结果切换结果面板的可见性和高度。
     */
    search = async (keyword: string) => {
      let searchResultArr = [];

      // @ts-ignore
      const ret = await pagefind.search(keyword);
      for (const item of ret.results) {
        searchResultArr.push(await item.data());
      }
      searchResult = searchResultArr;

      const searchResultVisable = keyword != "" && searchResult.length != 0;

      if (searchResultVisable) {
        resultPannel.style.height = `${searchResultArr.length * 84 + 16}px`;
        resultPannel.style.opacity = "100%";
      } else {
        resultPannel.style.height = "0px";
        resultPannel.style.opacity = "0";
      }
    };

    // handle click outside to closed result pannel
    document.addEventListener("click", (event) => {
      if (
        !resultPannel.contains(event.target as any) &&
        !searchBar.contains(event.target as any)
      ) {
        search("");
      }
    });
  });
//  Svelte 的响应式语句，是实现“实时”搜索的魔法所在。
// $: 这个符号告诉 Svelte：“请监视 searchKeyword 这个变量，
// 一旦它的值发生任何改变（即用户打字或删字），就立刻自动执行 search() 这个函数。”
  $: search(searchKeyword);
</script>

<!-- search bar -->
<div bind:this={searchBar} class="search-bar hidden lg:block">
  <div class="bg-black/5 dark:bg-white/5 h-10 rounded-lg flex flex-row">
    <label
      for="search-bar-input"
      class="w-10 h-10 flex flex-row justify-center items-center pl-2 pr-1 hover:cursor-text text-gray-400"
    >
      <Icon icon="mingcute:search-line" width={24} height={24} />
    </label>
    <input
      id="search-bar-input"
      class="w-36 text-[var(--text-color)] xl:focus:w-60 bg-transparent outline-none transition-all"
      placeholder={i18n(I18nKeys.nav_bar_search_placeholder)}
      type="text"
      autocomplete="off"
      on:focus={() => {
        search(searchKeyword);
      }}
      bind:value={searchKeyword}
    />
  </div>
</div>
<!-- result pannel -->
<div
  id="result-pannel"
  bind:this={resultPannel}
  class="max-h-[436px] overflow-y-scroll opacity-0 !absolute h-0 -right-3 w-[28rem] bg-[var(--card-color)] rounded-2xl top-20 transition-all"
>
  <div
    class="flex flex-col h-full onload-animation before:content-[''] before:pt-2 after:content-[''] after:pb-2"
  >
    {#each searchResult as item}
      <a
        href={item.url}
        class="mx-2 py-2 px-3 rounded-xl result-item transition-all"
      >
        <div class="flex flex-row space-x-1 items-center">
          <p
            class="line-clamp-1 text-lg font-semibold text-[var(--text-color)] result-title"
          >
            {item.meta.title}
          </p>
          <span class="text-[var(--primary-color)] font-extrabold">
            <Icon icon="cuida:caret-right-outline" width={16} height={16} />
          </span>
        </div>
        <div>
          <div class="h-10">
            <p
              class="item-excerpt text-sm line-clamp-2 text-[var(--text-color-lighten)]"
            >
              {@html item.excerpt}
            </p>
          </div>
        </div>
      </a>
    {/each}
  </div>
</div>
