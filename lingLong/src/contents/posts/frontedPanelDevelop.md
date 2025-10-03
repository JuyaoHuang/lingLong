---
title: "fronted Admin-panel Development"
published: 2025-10-01
tags: ['技术改进']
first_level_category: "blog项目"
second_level_category: "backendDevelop"
author: "Alen"
draft: false
---
<div align="right"> <a href="/posts/frontedPanelDevelop"><strong>English</strong></a> | <a href="/posts/前端管理员面板开发">简体中文</a> </div>

# Frontend Admin Panel Development

​	***A summary can be found in another, longer article, which is primarily a collection of bug fixes*** ==> [Click here](./frontedAdminPanelSummary.md)

​	This document outlines a robust and maintainable admin system architecture designed from a pure frontend perspective, intended for seamless integration into an Astro project. This architecture will be completely independent of any backend implementation.

## Core Architecture Principles

1. **Client-Side Rendering Zone**:

   1. The public-facing blog should maintain Astro's SSG (Static Site Generation) advantages for ultimate performance and SEO.
   2. The entire admin backend (from login to post editing) will be a **Single Page Application (SPA)** that runs entirely on the client side.
   3. We will utilize Astro's client:only directive to create this "SPA Zone," ensuring that the dynamic logic of the backend does not impact the performance of the static site.

2. **Strict Separation of Concerns**:

   ​	The frontend code will be divided into clear, single-responsibility modules.

   - UI components are only responsible for rendering.

   - Service modules are only responsible for business logic and data requests.

   - State management modules are only responsible for maintaining application state.

     This separation is the foundation for maintainability and testability.

3. **Stateless Authentication**:

   ​	The frontend application itself will not store any persistent user state. The application's "logged-in state" is determined solely by the presence of a valid JWT stored in localStorage. This is the frontend's **Single Source of Truth**.

## Frontend Engineering Architecture

The Astro project's src/ directory will be extended with the following structure:

```
    src/
├── pages/
│   ├── posts/
│   │   └── [slug].astro       // (Public) Blog post page (SSG)
│   ├── index.astro            // (Public) Blog homepage (SSG)
│   │
│   └── admin/                 // [New] Root route for the admin application
│       ├── login.astro        // Admin login page (entry point)
│       ├── dashboard.astro    // Admin dashboard/post list page
│       ├── editor/
│           ├── new.astro      // New post page
│           └── [slug].astro   // Edit post page
│
├── components/
│   ├── admin/                 // [New] All dedicated admin UI components
│   │   ├── LoginForm.svelte      // Login form (interactive component)
│   │   ├── PostTable.svelte      // Post list table (interactive component)
│   │   └── Editor.svelte         // Markdown editor (interactive component)
│
├── script/
│   └── managePost.js 				// Actual operator for file modifications (backup)
│
├── layouts/
│   ├── AdminLayout.astro      // [New] Common layout for admin pages
│
└── services/                  // [New] Core business logic layer (pure TS)
    ├── authService.ts         // Auth Service: Handles login, logout, token management
    ├── apiClient.ts           // API Client: Wraps fetch, automatically attaches JWT
    ├── postService.ts         // Post Service: Handles CRUD data requests for posts
  
```

### Core Module Design & Responsibilities

#### 1. **Services Layer**

This is the brain of the entire admin application, handling all non-UI logic.

- **authService.ts**:

  - **Responsibility**: Provides methods like login(username, password), logout(), getToken(), and isLoggedIn().
  - login(): Sends credentials to the future backend endpoint /api/auth/token. On success, stores the received JWT in localStorage.
  - logout(): Removes the JWT from localStorage.
  - getToken(): Reads the JWT from localStorage.
  - isLoggedIn(): Checks if a JWT exists in localStorage (can be enhanced later to decode and check for expiration).

- **apiClient.ts**:

  - **Responsibility**:

    ​	Creates a centralized, configurable HTTP request client (can be thought of as a custom Axios instance).

  - **Core Functionality**:

    ​	Wraps the native fetch API. Internally, for **all non-public** requests, it automatically calls authService.getToken() and adds the JWT to the Authorization: Bearer` <token>` request header.

  - **Benefits**:

    ​	Centralizes the logic for attaching authentication headers, avoiding repetitive code in every component's request. It can also handle the base API URL, timeouts, and error formatting uniformly.

