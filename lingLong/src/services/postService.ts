/**
 * Post Service
 * Handles CRUD operations for blog posts
 */

import { apiClient } from './apiClient';
import type { ApiResponse } from './apiClient';

// Post metadata interface - matches backend PostMetadata
export interface PostMetadata {
  slug: string;
  title: string;
  published: string; // Date string
  description?: string;
  tags?: string[];
  first_level_category: string;
  second_level_category: string;
  author?: string;
  draft?: boolean;
  cover?: string;
  sourceLink?: string;
  licenseName?: string;
  licenseUrl?: string;
}

// Full post interface - includes content
export interface PostFull extends PostMetadata {
  content: string;
}

// Post creation interface
export interface PostCreate {
  title: string;
  content: string;
  published?: string;
  description?: string;
  tags?: string[];
  first_level_category: string;
  second_level_category: string;
  author?: string;
  draft?: boolean;
  cover?: string;
  sourceLink?: string;
  licenseName?: string;
  licenseUrl?: string;
}

// Post update interface - all fields optional
export interface PostUpdate {
  title?: string;
  content?: string;
  published?: string;
  description?: string;
  tags?: string[];
  first_level_category?: string;
  second_level_category?: string;
  author?: string;
  draft?: boolean;
  cover?: string;
  sourceLink?: string;
  licenseName?: string;
  licenseUrl?: string;
}

class PostService {
  private apiPrefix = '/api/admin';

  /**
   * Get all posts metadata (without content)
   */
  async getAllPosts(): Promise<PostMetadata[]> {
    return apiClient.get<PostMetadata[]>(`${this.apiPrefix}/posts`);
  }

  /**
   * Get post by slug (with full content)
   */
  async getPostBySlug(slug: string): Promise<PostFull> {
    return apiClient.get<PostFull>(`${this.apiPrefix}/posts/${slug}`);
  }

  /**
   * Create new post
   */
  async createPost(postData: PostCreate): Promise<ApiResponse> {
    return apiClient.post<ApiResponse>(`${this.apiPrefix}/posts`, postData);
  }

  /**
   * Update existing post
   */
  async updatePost(slug: string, postData: PostUpdate): Promise<ApiResponse> {
    return apiClient.put<ApiResponse>(`${this.apiPrefix}/posts/${slug}`, postData);
  }

  /**
   * Delete post
   */
  async deletePost(slug: string): Promise<ApiResponse> {
    return apiClient.delete<ApiResponse>(`${this.apiPrefix}/posts/${slug}`);
  }

  /**
   * Get posts grouped by categories
   */
  async getPostsByCategory(): Promise<Record<string, PostMetadata[]>> {
    const posts = await this.getAllPosts();
    const grouped: Record<string, PostMetadata[]> = {};

    posts.forEach(post => {
      const categoryKey = `${post.first_level_category}/${post.second_level_category}`;
      if (!grouped[categoryKey]) {
        grouped[categoryKey] = [];
      }
      grouped[categoryKey].push(post);
    });

    return grouped;
  }

  /**
   * Search posts by title or tags
   */
  async searchPosts(query: string): Promise<PostMetadata[]> {
    const posts = await this.getAllPosts();
    const searchTerm = query.toLowerCase();

    return posts.filter(post =>
      post.title.toLowerCase().includes(searchTerm) ||
      post.tags?.some(tag => tag.toLowerCase().includes(searchTerm)) ||
      post.description?.toLowerCase().includes(searchTerm)
    );
  }
}

// Export singleton instance
export const postService = new PostService();