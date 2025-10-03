<!--
  帖子管理表组件
  功能：CRUD 操作、类别过滤、响应式设计
  Posts Management Table Component
  Features: CRUD operations, category filtering, responsive design
-->
<script>
  import { onMount } from 'svelte';
  import { postService } from '../../services/postService';

  let posts = [];
  let loading = true;
  let error = '';
  let searchTerm = '';
  let selectedCategory = '';
  let showDeleteModal = false;
  let postToDelete = null;

  $: filteredPosts = posts.filter(post => {
    const matchesSearch = !searchTerm ||
      post.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      post.tags?.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()));

    const matchesCategory = !selectedCategory ||
      `${post.first_level_category}/${post.second_level_category}` === selectedCategory;

    return matchesSearch && matchesCategory;
  });

  $: categories = [...new Set(posts.map(post =>
    `${post.first_level_category}/${post.second_level_category}`
  ))].sort();

  onMount(async () => {
    await loadPosts();
  });

  async function loadPosts() {
    try {
      loading = true;
      error = '';
      posts = await postService.getAllPosts();
    } catch (err) {
      error = 'Failed to load posts: ' + (err.message || 'Unknown error');
      console.error('Error loading posts:', err);
    } finally {
      loading = false;
    }
  }

  function formatDate(dateString) {
    try {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    } catch (err) {
      return dateString;
    }
  }

  function handleEdit(slug) {
    window.location.href = `/admin/editor/${slug}`;
  }

  function handleDelete(post) {
    postToDelete = post;
    showDeleteModal = true;
  }

  async function confirmDelete() {
    if (!postToDelete) return;

    try {
      await postService.deletePost(postToDelete.slug);
      posts = posts.filter(p => p.slug !== postToDelete.slug);
      showDeleteModal = false;
      postToDelete = null;
    } catch (err) {
      error = 'Failed to delete post: ' + (err.message || 'Unknown error');
      console.error('Error deleting post:', err);
    }
  }

  function cancelDelete() {
    showDeleteModal = false;
    postToDelete = null;
  }

  function clearFilters() {
    searchTerm = '';
    selectedCategory = '';
  }
</script>