- **postService.ts**:

  - **Responsibility**:

    ​	Provides methods like getAllPosts(), getPostBySlug(slug), createPost(data), updatePost(slug, data), and deletePost(slug).

  - **Implementation**:

    ​	 This module **does not execute fetch directly**. It calls the apiClient to make requests, thereby automatically getting the JWT injection. For example, getAllPosts() would internally call apiClient.get('/api/admin/posts').

#### 2. **Page and Routing Layer (src/pages/admin/)**

- **login.astro**:

  - **Architecture**: The page itself is an Astro file, responsible for providing the basic HTML structure and SEO metadata.

  - **Core**:

    ​	The page will import an interactive component (e.g.,` <LoginForm client:only="svelte" />`). All user interaction, state management, and API calls are handled within this client-side component, which will call authService.login().

- **Protected Pages (e.g., dashboard.astro)**:

  - **Architecture**: Similarly, an Astro file acts as a shell, loading a main client-side component like `<DashboardPage client:only="svelte" />`.

  - **Route Guard Implementation**: Astro pages are static and cannot perform server-side redirects directly. Therefore, we embed a **Bootstrap Script** at the top of the page.----For reference only

    ```js
        <!-- dashboard.astro -->
    <script is:inline>
      // This script executes first, synchronously
      import { isLoggedIn } from '../../services/authService';
      if (!isLoggedIn()) {
        // If not logged in, redirect immediately before any content renders
        window.location.href = '/admin/login';
      }
    </script>
    
    <AdminLayout>
      <!-- The component below will only be rendered and executed if the check passes -->
      <DashboardPage client:only="svelte" />
    </AdminLayout>
      
    ```

  - **Logic**: This inline script forms a client-side "route guard." It checks the login state at the very beginning of the page rendering process, thereby protecting the entire page.

#### 3. **Component Layer (src/components/admin/)**

- **Responsibility**: To build reusable, interactive UI units. These components should be designed as "controlled" or "presentational" components.

- **Interaction Logic**:

  ​	Components receive data via props and communicate user intent upwards through callback functions (e.g., onSave, onDelete). The component itself **does not directly call** postService; instead, it calls functions passed down from its parent page/component.

- **Example (PostTable.svelte)**:

  1. It receives a posts array to render a table. When a user clicks the delete button, it calls props.onDelete(postId). The actual API request logic is handled by the parent component (DashboardPage).

- **Reusable Component (AdminPostCard.astro)**:

  1. Reuses the card style from the public-facing PostCard.astro component to render the layout of the post list in dashboard.astro.

  2. Uses import { Icon } from "astro-icon/components" to reuse existing icon styles (same as PostCard.astro).

  3. Since it only receives summarized post data:

     1. Title
     2. First Level Category
     3. Second Level Category
     4. Date
     5. Tags
     6. Author

     It does not have an image parameter, so its props differ from PostCard.astro.

- **Data Structure Transmitted by the Backend**

  ```py
  from pydantic import BaseModel
  from typing import Optional, List
  from datetime import date
  
  class PostMetadata(BaseModel):
      """
      Post metadata model - matches frontend AdminPostCard.astro Props interface
      Used for article list display without content body
      """
      slug: str
      title: str
      published: date  
      description: Optional[str] = None
      tags: Optional[List[str]] = None
      first_level_category: str
      second_level_category: str
      author: Optional[str] = None
      draft: Optional[bool] = False
      cover: Optional[str] = None
      sourceLink: Optional[str] = None
      licenseName: Optional[str] = None
      licenseUrl: Optional[str] = None
    
  ```

  The data structure for the post list fetched by the frontend admin panel should match this model.

### Data Flow & Workflow

1. **User visits /admin/dashboard**:
   1. The Astro page loads, and the inline "route guard" script executes.
   2. authService.isLoggedIn() checks localStorage.
   3. If **not logged in**, the page redirects to /admin/login.
   4. If **logged in**, the page continues to render, and the <DashboardPage> client-side component is mounted.
2. **DashboardPage Component Mounts**:
   1. The component's onMount (or equivalent lifecycle hook) is triggered.
   2. It calls postService.getAllPosts() to request data.
   3. postService calls apiClient.get(...).
   4. apiClient calls authService.getToken(), places the JWT in the request header, and initiates the fetch request.
   5. Upon receiving the backend response, the data is returned up the call chain to the component.
   6. The component updates its internal state and passes the data as props to the `<PostTable>` component, updating the UI.

