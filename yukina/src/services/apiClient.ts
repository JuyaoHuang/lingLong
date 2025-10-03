/**
 * API Client
 * Encapsulates fetch API with automatic JWT authentication header handling
 */

import { authService } from './authService';

export interface ApiResponse<T = any> {
  success?: boolean;
  message?: string;
  data?: T;
}

class ApiClient {
  // 使用空字符串，这样所有请求都会使用相对路径
  // 在生产环境中，请求会通过Nginx代理到backend
  // 在开发环境中，可以通过环境变量配置完整URL
  private baseURL = import.meta.env.PUBLIC_API_URL || '';

  /**
   * Execute HTTP request
   */
  private async request<T = any>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;

    // Merge default headers with proper typing
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...options.headers as Record<string, string>,
    };

    // Auto-add auth header if logged in
    const authHeader = authService.getAuthHeader();
    if (authHeader) {
      headers['Authorization'] = authHeader;
    }

    const config: RequestInit = {
      ...options,
      headers,
    };

    try {
      const response = await fetch(url, config);

      // Handle authentication failure
      if (response.status === 401) {
        authService.logout();
        throw new Error('Authentication failed, please login again');
      }

      // Handle other errors
      if (!response.ok) {
        throw new Error(`HTTP Error: ${response.status} ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  /**
   * GET request
   */
  async get<T = any>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'GET' });
  }

  /**
   * POST request
   */
  async post<T = any>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  /**
   * PUT request
   */
  async put<T = any>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  /**
   * DELETE request
   */
  async delete<T = any>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'DELETE' });
  }

  /**
   * File upload (FormData)
   */
  async upload<T = any>(endpoint: string, formData: FormData): Promise<T> {
    const authHeader = authService.getAuthHeader();
    const headers: Record<string, string> = {};

    if (authHeader) {
      headers['Authorization'] = authHeader;
    }

    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'POST',
      headers,
      body: formData,
    });

    if (response.status === 401) {
      authService.logout();
      throw new Error('Authentication failed, please login again');
    }

    if (!response.ok) {
      throw new Error(`HTTP Error: ${response.status} ${response.statusText}`);
    }

    return await response.json();
  }
}

// Export singleton instance
export const apiClient = new ApiClient();