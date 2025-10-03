<!--
  带实时预览功能的 Monaco Markdown 编辑器
  功能：vs-dark 主题、全屏模式、响应式布局、自定义事件
  Monaco Markdown Editor with Live Preview
  Features: vs-dark theme, fullscreen mode, responsive layout, custom events
-->
<script>
  import { onMount, onDestroy } from 'svelte';

  export let value = '';
  export let onContentChange = (content) => {};
  export let height = '600px';
  export let placeholder = 'Start writing your markdown content...';

  let editorContainer;
  let editor;
  let isFullscreen = false;
  let isLoading = true;
  let loadingError = '';
  let loadingProgress = 'Initializing Monaco Editor...';
  let editorCreated = false; // Prevent multiple creation

  // 响应断点
  let windowWidth = 0;
  $: isMobile = windowWidth < 1024;

  onMount(() => {
    console.log('Editor component mounted');
    console.log('editorContainer:', editorContainer);
    console.log('window defined:', typeof window !== 'undefined');

    if (typeof window !== 'undefined') {
      loadingProgress = 'Loading Monaco Editor from CDN...';

      // Add more detailed container checking--添加更详细的容器检查
      const checkContainer = () => {
        console.log('Checking container...');
        console.log('editorContainer now:', editorContainer);

        if (editorContainer) {
          console.log('Container found! Loading Monaco...');

          if (editorCreated) {
            console.log('Editor already created, skipping...');
            return;
          }

          editorCreated = true; // 标记为进行中--Mark as in progress

          // 首先仅加载 Monaco 编辑器，暂时跳过标记--Load only Monaco Editor first, skip marked for now
          loadMonacoFromCDN()
            .then(monaco => {
              console.log('Monaco loaded successfully');
              loadingProgress = 'Initializing editor...';

              try {
                // Create Monaco Editor
                editor = monaco.editor.create(editorContainer, {
                  value: value,
                  language: 'markdown',
                  theme: 'vs-dark',
                  automaticLayout: true,
                  wordWrap: 'on',
                  fontSize: 14,
                  lineHeight: 20,
                  minimap: { enabled: !isMobile },
                  scrollBeyondLastLine: false,
                  folding: true,
                  lineNumbers: 'on',
                  renderWhitespace: 'boundary',
                  bracketPairColorization: { enabled: true }
                });

                console.log('Monaco editor created successfully');

                // 设置内容更改监听器 Set up content change listener
                editor.onDidChangeModelContent(() => {
                  const newValue = editor.getValue();
                  value = newValue;
                  onContentChange(newValue);
                });
                const handleResize = () => {
                  isMobile = window.innerWidth < 1024;
                  if (editor) {
                    editor.updateOptions({ minimap: { enabled: !isMobile } });
                    editor.layout();
                  }
                };

                window.addEventListener('resize', handleResize);
                isLoading = false;

                // Dispatch ready event
                const editorReadyEvent = new CustomEvent('editor-ready', {
                  detail: {
                    getValue: () => editor.getValue(),
                    setValue: (newValue) => {
                      if (editor && newValue !== editor.getValue()) {
                        editor.setValue(newValue);
                      }
                    },
                    focus: () => editor.focus(),
                    dispose: () => editor.dispose(),
                    getEditor: () => editor
                  }
                });
                document.dispatchEvent(editorReadyEvent);

              } catch (error) {
                console.error('Failed to create Monaco Editor:', error);
                loadingError = 'Failed to create Monaco Editor: ' + error.message;
                isLoading = false;
                editorCreated = false; // Reset on error
              }
            })
            .catch(error => {
              console.error('Failed to load Monaco Editor:', error);
              loadingError = 'Failed to load Monaco Editor from CDN: ' + error.message;
              isLoading = false;
              editorCreated = false; // Reset on error
            });
        } else {
          console.log('Container still not found, retrying...');
          loadingError = 'Editor container not found. Please refresh the page.';
          isLoading = false;
        }
      };

      // Try multiple times with increasing delays
      setTimeout(checkContainer, 100);
      setTimeout(checkContainer, 500);
      setTimeout(checkContainer, 1000);
    }
  });

  // Load Monaco Editor from CDN
  function loadMonacoFromCDN() {
    return new Promise((resolve, reject) => {
      if (window.monaco) {
        resolve(window.monaco);
        return;
      }

      // Load Monaco Editor CSS
      const cssLink = document.createElement('link');
      cssLink.rel = 'stylesheet';
      cssLink.href = 'https://cdn.jsdelivr.net/npm/monaco-editor@0.45.0/min/vs/editor/editor.main.css';
      document.head.appendChild(cssLink);

      // Load Monaco Editor JS
      const script = document.createElement('script');
      script.src = 'https://cdn.jsdelivr.net/npm/monaco-editor@0.45.0/min/vs/loader.js';
      script.onload = () => {
        window.require.config({
          paths: {
            vs: 'https://cdn.jsdelivr.net/npm/monaco-editor@0.45.0/min/vs'
          }
        });
        window.require(['vs/editor/editor.main'], () => {
          resolve(window.monaco);
        });
      };
      script.onerror = () => reject(new Error('Failed to load Monaco Editor script'));
      document.head.appendChild(script);
    });
  }

  onDestroy(() => {
    if (editor) {
      editor.dispose();
    }
  });

  // External methods for backward compatibility
  export function setValue(newValue) {
    if (editor && newValue !== editor.getValue()) {
      editor.setValue(newValue);
    }
  }

  export function getValue() {
    return editor ? editor.getValue() : '';
  }

  // Toggle fullscreen mode
  function toggleFullscreen() {
    isFullscreen = !isFullscreen;
    setTimeout(() => {
      if (editor) {
        editor.layout();
      }
    }, 100);
  }

  // Handle escape key for fullscreen exit
  function handleKeydown(event) {
    if (event.key === 'Escape' && isFullscreen) {
      isFullscreen = false;
      setTimeout(() => {
        if (editor) {
          editor.layout();
        }
      }, 100);
    }
  }