<div class="posts-table-container">
  <!-- Search and Filters -->
  <div class="table-controls">
    <div class="search-section">
      <input
        type="text"
        placeholder="Search posts..."
        bind:value={searchTerm}
        class="search-input"
      />
    </div>

    <div class="filter-section">
      <select bind:value={selectedCategory} class="category-filter">
        <option value="">All Categories</option>
        {#each categories as category}
          <option value={category}>{category}</option>
        {/each}
      </select>

      {#if searchTerm || selectedCategory}
        <button on:click={clearFilters} class="clear-filters-btn">
          Clear Filters
        </button>
      {/if}
    </div>
  </div>

  <!-- Error Message -->
  {#if error}
    <div class="error-message">
      {error}
      <button on:click={loadPosts} class="retry-btn">Retry</button>
    </div>
  {/if}

  <!-- Loading State -->
  {#if loading}
    <div class="loading-state">
      <div class="loading-spinner"></div>
      <p>Loading posts...</p>
    </div>
  {:else}
    <!-- Posts Table -->
    <div class="table-wrapper">
      <table class="posts-table">
        <thead>
          <tr>
            <th>Title</th>
            <th class="hidden-mobile">Category</th>
            <th class="hidden-mobile">Author</th>
            <th class="hidden-mobile">Published</th>
            <th class="hidden-mobile">Tags</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {#each filteredPosts as post (post.slug)}
            <tr class="post-row" class:draft={post.draft}>
              <td class="title-cell">
                <div class="title-content">
                  <span class="post-title">{post.title}</span>
                  {#if post.draft}
                    <span class="draft-badge">Draft</span>
                  {/if}
                  <!-- Mobile-only additional info -->
                  <div class="mobile-info">
                    <span class="mobile-category">{post.first_level_category}/{post.second_level_category}</span>
                    <span class="mobile-date">{formatDate(post.published)}</span>
                  </div>
                </div>
              </td>

              <td class="hidden-mobile category-cell">
                <div class="category-stack">
                  <span class="first-category">{post.first_level_category}</span>
                  <span class="second-category">{post.second_level_category}</span>
                </div>
              </td>

              <td class="hidden-mobile author-cell">
                {post.author || 'Unknown'}
              </td>

              <td class="hidden-mobile date-cell">
                {formatDate(post.published)}
              </td>

              <td class="hidden-mobile tags-cell">
                {#if post.tags && post.tags.length > 0}
                  <div class="tags-container">
                    {#each post.tags.slice(0, 3) as tag}
                      <span class="tag">{tag}</span>
                    {/each}
                    {#if post.tags.length > 3}
                      <span class="tag-more">+{post.tags.length - 3}</span>
                    {/if}
                  </div>
                {:else}
                  <span class="no-tags">No tags</span>
                {/if}
              </td>

              <td class="actions-cell">
                <div class="action-buttons">
                  <button
                    on:click={() => handleEdit(post.slug)}
                    class="action-btn edit-btn"
                    title="Edit post"
                  >
                    Edit
                  </button>
                  <button
                    on:click={() => handleDelete(post)}
                    class="action-btn delete-btn"
                    title="Delete post"
                  >
                    Delete
                  </button>
                </div>
              </td>
            </tr>
          {:else}
            <tr>
              <td colspan="6" class="no-posts">
                {searchTerm || selectedCategory ? 'No posts match your filters' : 'No posts found'}
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>

    <!-- Results Summary -->
    <div class="results-summary">
      Showing {filteredPosts.length} of {posts.length} posts
    </div>
  {/if}
</div>

<!-- Delete Confirmation Modal -->
{#if showDeleteModal && postToDelete}
  <div
    class="modal-overlay"
    on:click={cancelDelete}
    on:keydown={(e) => e.key === 'Escape' && cancelDelete()}
    role="button"
    tabindex="0"
  >
    <div
      class="modal-content"
      on:click|stopPropagation
      on:keydown|stopPropagation
      role="dialog"
      tabindex="-1"
    >
      <h3 class="modal-title">Confirm Delete</h3>
      <p class="modal-message">
        Are you sure you want to delete "<strong>{postToDelete.title}</strong>"?
        This action cannot be undone.
      </p>
      <div class="modal-actions">
        <button on:click={cancelDelete} class="modal-btn cancel-btn">
          Cancel
        </button>
        <button on:click={confirmDelete} class="modal-btn confirm-btn">
          Delete
        </button>
      </div>
    </div>
  </div>
{/if}

<style>
  .posts-table-container {
    background: white;
    border-radius: 8px;
    box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
    overflow: hidden;
  }

  .table-controls {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem;
    border-bottom: 1px solid #e5e7eb;
    gap: 1rem;
  }

  .search-section {
    flex: 1;
    max-width: 400px;
  }

  .search-input {
    width: 100%;
    padding: 0.5rem 0.75rem;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    font-size: 0.875rem;
    transition: border-color 0.2s;
  }

  .search-input:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgb(59 130 246 / 0.1);
  }

  .filter-section {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  .category-filter {
    padding: 0.5rem 0.75rem;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    font-size: 0.875rem;
    background: white;
  }

  .clear-filters-btn {
    padding: 0.5rem 1rem;
    background: #f3f4f6;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    font-size: 0.875rem;
    cursor: pointer;
    transition: background-color 0.2s;
  }

  .clear-filters-btn:hover {
    background: #e5e7eb;
  }

  .error-message {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 1.5rem;
    background: #fef2f2;
    color: #dc2626;
    border-bottom: 1px solid #fecaca;
  }

  .retry-btn {
    padding: 0.25rem 0.75rem;
    background: #dc2626;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 0.875rem;
    cursor: pointer;
  }

  .loading-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem;
    color: #6b7280;
  }

  .loading-spinner {
    width: 2rem;
    height: 2rem;
    border: 2px solid #e5e7eb;
    border-top: 2px solid #3b82f6;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 1rem;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  .table-wrapper {
    overflow-x: auto;
  }

  .posts-table {
    width: 100%;
    border-collapse: collapse;
  }

  .posts-table th {
    text-align: left;
    padding: 1rem 1.5rem;
    background: #f9fafb;
    border-bottom: 1px solid #e5e7eb;
    font-weight: 600;
    font-size: 0.875rem;
    color: #374151;
  }

  .posts-table td {
    padding: 1rem 1.5rem;
    border-bottom: 1px solid #f3f4f6;
    vertical-align: top;
  }

  .post-row:hover {
    background: #f9fafb;
  }

  .post-row.draft {
    background: #fefce8;
  }

  .title-cell {
    min-width: 200px;
  }

  .title-content {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .post-title {
    font-weight: 500;
    color: #111827;
    line-height: 1.4;
  }

  .draft-badge {
    display: inline-block;
    padding: 0.125rem 0.5rem;
    background: #fbbf24;
    color: #92400e;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 500;
    width: fit-content;
  }

  .mobile-info {
    display: none;
    flex-direction: column;
    gap: 0.25rem;
    font-size: 0.75rem;
    color: #6b7280;
  }

  .category-stack {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .first-category {
    font-weight: 500;
    color: #374151;
  }

  .second-category {
    font-size: 0.875rem;
    color: #6b7280;
  }

  .tags-container {
    display: flex;
    flex-wrap: wrap;
    gap: 0.25rem;
  }

  .tag {
    display: inline-block;
    padding: 0.125rem 0.5rem;
    background: #eff6ff;
    color: #1d4ed8;
    border-radius: 9999px;
    font-size: 0.75rem;
  }

  .tag-more {
    display: inline-block;
    padding: 0.125rem 0.5rem;
    background: #f3f4f6;
    color: #6b7280;
    border-radius: 9999px;
    font-size: 0.75rem;
  }

  .no-tags {
    color: #9ca3af;
    font-style: italic;
    font-size: 0.875rem;
  }

  .action-buttons {
    display: flex;
    gap: 0.5rem;
  }

  .action-btn {
    padding: 0.375rem 0.75rem;
    border: 1px solid;
    border-radius: 4px;
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
  }

  .edit-btn {
    background: #eff6ff;
    border-color: #bfdbfe;
    color: #1d4ed8;
  }

  .edit-btn:hover {
    background: #dbeafe;
    border-color: #93c5fd;
  }

  .delete-btn {
    background: #fef2f2;
    border-color: #fecaca;
    color: #dc2626;
  }

  .delete-btn:hover {
    background: #fee2e2;
    border-color: #fca5a5;
  }

  .no-posts {
    text-align: center;
    padding: 3rem;
    color: #6b7280;
    font-style: italic;
  }

  .results-summary {
    padding: 1rem 1.5rem;
    background: #f9fafb;
    border-top: 1px solid #e5e7eb;
    font-size: 0.875rem;
    color: #6b7280;
    text-align: center;
  }

  /* Modal Styles */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
  }

  .modal-content {
    background: white;
    border-radius: 8px;
    padding: 2rem;
    max-width: 400px;
    width: 90%;
    margin: 1rem;
  }

  .modal-title {
    margin: 0 0 1rem 0;
    font-size: 1.25rem;
    font-weight: 600;
    color: #111827;
  }

  .modal-message {
    margin: 0 0 2rem 0;
    color: #374151;
    line-height: 1.5;
  }

  .modal-actions {
    display: flex;
    gap: 0.75rem;
    justify-content: flex-end;
  }

  .modal-btn {
    padding: 0.5rem 1rem;
    border: 1px solid;
    border-radius: 6px;
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
  }

  .cancel-btn {
    background: white;
    border-color: #d1d5db;
    color: #374151;
  }

  .cancel-btn:hover {
    background: #f9fafb;
  }

  .confirm-btn {
    background: #dc2626;
    border-color: #dc2626;
    color: white;
  }

  .confirm-btn:hover {
    background: #b91c1c;
  }

  /* Mobile Responsive */
  @media (max-width: 768px) {
    .table-controls {
      flex-direction: column;
      align-items: stretch;
      gap: 1rem;
    }

    .filter-section {
      justify-content: space-between;
    }

    .hidden-mobile {
      display: none;
    }

    .mobile-info {
      display: flex;
    }

    .action-buttons {
      flex-direction: column;
    }

    .action-btn {
      text-align: center;
    }

    .posts-table th,
    .posts-table td {
      padding: 0.75rem;
    }
  }
</style>