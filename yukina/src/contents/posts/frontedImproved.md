---
title: Front-end Improvement Plan
published: 2025-10-01
description: Layout adjustments for the blog's front-end pages
tags: [Technical Improvement]
first_level_category: 'blog项目'
second_level_category: 'frontedDevelop'
author: Alen
---
<div align="right"> <a href="/posts/frontedImproved"><strong>English</strong></a> | <a href="/posts/前端改进方案">简体中文</a> </div>

# Front-end Improvement Plan

## Improvement Requirements

1. **Two-level Categories**:
   1. Each post will have two categories: first_level_category and second_level_category.
   2. The first-level category is a broad classification based on the post's attributes, such as AI Frontiers, Poetry Sharing, News Briefs, Math Topics, Embedded Systems, Programming Collections, etc.
   3. The second-level category is for different directions within that field. For example, Programming Collections could include Python, C++, JS, VUE.
2. **Card-style Article Presentation**:
   1. Replace the current "Timeline/Archive style after clicking a category" with a card-style layout similar to the homepage.
3. **Format Flow**: Homepage -> First-level Category List -> Second-level Category List -> Post List.
4. **Presentation Layouts**:
   1. First-level Category List: Use yukina/src/layouts/ChipLayout.astro.
   2. Second-level Category List: Use yukina/src/layouts/ChipLayout.astro.
   3. Post List (after clicking a second-level category): Use the yukina/src/components/PostCard.astro component.

## Improvement Plan

### Step 1: Modify the Content Data Model (src/content.config.ts)

1. **Update Data Model**: Replace the original single category field category: z.string().optional() with a two-level structure:

   ```ts
   first_level_category: z.string(),    // First-level category (required)
   second_level_category: z.string(),   // Second-level category (required)
   ```

1. **Adapt Component Interfaces**:
   - **PostCard Component** (src/components/PostCard.astro):
     - Update the Props interface to support the new category fields.
     - Modify the category link generation logic: clicking a category tag should navigate to the first-level category page.
     - Keep the behavior of post titles/images linking to the post details page.
   - **Data Passing Optimization** (src/utils/content.ts):
     - Add a new postCard interface to include all data required for card presentation.
     - Standardize data passing: pass the raw ID and let the component handle URL generation.
     - Ensure compatibility with both HASH and RAW slug modes.

### Step 2: Implement Category Handling and Routing System

1. **Category Data Processing Functions** (src/utils/content.ts):

   - **getFirstCategories()**:
     - Get all first-level categories and the count of posts within each.
     - Generate chip data required for the first-level category page.
     - Support the /categories/index.astro page display.
   - **getSecondCategories()**:
     - Process second-level category data and build the full category path.
     - Collect the list of posts for each second-level category.
     - **Important Optimization**: Sort posts by publication date in descending order (newest first).
     - Generate data in the postCard format, including category information.

2. **Routing Structure Design**:

   ```
   /categories/                              # First-level category list
   /categories/[first_category]/             # Second-level category list
   /categories/[first_category]/[second_category]/  # Post list
   ```

3. **URL Generation Strategy**:

   - Support both HASH and RAW slug modes.
   - Standardize URL conversion using the IdToSlug() function.
   - Resolve issues with duplicate URL prefixes to prevent 404 errors.

### Step 3: Optimize Page Layout and User Experience

1. **Layout Component Selection**:

   - **First-level Category Page** (/categories/[first_category].astro):
     - Use ChipLayout.astro to display second-level category options.
     - Show the number of posts under each second-level category.
   - **Second-level Category Page** (/categories/[first_category]/[second_category].astro):
     - Use the PostCard.astro component to display posts in a card grid.
     - Responsive design: single column on mobile, two on tablets, three on desktops (adjustable).
     - **Key Improvement**: Posts are sorted by publication date in descending order, showing the newest posts first.

2. **Data Flow Optimization**:

   ```ts
   // Raw Data → Processing Function → Page Component
   Markdown File → getSecondCategories() → PostCard Component
   
   // Key Improvement: Sorting Logic
   category.posts.sort((a, b) => {
     return new Date(a.published) > new Date(b.published) ? -1 : 1;
   });
   ```