</script>

<svelte:window bind:innerWidth={windowWidth} on:keydown={handleKeydown} />

<div
  class="editor-wrapper"
  class:fullscreen={isFullscreen}
  style="height: {isFullscreen ? '100vh' : height}"
>
  <!-- Toolbar -->
  <div class="toolbar">
    <div class="toolbar-left">
      <span class="toolbar-title">Markdown Editor</span>
      {#if isMobile}
        <span class="mobile-indicator">Mobile Mode</span>
      {/if}
    </div>

    <div class="toolbar-right">
      <button
        class="toolbar-btn"
        on:click={toggleFullscreen}
        title="Toggle Fullscreen"
      >
        {isFullscreen ? 'Exit Fullscreen' : 'Fullscreen'}
      </button>
    </div>
  </div>

  <!-- Editor Content Area -->
  <div class="editor-content">
    <!-- Editor container (full width) -->
    <div class="editor-panel">
      <div bind:this={editorContainer} class="editor-container"></div>
    </div>

    <!-- Loading Overlay -->
    {#if isLoading}
      <div class="loading-overlay">
        <div class="loading-spinner"></div>
        <p>{loadingProgress}</p>
        <div class="loading-tips">
          <small>Monaco Editor is large (~2MB). First load may take a moment...</small>
        </div>
      </div>
    {/if}

    <!-- Error Overlay -->
    {#if loadingError}
      <div class="error-overlay">
        <div class="error-icon">⚠️</div>
        <p class="error-message">{loadingError}</p>
        <button class="retry-btn" on:click={() => window.location.reload()}>
          Reload Page
        </button>
      </div>
    {/if}
  </div>
</div>

<style>
  .editor-wrapper {
    display: flex;
    flex-direction: column;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    overflow: hidden;
    background: #1e1e1e;
    position: relative;
  }

  .editor-wrapper.fullscreen {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: 9999;
    border-radius: 0;
  }

  .toolbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem 1rem;
    background: #2d2d2d;
    border-bottom: 1px solid #404040;
    color: #ffffff;
  }

  .toolbar-left {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .toolbar-title {
    font-size: 0.875rem;
    font-weight: 500;
  }

  .mobile-indicator {
    font-size: 0.75rem;
    color: #fbbf24;
    background: #451a03;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
  }

  .toolbar-right {
    display: flex;
    gap: 0.5rem;
  }

  .toolbar-btn {
    background: #404040;
    border: none;
    color: #ffffff;
    padding: 0.5rem;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
    transition: background-color 0.2s;
  }

  .toolbar-btn:hover {
    background: #525252;
  }

  .editor-content {
    flex: 1;
    display: flex;
    overflow: hidden;
    position: relative;
  }

  .editor-panel {
    display: flex;
    flex-direction: column;
    width: 100%;
  }

  .editor-container {
    flex: 1;
    min-height: 0;
  }

  .loading-overlay,
  .error-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: rgba(30, 30, 30, 0.95);
    color: #94a3b8;
    padding: 2rem;
    text-align: center;
    z-index: 10;
  }

  .error-overlay {
    background: rgba(30, 30, 30, 0.98);
  }

  .loading-spinner {
    width: 2rem;
    height: 2rem;
    border: 2px solid #404040;
    border-top: 2px solid #3b82f6;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 1rem;
  }

  .loading-tips {
    margin-top: 1rem;
    opacity: 0.7;
  }

  .loading-tips small {
    font-size: 0.875rem;
    color: #9ca3af;
  }

  .error-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
  }

  .error-message {
    color: #ef4444;
    margin-bottom: 1.5rem;
    font-size: 0.875rem;
  }

  .retry-btn {
    background: #3b82f6;
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.875rem;
    transition: background-color 0.2s;
  }

  .retry-btn:hover {
    background: #2563eb;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  .editor-panel {
    display: flex;
    flex-direction: column;
    width: 100%;
  }

  .editor-container {
    flex: 1;
    min-height: 0;
  }

  /* Mobile responsiveness */
  @media (max-width: 1024px) {
    .toolbar-title {
      font-size: 0.75rem;
    }
  }

  @media (max-width: 640px) {
    .toolbar {
      padding: 0.5rem;
    }
  }
</style>