​	With this architecture, you can build a structurally sound, logically separated, and easily extendable frontend admin system without touching the backend. All logic for communicating with the backend is perfectly encapsulated in the services layer, ready to be filled in with real FastAPI endpoint implementations in the future.

### Specific Component Adjustments

#### Questions

1. **UI Design Preference**: Do you prefer to reuse the existing PostCard card-based layout, or is a table-based management interface required?
2. **Editor Functionality**: What level of Markdown editor is needed? A simple textbox or a rich-text editor with a live preview?
3. **Permission Design**: Are different permission levels needed (e.g., read-only vs. editor), or does any logged-in user have full privileges?
4. **Responsive Requirements**: Does the admin backend need to support mobile access?

#### Solutions

1. **Choose a Table-based management interface.**

   In the PostTable.svelte component, use standard <table> elements. With the help of Tailwind CSS, a plain table can be made to look beautiful and professional.

2. **Use the VS Code core editor, Monaco Editor, as the Markdown editor.**

3. **Logged-in users have full privileges**, as there will only be one administrator.

4. **Implement a responsive design** to ensure a good display on mobile devices, while prioritizing the desktop experience.

   ​	With a modern CSS framework like Tailwind CSS, the extra work to implement responsive layouts is minimal. You just need to use breakpoint prefixes like sm:, md:, lg: to adjust the layout.

   - **Specific Example**:

     ​	A **Table** displayed on a desktop can easily be converted into a **List of Cards** on mobile (small screens). This avoids horizontal scrollbars and provides a much better user experience.

#### Important Notes

1. **Using Monaco Editor**:

   ​	Monaco Editor is not a typical UI component library. It is a highly complex, self-contained "mini-VS Code." Therefore, integrating it into a modern frontend framework (like Astro/Svelte with Vite) requires a few more steps than simply importing a component.

   **The Core Issue**:

   ​	Monaco Editor includes numerous Web Workers (for syntax analysis, intellisense, etc., for different languages), and its module loading mechanism differs slightly from standard JavaScript modules. A direct import often causes bundlers (like Vite) to fail or work inefficiently.

   **Complete Steps for Integrating Monaco Editor (Astro + Svelte)**:

   1. **Install Dependencies**

      ```bash
          # Install the Monaco Editor core library
      pnpm add monaco-editor
      
      # Install the Vite plugin specifically for Monaco Editor
      #   This is the most critical step, as it handles all complex bundling issues.
      pnpm add -D vite-plugin-monaco-editor
        
      ```

   2. **Configure Vite (in Astro)**

      Tell Astro (and its underlying Vite bundler) to use the newly installed plugin.

      1. Open the Astro config file: yukina/astro.config.mjs.
      2. Modify the file to import and add monacoEditorPlugin.

      Example:

      ```js
      import { defineConfig } from 'astro/config';
      import svelte from '@astrojs/svelte';
      import tailwind from '@astrojs/tailwind';
      //  Import the plugin
      import monacoEditorPlugin from 'vite-plugin-monaco-editor';
      
      // https://astro.build/config
      export default defineConfig({
        integrations: [svelte(), tailwind()],
        // Add Vite configuration
        vite: {
          plugins: [
            // Note: The plugin needs to be called as monacoEditorPlugin.default()
            monacoEditorPlugin.default({})
          ]
        }
      });
        
      ```

   3. **Wrap Monaco Editor in a Svelte Component**

      ​	Create an Editor.svelte component to load and control the editor. The best practice for interacting with libraries that require direct DOM manipulation in Svelte is to use the onMount lifecycle function and the bind:this directive.

   4. **Use the Editor Component in an Astro Page**

      Now you can use Editor.svelte just like any other Svelte component.

      **However, there is one crucial consideration**: Monaco Editor is a purely client-side library; it cannot be server-side rendered (SSR).

      Therefore, you **must** use the **client:only** directive to load it.

**Summary**

1. **Install**: pnpm add monaco-editor and pnpm add -D vite-plugin-monaco-editor.
2. **Configure**: Add the Vite plugin in astro.config.mjs.
3. **Wrap**: In a Svelte component (.svelte), use onMount and bind:this to initialize and control the Monaco Editor instance.
4. **Use**: In an Astro page (.astro), you **must** use the` <Editor client:only="svelte" /> `directive to load the component.