3. **User Experience Enhancements**:

   - Category information is correctly displayed in the PostCard component.
   - Clicking category tags navigates to the corresponding first-level category page.
   - Newest posts are displayed first, eliminating the need to scroll.
   - The URL structure is clean, supporting direct access and bookmarking.

## Improvement Results

### Completed Features

1. **Two-level Category System**:
   - ✅ Data Model Support: first_level_category and second_level_category.
   - ✅ Routing Structure: Homepage → First-level List → Second-level List → Post List.
   - ✅ URL Mode Support: Compatible with both HASH and RAW modes.
2. **Component and Layout Optimization**:
   - ✅ First-level Category Page: Uses ChipLayout.astro for category cards.
   - ✅ Second-level Category Page: Uses PostCard.astro for card-style post display.
   - ✅ Responsive Design: Single/double/triple column layout for different screen sizes.
3. **URL Generation Optimization**:
   - ✅ Standardized Data Passing: Pass raw IDs, let components handle URLs.
   - ✅ Mode-agnostic Design: Code seamlessly supports both HASH and RAW modes.
   - ✅ 404 Fix: Resolved routing errors caused by duplicate URL prefixes.
4. **User Experience Enhancements**:
   - ✅ Post Sorting: Category pages sort posts by publication date (newest first).
   - ✅ Category Info Display: PostCard correctly shows both category levels.
   - ✅ Navigation: Clicking tags navigates to the first-level category page.

### Actual Routing Structure

```
/categories/                                    # First-level category list (ChipLayout)
├── /categories/blog-understanding-docs/        # Second-level category list (ChipLayout)
│   ├── /categories/blog-understanding-docs/blog/   # Post list (PostCard grid)
│   └── /categories/blog-understanding-docs/blogs/  # Post list (PostCard grid)
├── /categories/Examples/                       # Second-level category list (ChipLayout)
│   └── /categories/Examples/ex/                # Post list (PostCard grid)
└── /categories/math-theory/                    # Second-level category list (ChipLayout)
    └── /categories/math-theory/math/           # Post list (PostCard grid)
```

### Key Technical Implementations

1. **Data Interface Design**:

   ```ts
   // src/utils/content.ts
   export interface postCard {
     id: string;
     title: string;
     published: Date;
     first_level_category?: string;  // Added
     second_level_category?: string; // Added
     tags?: string[];
     description?: string;
     image?: string;
     readingMetadata?: { time: number; wordCount: number };
   }
   ```

2. **Key Functions**:

   - getFirstCategories(): Processes first-level category data.
   - getSecondCategories(): Processes second-level data, including post sorting.
   - Standardized URL generation: IdToSlug() handles conversion based on config.

3. **Sorting Optimization**:

   ```ts
   // Sort posts on second-level category pages by date descending
   category.posts.sort((a, b) => {
     const dateA = new Date(a.published);
     const dateB = new Date(b.published);
     return dateA > dateB ? -1 : 1; // Newest posts first
   });
   ```

### Document Category Management

**Steps to Modify a Category Name**:

1. Bulk-replace the category fields in the relevant Markdown files.
2. Rebuild the project: npm run build.
3. URLs will update automatically (RAW mode is intuitive; HASH mode generates new hashes).

**Notes**:

- Changing a category name will change its URL.
- Deleting all posts under a category will cause that category page to disappear.
- The RAW mode is recommended for easier management and debugging.

## Additional Improvement -- Floating Table of Contents (TOC) Component

**Feature Upgrade: Implement a Floating Table of Contents (TOC) Component**

### Background and Solution

​	An initial attempt to use Typora's built-in [TOC] syntax failed because it is a proprietary extension, not a universal Markdown standard, and thus cannot be parsed by browsers or Astro's build tools.

​	To build a robust and flexible TOC in a web environment, a standardized technical approach was adopted: **extract heading data during the build process and pass it to a separate front-end component for dynamic rendering.**

​	The core advantage of this solution is **decoupling**: the content (data) is separate from the TOC (presentation). Unlike tools like mdast-util-toc that inject HTML directly into the content, this method provides a solid foundation for implementing complex UI interactions like floating positions and active highlighting.

