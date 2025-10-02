/**
 * Authentication Service
 * Manages JWT token and user authentication state
 */

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

class AuthService {
  private tokenKey = 'admin_token';

  /**
   * User login
   */
  async login(credentials: LoginCredentials): Promise<boolean> {
    try {
      const formData = new FormData();
      formData.append('username', credentials.username);
      formData.append('password', credentials.password);

      // 使用相对路径，请求会通过Nginx代理到backend
      const response = await fetch('/token', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data: AuthResponse = await response.json();
        this.setToken(data.access_token);
        return true;
      }
      return false;
    } catch (error) {
      console.error('Login error:', error);
      return false;
    }
  }

  /**
   * User logout
   */
  logout(): void {
    localStorage.removeItem(this.tokenKey);
  }

  /**
   * Get stored token
   */
  getToken(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  /**
   * Set token
   */
  private setToken(token: string): void {
    localStorage.setItem(this.tokenKey, token);
  }

  /**
   * Check if user is logged in
   */
  isLoggedIn(): boolean {
    const token = this.getToken();
    if (!token) return false;

    // TODO: Add token expiration check
    // Currently only checks if token exists
    return true;
  }

  /**
   * Get Authorization header value with Bearer prefix
   */
  getAuthHeader(): string | null {
    const token = this.getToken();
    return token ? `Bearer ${token}` : null;
  }
}

// Export singleton instance
export const authService = new AuthService();