### Core Architecture

​	The implementation relies on Astro's native capabilities and modern front-end techniques, comprising three main modules:

1. **Data Extraction**
   	When processing Markdown, Astro's render() method automatically parses the content structure and returns a headings array. This is the data source for the entire feature, requiring no external Remark plugins. Each heading object contains:

   - depth: The heading level (e.g., h2 corresponds to 2).
   - text: The plain text content of the heading.
   - slug: A URL-friendly, unique ID generated from the heading text, which Astro automatically injects as the id attribute into the corresponding `<h2>` tag.

2. **Component Rendering**

   ​	A separate Svelte component (FloatingTOC.svelte) was created, which accepts the headings array as its sole prop. The component's responsibility is to iterate over this array and render it as a list of anchor links (`<a href="#slug">`). This data-driven pattern ensures the component is reusable and maintainable.

3. **Front-end Interaction**

   - **Anchor Navigation**:
     	Leverages native browser functionality. Since Astro has already generated an id for each heading, clicking a link in the TOC triggers the browser's built-in smooth scrolling.

   - **Floating Position**:

     ​	Using the CSS position: fixed property, the TOC component is fixed to a specific position in the viewport, so it does not move as the page scrolls.

   - **Dynamic Highlighting**:

     ​	To enhance user experience, the Intersection Observer API is used to efficiently monitor heading elements in the article. When a heading enters the predefined viewport area, JavaScript adds an active class to the corresponding link in the TOC, achieving automatic highlighting on scroll with minimal performance overhead.

### Feasibility Analysis

Completely correct and feasible:

1. **Get TOC Data**
   - Astro has a built-in heading extraction feature, no extra plugins needed.
   - The headings array is automatically available from post.render().
   - Includes: depth (level), text (content), slug (anchor ID).
2. **Pass to a Floating UI Component**
   - Uses Astro's data-driven architecture.
   - Pass the headings array directly to a Svelte component.
   - Completely decoupled, does not affect post content.
3. **Article Content Remains Unchanged**
   - Astro automatically generates id attributes for headings (e.g.,` <h2 id="hello-world">`).
   - The browser natively supports anchor navigation (`#hello-world`).
   - No modifications to the source Markdown files are needed.

#### Technical Advantages

Superior to the previous mdast-util-toc approach:

- **Previous Problem**: Used an external plugin, leading to complex dependencies and potential errors.
- **New Solution Advantages**:
  - Uses Astro's built-in features, zero extra dependencies.
  - More reliable data extraction, no risk of parsing errors.
  - Cleaner code, better maintainability.

#### Implementation Steps (Simplified)

1. Modify the post page to get the built-in headings data from Astro.
2. Create a Svelte component to receive the headings array and render the floating TOC.
3. Add interactive features: scroll-based highlighting, smooth navigation.

**Key Point**: No Remark plugins are required; this is based entirely on Astro's native functionality.

### Implementation Details

**Completed**

1. **Native Integration, Zero Dependencies**:
   - Completely based on Astro's built-in render() method to extract the headings array, abandoning external plugins like mdast-util-toc and eliminating potential dependency conflicts and parsing errors.
2. **Independent Floating Component**:
   - The FloatingTOC.svelte component handles all UI rendering, supports indented display for multi-level headings, and is fully decoupled from the article content.
3. **Advanced Interactive Experience**:
   - **Smart Highlighting**: Based on the Intersection Observer API to highlight the TOC item corresponding to the current reading area in real-time.
4. **Refined UI/UX Design**:
   - **Custom Theme**: Adopts the muzimi color theme and applies a glassmorphism effect (backdrop-filter) for an enhanced visual feel.
   - **Dark Mode Adaptive**: Automatically responds to the operating system's color mode preference.
   - **Responsive Layout**: Displayed by default on desktops (>1200px) and automatically hidden on tablets and mobile devices to prioritize content readability.

### Key Technical Implementations

1. **Data Flow**:

   ```
   Markdown File → Astro render() → headings array → Svelte Component
   ```

2. **Core Files**:

   ```ts
   // src/pages/posts/[...slug].astro
   const { Content, headings } = await render(entry);
   
   // Move outside the layout to ensure it truly floats
   <>
     <PostLayout>...</PostLayout>
     <FloatingTOC headings={headings} client:load />
   </>
   ```

3. **Component Interface**:

   ```ts
   // src/components/FloatingTOC.svelte
   export let headings: Array<{
     depth: number;    // Heading level (1-6)
     text: string;     // Heading text
     slug: string;     // Anchor ID
   }> = [];
   ```

4. **Scroll Listener Optimization**:

   ```js
   // Using the modern Intersection Observer API
   observer = new IntersectionObserver((entries) => {
     entries.forEach((entry) => {
       if (entry.isIntersecting && entry.boundingClientRect.top <= 100) {
         activeId = entry.target.id;
       }
     });
   }, {
     rootMargin: '-100px 0px -80% 0px',
     threshold: 0
   });
   ```

### User Experience

**Viewing Effect**:

- **Desktop**: A floating TOC is displayed on the left, with smart highlighting on scroll.
- **Tablet/Mobile**: Automatically hidden to not interfere with the reading experience.
- **Interaction**: Clicking a TOC item scrolls to the corresponding heading.
- **Visual Feedback**: The heading for the current reading position is highlighted.

**Notes**:

- Based entirely on native browser features for excellent compatibility.
- Does not modify the source Markdown files, so document editing is unaffected.
- Only appears for posts that have headings; no empty component will be rendered.

### New Issues:

#### Issue 1: Floating TOC Fails to Update on Navigation

**Description**:
The TOC component appears correctly, but when navigating between posts, its content does not update; it continues to show the TOC of the previous post. A manual page refresh is required.

**Cause Analysis**:
Because the FloatingTOC component used the client:load directive, the JavaScript component instance was not being re-initialized during Astro's client-side page transitions. The project uses Swup for SPA-like navigation, which prevented the Svelte component from reacting correctly to page changes.

**Solution**: Abandon the Svelte component approach in favor of a pure JavaScript implementation integrated into Swup's page transition hooks.

**Key Implementation**:

1. Add a setupFloatingTOC() function in ScriptSetup.astro.
2. Integrate it into Swup's content:replace hook to ensure the TOC is recreated on every page transition.
3. Add cleanup logic for the old component to prevent memory leaks.

#### Issue 2: Search Function Fails

**Description**: Console error pagefind is not defined. The search function fails in both development and build modes.

**Cause Analysis**:

1. **Missing sharp Dependency**: The Astro build process failed because the sharp image processing library was missing, preventing the pagefind index from being generated.
2. **Development Mode Limitation**: The pagefind files are only generated during a **build**, so the /pagefind/pagefind.js path does not exist in development mode.

**Solution Approach**:

1. Install the missing dependency to fix the build issue.
2. Implement a graceful fallback for development mode.

**Solution**:

**Step 1: Fix Build Dependency**

```
pnpm add sharp
```

**Step 2: Improve Pagefind Loading Logic**

```js
// NavBar.astro
async function loadPagefind() {
  try {
    const pagefind = await import("/pagefind/pagefind.js");
    await pagefind.options({
      excerptLength: 20,
    });
    pagefind.init();
    window.pagefind = pagefind;
    pagefind.search("");
    console.log('Pagefind loaded successfully');
  } catch (error) {
    console.warn('Pagefind not available (likely development mode):', error.message);
    // Dev mode fallback: create a mock object to prevent errors
    window.pagefind = {
      search: async () => ({ results: [] }),
      options: async () => {},
      init: () => {}
    };
  }
}
```

**Validation Results**:

- **Development Mode**: http://localhost:4323/ runs without errors, using the mock search object.
- **Build Mode**: [pagefind] Pagefind indexed 27 pages - index generation is successful.
- **Preview Mode**: http://localhost:4322/ - full search functionality works correctly.

**Technical Summary**

1. **SPA Navigation Compatibility**: In projects using Swup, component logic must be integrated into page transition hooks.
2. **Dependency Management**: Ensure all build-time dependencies, especially image processing libraries like sharp, are correctly installed.
3. **Environment Differences**: Provide appropriate fallback solutions for different environments (dev vs. prod) to prevent errors from halting development.
