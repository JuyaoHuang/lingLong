---
title: "backendDevelopment"
published: 2025-10-01
tags: ['技术改进']
first_level_category: "blog项目"
second_level_category: "backendDevelop"
author: "Alen"
draft: false
---

<div align="right"> <a href="/posts/backendDevelopment"><strong>English</strong></a> | <a href="/posts/后端面板开发">简体中文</a> </div>

# Backend Panel Development

## Functional Requirements

1. Create a URL path in the frontend for an admin login page, but do not display the link in the main UI. Access should only be possible by entering the correct URL.
2. On the login page, send a request to the corresponding backend API endpoint. Compare the provided credentials with the admin account stored in the database (which contains only one table for admin login information).
3. Upon successful login, redirect to an admin interface. This interface will differ from the public view, showing a list of articles with key information (Title, Author, Publication Date, etc., matching the posts.schema defined in yukina\src\content.config.ts), organized by primary and secondary categories. It must include functionality to edit, delete, and create new documents.
4. The "create" function will generate a new .md file in the frontend/posts/ directory. The content is written by the backend and then pushed to the frontend's source tree.
5. The "edit" and "delete" functions: When an article is clicked, the backend requests the full content of that article. The frontend receives and displays this full content (including the article's ID for subsequent operations). After editing or deleting, the updated article data is sent to the frontend, which then overwrites or deletes the article file corresponding to that ID.

------



### Engineering Translation

1. **Hidden Admin Entrypoint**: Create a hidden URL path without a visible login link in the UI.
2. **Authentication**: Use **JWT Authentication**, validating credentials against a user table in a SQLite database.
3. **Protected Article Management Interface**: After login, display an article list organized by secondary categories, with support for Edit/Delete/New actions.
4. **Article CRUD Operations**: Directly manipulate .md files within the yukina\src\contents\posts directory.
5. **Automatic Rebuild**: After any article operation, automatically trigger pnpm run build to rebuild the frontend.

## Backend Architecture

### Core Architectural Principles

1. **Layered Architecture**:
   - **Routing Layer (api)**: Defines API endpoints and handles HTTP requests/responses.
   - **Service Layer (Services)**: Implements core business logic (e.g., file operations).
   - **Data Access Layer (Data)**: Interacts with the database.
   - **Schema Layer (Schemas)**: Defines data structures.
2. **Dependency Injection**:
   - Deeply leverage FastAPI's dependency injection system to manage database sessions, get the current logged-in user, etc., which promotes decoupling and testability.
3. **Configuration-Driven**:
   - All sensitive information (Database URL, JWT secret key) and environment-specific configurations (Astro project path) will be managed via configuration files or environment variables, never hard-coded.
4. **API Contract First**:
   - Use Pydantic models to precisely define all API inputs and outputs. This provides automatic data validation and documentation generation, forming a clear "data contract" between the frontend and backend.

### Project Structure

```bash
    /webTest/
├── /backend/                  <-- FastAPI Project
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            // FastAPI application entrypoint
│   │   ├── core/              // Core configuration and security
│   │   │   ├── config.py      // Application configuration (env vars)
│   │   │   └── security.py    // Password hashing, JWT creation/validation
│   │   ├── data/              // Database-related
│   │   │   ├── database.py    // Database engine and session management
│   │   │   └── models.py      // SQLAlchemy data models (User table)
│   │   ├── api/           	   // API routing layer
│   │   │   ├── auth.py        // Authentication routes (/token)
│   │   │   └── posts.py       // Post management routes (/api/admin/posts)
│   │   ├── schemas/           // Pydantic data contract layer
│   │   │   ├── post.py        // Pydantic models related to Posts
│   │   │   └── user.py        // Pydantic models related to Users
│   │   └── services/          // Business logic layer
│   │       ├── post_service.py// Core file operation logic
│   │       └── user_service.py// User authentication business logic
│   ├── .env                   // Environment variables file
│   ├── Dockerfile             #  Recipe for building the image
│   ├── docker-compose.yml     #  Launcher for local development
│   └── requirements.txt       # Python dependency list
│
└── /yukina/                 <-- Astro Project
    ├── src/
    │   ├── content/
    │   │   └── posts/          <-- [Main target for backend operations]
    │   └── ...
    └── ...
  
```

### Implementation Strategy

**1. & 2. Admin Login & Authentication**

The core of this feature is **Authentication**: confirming "who you are."

- **Database (data/models.py)**: Define a User SQLAlchemy model with at least id, username, and hashed_password fields.
  **Note: Only hashed passwords should be stored in the database.**
- **Security Layer (core/security.py)**:
  - Provide verify_password() and get_password_hash() functions (using passlib).
  - Provide create_access_token() and a core get_current_user() FastAPI dependency. This dependency is responsible for decoding and validating the JWT from the Authorization header.
- **Service Layer (services/user_service.py)**:
  - Implement an authenticate_user(db, username, password) function. It will look up the user in the database and, if found, call verify_password() to compare passwords.
- **Routing Layer (api/auth.py)**:
  - Create a POST /token endpoint.
  - It should accept form data in OAuth2PasswordRequestForm format (username and password).
  - Call user_service.authenticate_user() for validation.
  - On success, call security.create_access_token() to generate a JWT and return it to the frontend.
  - On failure, return an HTTP 401 Unauthorized error.

**3. Fetching the Protected Post List After Login**

​	The core of this feature is **Authorization**: confirming "what you are allowed to do."

- **Configuration (core/config.py)**: Define an ASTRO_CONTENT_PATH variable pointing to the absolute path of yukina\src\contents\posts.
- **Schema Layer (schemas/post.py)**:
  - Create a PostMetadata Pydantic model whose fields **must strictly match** the posts.schema defined in the frontend's content/config.ts (e.g., title, author, pubDate, tags). This is the data contract.
- **Service Layer (services/post_service.py)**:
  - Implement a `get_all_posts_metadata()`function. It will iterate through all .md files in the `ASTRO_CONTENT_PATH`, use the `python-frontmatter` library to **read only the metadata (Frontmatter)** from each file, and then parse this metadata into a list of PostMetadata objects.
- **Routing Layer (api/posts.py)**:
  - Create a `GET /api/admin/posts endpoint`.
  - **Crucially**: Add the Depends(security.get_current_user) dependency to this endpoint. This ensures that only requests with a valid JWT can access it.
  - The endpoint will internally call `post_service.get_all_posts_metadata() `and return the result.

**4. & 5. Article Create, Read, Update, Delete (CRUD)**

​	**This is the core business logic of the backend,** operating directly on the file system.

​	The backend directly creates, modifies, or deletes .md files on the server's file system (i.e., in the yukina\src\contents\posts directory). 

​	These files are the source code for the Astro project. After an operation is complete, the backend triggers a command to tell Astro to **rebuild (pnpm run build)** the entire static site, making the changes live.

- **Schema Layer** (schemas/post.py):

  - `PostCreate`: Defines the data structure the frontend must send to create a new post (e.g., title, tags, content).
  - `PostFull`: Defines the structure for a complete post, including all metadata and content, used for editing.

- **Service Layer** (services/post_service.py):

  - `create_post(post_data: PostCreate)`:
    1. Generate a URL-friendly slug from the title.
    2. Concatenate the Markdown string (Frontmatter + --- + content).
    3. Write the string to a new {slug}.md file in the `ASTRO_CONTENT_PATH`.
    4. Call the `trigger_astro_rebuild()` function.
  - `get_post_by_slug(slug)`:
    - Read the {slug}.md file, parse its contents, and return a PostFull object.
  - `update_post(slug, post_data)`:
    - Similar logic to create_post, but it overwrites an existing file.
  - `delete_post(slug)`:
    - Use `os.remove()` to delete the {slug}.md file, then call `trigger_astro_rebuild()`.
  - `trigger_astro_rebuild()`: Internally uses Python's subprocess module to execute the pnpm run build command in the ../yukina/ directory. **This is the key to automation.**

- **Routing Layer** (api/posts.py):

  - POST /api/admin/posts: 

    ​	Receives PostCreate data, calls `post_service.create_post(). `Protected by JWT.

  - GET /api/admin/posts/{slug}: 

    ​	Calls post_service.get_post_by_slug(). Protected by JWT.

  - PUT /api/admin/posts/{slug}: 

    ​	Receives PostCreate data, calls post_service.update_post(). Protected by JWT.

  - DELETE /api/admin/posts/{slug}: 

    ​	Calls `post_service.delete_post().` Protected by JWT.

### Data Flow & Responsibilities

1. **Startup**: The FastAPI application starts, loading all routes and configurations.

2. **Login**:

   ```
   Frontend POST /token -> api.auth -> services.user validates -> core.security generates JWT -> Returns to Frontend.
   ```

3. **Protected Request**:

   ```
   Frontend requests GET /api/admin/posts with JWT -> core.security.get_current_user validates JWT -> api.posts -> services.post reads file metadata -> Returns to Frontend.
   ```

4. **Write Operation**:

   ```
   Frontend POST /api/admin/posts with post data -> core.security validates JWT -> api.posts receives data -> services.post creates .md file -> services.post triggers pnpm run build -> Returns success response to Frontend.
   ```

## Backend Environment Setup

### Preamble

​	The complete backend and frontend are intended to be packaged and deployed together on a Raspberry Pi 4B (Linux ARM64 system). Therefore, Docker must be used to accomplish the following:

1. Write code in VS Code on a PC (local development).
2. Ultimately deploy to the Raspberry Pi 4B.

**Solution**:
	Use Docker's **Multi-platform Builds** feature to develop on an x86 PC and build a Docker image that runs natively on the ARM-based Raspberry Pi. You only need to write code on your PC; Docker handles all environment consistency issues.

#### Core Philosophy: Build Once, Run Anywhere

​	The goal is to create a self-contained, portable backend application package (a Docker image). This package includes the FastAPI application, all Python dependencies, and a standardized runtime environment.

- **PC (Development Environment)**:
  - Use Docker Compose to launch the environment.
  - Crucially, **mount** the source code directory from the PC into the Docker container. This allows you to modify code in your editor (like VS Code), and the FastAPI service inside the container will **hot-reload** in real-time to reflect the changes.
- **Raspberry Pi (Production Environment)**:
  - Do not copy the code to the Raspberry Pi. Instead, pull the Docker image—which has been **cross-compiled** on the PC for the Raspberry Pi's ARM architecture—from an image repository (like Docker Hub) and run it directly.

### Project Structure Setup

​	The project structure is as described in the "Backend Architecture => Project Structure" section.
​	All backend code will be written in the backend/app/ directory.

### Writing Docker Environment Definition Files

*The project's integrated Dockerfile architecture will be detailed later during the discussion of integrated deployment, which will partially cover the backend's Dockerfile and .yml files.*

- Dockerfile: Defines how to build the application's runtime environment from scratch. --- *Used for standalone backend development; will be used as a child file during integration.*

  ```dockerfile
  # Select an official, multi-platform Python base image
  # python:3.11-slim-bookworm is an excellent choice, available for both amd64(PC) and arm64(Pi)
  FROM python:3.11-slim-bookworm
  
  # Set the working directory inside the container
  WORKDIR /code
  
  # Set a faster PIP source (optional)
  RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
  
  # Copy the requirements file and install dependencies
  # This step is separated to leverage Docker's layer caching; no re-installation unless requirements.txt changes
  COPY ./requirements.txt /code/requirements.txt
  RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
  
  # Copy all application source code to the working directory
  COPY ./app /code/app
  
  # Expose the port the FastAPI application runs on (usually 8000)
  EXPOSE 8000
  
  # Define the command to run when the container starts
  # Use uvicorn to start the app. --host 0.0.0.0 makes it accessible from outside.
  CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
    
  ```

- docker-compose.yml: Enables one-click startup and management of the development environment on the PC.

  ```yml
      version: '3.8'
  services:
    backend:
      # Tell Docker Compose to use the Dockerfile in the current directory
      build: .
      # Name the container for easier management
      container_name: blog_backend_dev
      # Port mapping: Map port 8000 on the PC to port 8000 in the container
      ports:
        - "8000:8000"
      # Volume mounting
      # Sync the ./app directory on the PC with the /code/app directory in the container in real-time
      volumes:
        - ./app:/code/app
        - ./data:/code/data
      # Override the Dockerfile's CMD to enable hot-reloading with --reload
      command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    
  ```

### Local Development Workflow (on PC)

1. **Initialization**:
   - In the backend/ directory, create requirements.txt and add fastapi and uvicorn[standard].
   - In the backend/app/ directory, create a minimal main.py for testing.
2. **Start Development Environment**:
   - Open a terminal on your PC, cd into the backend directory.
   - Run the command: docker-compose up --build
   - Docker will:
     a. Build a local development image based on the Dockerfile.
     b. Start a container based on docker-compose.yml.
     c. Mount the app directory and start FastAPI in hot-reloading mode.
3. **Start Coding**:
   - You can now **open the /webTest/backend/app/ directory on your PC with any editor** and start writing your FastAPI code.
   - Every time you save a file, uvicorn running in the terminal will detect the change and reload the service.
   - You can test your API by visiting http://localhost:8000 in your browser.

## Backend Build Action List (TODO List)

### Phase 0: Environment Setup & Validation ---- Completed ✅

**1. Install Docker Desktop**

**2. Create Project Directory Structure**:

- Create a main project folder, e.g., webTest.
- Create backend and frontend subfolders within it.

**3. Initialize backend Directory**:

- Navigate into the backend directory.

- Create a Dockerfile, reusing the code from before.

- Create a docker-compose.yml file, reusing the code from before.

- Create a requirements.txt file and populate it:

  ```
  fastapi
  uvicorn[standard]
  python-jose[cryptography]
  passlib[bcrypt]
  pydantic-settings
  sqlalchemy
  python-frontmatter
  # Add psycopg2-binary if connecting to PostgreSQL
    
  ```

**4. Create Minimal App and First Launch**:

- Create an app folder inside the backend directory.

- Inside app, create a main.py file with a simple "Hello World" app:

  ```
  from fastapi import FastAPI
  app = FastAPI()
  @app.get("/")
  def root():
      return {"message": "Backend is running!"}
    
  ```

- Open a terminal in VS Code, cd to the backend directory, and run docker-compose up --build.

- **Validation**: Open a browser and navigate to http://localhost:8000. If you see {"message":"Backend is running!"}, your development environment is set up successfully. Stop the service with Ctrl+C.

### Phase 1: Build Application Skeleton ✅

**1. Set up Directory Structure**: In backend/app/, create the following folders and empty __init__.py files for a clear, modular structure:

```
    app/
├── core/
│   └── __init__.py
├── data/
│   └── __init__.py
├── api/
│   └── __init__.py
├── schemas/
│   └── __init__.py
└── services/
    └── __init__.py
  
```

**2. Core Configuration (app/core/config.py)**:

​	Create this file. Use Pydantic Settings to define your application configuration, including JWT secret key, algorithm, expiration time, and, most importantly, the **absolute path to the Astro content directory**.

**3. Database Setup (app/data/)**:

**Note**: The table has been created manually and is located at webTest\backend\data\dataBase.db. The schema is:

```sqlite
CREATE TABLE users (
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, -- Primary Key
username TEXT NOT NULL UNIQUE,                 -- Unique username
hashed_password TEXT NOT NULL
)
```

- In database.py, set up the SQLAlchemy database engine and session management (get_db dependency).
- In models.py, define the User model, including id, username, and hashed_password fields.
- **Pro-Tip**: You can write a small script or manually create an admin user and store their hashed password in the database upon first run.

### Phase 2: Implement Core Services ✅

**1. Security & Authentication Service (app/core/security.py)**:

- Implement password hashing and verification functions (get_password_hash, verify_password).
- Implement the JWT creation function (create_access_token).
- Implement the core get_current_user FastAPI dependency, which will decode the JWT and fetch the user from the database.

**2. User Service (app/services/user_service.py)**:

- Create the authenticate_user(db, username, password) function. This will be the core logic for the login endpoint, calling the database and security services to validate credentials.

**3. Post Service (app/services/post_service.py)**:

- Implement get_all_posts_metadata(): Iterate through the file directory, reading and returning only the Frontmatter of all posts.
- Implement get_post_by_slug(slug): Read and return the full content of a single post.
- Implement create_post(post_data): Concatenate the string and create a new .md file.
- Implement update_post(slug, post_data): Overwrite an existing .md file.
- Implement delete_post(slug): Delete the specified .md file.
- Implement trigger_astro_rebuild(): Use the subprocess module to execute the npm run build command. **Ensure this function is called after successful create, update, and delete operations.**

### Phase 3: Expose API Endpoints ✅

**1. Define Data Contracts (app/schemas/)**:

- Create post.py and user.py.
- Define all Pydantic models for API interaction, such as PostMetadata, PostCreate, PostFull, Token, and User.

**2. Authentication Routes (app/api/auth.py)**:

- Create the POST /token endpoint.
- It should not be protected by JWT.
- Call user_service.authenticate_user for validation and return a token generated by create_access_token on success.

**3. Post Management Routes (app/api/posts.py)**:

- Create GET /api/admin/posts
- Create POST /api/admin/posts
- Create GET /api/admin/posts/{slug}
- Create PUT /api/admin/posts/{slug}
- Create DELETE /api/admin/posts/{slug}
- **Crucially**: Add the Depends(get_current_user) dependency to **all** these endpoints to ensure they are protected.

**4. Assemble the Application (app/main.py)**:

- Clear the "Hello World" code from main.py.
- Create the main FastAPI application instance.
- Use app.include_router() to include the routers defined in auth.py and posts.py.
- Configure CORS middleware to allow access from your frontend domain.

------



### Phase 4: Integration & Validation ✅

**1. Restart Development Environment**: In a VS Code terminal, run docker-compose up. Your complete backend application should now be running.

**2. Unit Testing (with Swagger UI)**:

- Open a browser and navigate to http://localhost:8000/docs.
- **Test Authentication**: Use the /token endpoint with your admin credentials to obtain a JWT.
- **Test Protection**: Attempt to access GET /api/admin/posts without authorization; you should receive a 40x error.
- **Test Full Flow**: Click the "Authorize" button in the top right, paste the JWT, and then test each of the post management endpoints to ensure they work as expected.

**3. Frontend-Backend Integration**:

- You can now start writing the frontend's services layer code to have the admin panel make real calls to the backend APIs you've just validated.

## Bugs Log

### Rendering Glitches in Dev Mode ----- IMPORTANT ⚠️

#### Problem Description

​	After successfully building the admin panel with Svelte and enabling real-time modification/addition/deletion of .md files, a problem emerged: **in dev mode, any modification, addition, or deletion of an article causes the page to suffer a rendering glitch.**

#### Cause -- Cross-Process FS Event Storm

​	This is a **Cross-Process File System Event Storm**, a very subtle "cross-process race condition" found in advanced development environments.

​	Imagine the **Astro Dev Server (Node.js/Vite)** and the **FastAPI Backend (Python)** as two highly efficient teams that speak different languages and work at different paces, both staring at the same whiteboard (the file system).

1. **Astro Dev Server Team**:
   - This team reacts extremely quickly and communicates internally with high efficiency (based on the Node.js event loop).
   - They use an ultra-sensitive surveillance camera (the file watcher, chokidar) to monitor the whiteboard.
   - The slightest change on the whiteboard—even erasing a single dot—is instantly captured by the camera, which notifies the entire team (the HMR system) to respond. The team maintains complex caches and states to ensure lightning-fast responses.
2. **FastAPI Backend Team**:
   - This team works in another room. When they need to modify the whiteboard, they send a person (the Python process) to run over and make changes directly (create, modify, delete files).

**The conflict point is here:**
	The file operations performed by the Python process generate "notifications" (FS Events) at the OS level that, to Astro's highly sensitive camera, can appear as "brute-force," non-standard signals.

- **Event Storm**:
  - A simple os.remove might trigger multiple file system events at a low level, or the order and timing of these events might differ from what Astro expects (e.g., from an event generated by saving a file in VS Code).
- **Cache Race Condition**:
  - When Astro's camera detects this "brute-force signal," it immediately commands the team to read the latest state of the whiteboard. However, the Python process might not have fully "left the scene," or the OS might not have fully synchronized the file's metadata. This can cause the Astro team to read an **intermediate** or **corrupted** state.
- **Internal State Collapse**:
  - The Astro team then updates its internal cache and dependency graph based on this faulty information, causing its internal logic to collapse completely. At this point, whether the browser receives an HMR push or is manually refreshed, it receives "deranged" page data from this confused brain, leading to a rendering glitch.

​	**This is why even the simplest delete operation causes it to crash**. The problem isn't the operation itself, but the fact that the operation was initiated by an "outsider" (the Python process).

#### Solution

1. **Atomic Deployment**

   ​	The professional solution is to ensure that the deployment action (i.e., replacing old files with new ones) is **atomic**—meaning it must complete in a single, indivisible moment, with no intermediate states.

   ​	Upgrade the trigger_astro_rebuild() function in backend\app\services\post_service.py to adopt a simple yet highly effective "**build to a temporary directory, then instantly replace**" strategy.

2. **Make External Modifications "Friendlier"**

   ​	Since we cannot change the core mechanism of the Astro Dev Server, we need to make the backend's write operations as "atomic" and "clean" as possible to minimize interference with the file watcher.

   ​	Make a small but crucial upgrade to the backend's **file-writing logic**: **write to a temporary file first, then rename it**. The os.rename operation is an **atomic operation** for most operating systems.

   ​	This means the file watcher will only see a single, instantaneous "file appeared" event, not a continuous "file is being written" process.

   ​	Modify `update_post` and `create_post` in `backend\app\services\post_service.py` to use the `os.rename `operation.

   ​	With this change, Astro's file watcher will no longer observe the process of "a file being slowly written." It will only see a single, complete event at the instant `os.rename or os.replace` completes:

   - For create_post: a brand new, fully-formed .md file suddenly "appears."
   - For update_post: the content of an existing .md file suddenly "changes."

   ​	This clean, decisive event can be handled more reliably by the Astro Dev Server, significantly reducing the probability of its internal state becoming corrupted and thus solving the rendering glitch issue.

#### Production Mode Workflow: Clear, Linear, No Conflicts

​	In production mode (i.e., when deployed on a Raspberry Pi/server), the entire process is **unidirectional, deterministic, and free of race conditions**. There is no "hot module replacement," no "file watcher," only a clear objective: **generate a new set of static site files and replace the old ones**.

​	When "Publish," "Update," or "Delete" is clicked in the admin panel, the following sequence of events occurs:

1. **[Frontend] Send Instruction**:
   - The Svelte admin interface sends an API request to the FastAPI backend (e.g., POST /api/admin/posts).
2. **[Backend] Execute File Operation**:
   - FastAPI receives the request and calls a function in post_service.py.
   - The create_post, update_post, or delete_post function **directly and safely** creates, modifies, or deletes the .md file in the yukina/src/contents/posts/ directory.
   - **Key Point**: At this stage, the **public-facing website is completely unaffected**. **Nginx** is still serving the old static files from the dist directory to all visitors. Visitors are unaware of the changes happening in the src directory behind the scenes.
3. **[Backend] Trigger Build Script**:
   - After the file operation succeeds, the code executes the trigger_astro_rebuild() step.
   - The **trigger_astro_rebuild function is called**. It starts an independent pnpm run build process.
4. **[Build Process] Work "Behind the Scenes"**:
   - Astro's build script begins to run. It will:
     a. Read **all** content from the src directory (including the recent changes).
     b. Build all pages in memory.
     c. Output the final, complete, brand-new HTML/CSS/JS/image files to a **specified output directory** (e.g., dist or the optimized dist_new).
   - **Key Point**: During the seconds or tens of seconds that the build command is running, the old dist directory remains online, and the website service is **never interrupted**.
5. **[Deployment] Atomic Replacement**:
   - When pnpm run build finishes successfully, the subsequent part of the trigger_astro_rebuild script executes.
   - In an instant, it uses os.rename to rename the newly built dist_new directory to dist, while backing up the old dist directory as dist_old.
   - **Key Point**: This switch is **atomic**. To Nginx, which is handling requests, the content of the dist directory appears to have been updated instantaneously.
6. **[Complete] New Version is Live**:
   - From the moment the switch is complete, all new requests to the website will be served by Nginx from this brand-new dist directory.
   - Visitors will see the website content including the latest changes.

#### Why No Rendering Glitches in Production Mode❓️

1. **No HMR, No Real-time Watching**:
   - Production mode **does not have** the highly sensitive file watcher and hot module replacement system. Astro only reads all files once when pnpm run build is called. Therefore, there is no race condition between the Python process and the Node.js process regarding file reads/writes.
2. **Read/Write Separation**:
   - The entire process is **write-then-read**. FastAPI first completes all write operations to the src directory, and only then starts an independent build process to read these now-stable files.
3. **Service and Build Separation**:
   - The **Nginx web service and the Astro build process are two completely separate things**. Nginx only cares about the dist directory, while the build process only cares about the src directory and outputting to dist_new. They do not interfere with each other during their work, until the final atomic switch.

**Need to ensure:**

- **Use the atomic trigger_astro_rebuild function**.
  - Use the Python script that "builds to dist_new first, then os.rename." This ensures the site doesn't show a broken page or a 404 for even a second while a user might be visiting during a build.
- **Ensure the settings.ENVIRONMENT variable is correctly set to "production" on the Raspberry Pi**.
  - This can be achieved most flexibly through environment variables.

**Subsequent integration of the frontend and backend proved this to be correct.**

------



### Backend API Login Returns 500 Status Code

**Problem successfully resolved.**

**Problem:**
The backend API returned a 500 Internal Server Error upon login due to a bcrypt version compatibility issue.
The issue was between passlib[bcrypt]==1.7.4 and bcrypt==5.0.0.

**Solution:**

1. Updated requirements.txt to use compatible versions, fixing the bcrypt version conflict:
   - passlib==1.7.4 (without the [bcrypt] extra)
   - bcrypt==4.1.3 (a specific compatible version)
2. Rebuilt the Docker container with the corrected dependencies.
3. Verified that authentication was working via testing:
   - ✅ Login Endpoint: POST /token with admin/admin credentials.
   - ✅ Protected Endpoint: GET /api/admin/posts with a JWT token.
   - ✅ API Documentation: GET /docs was accessible.

## 📋 Summary

### 🏗️ Technical Architecture

Layered Architecture Design:

- Routing Layer (api/): Handles HTTP requests/responses.
- Service Layer (services/): Core business logic (file operations).
- Data Access Layer (data/): Database interaction.
- Schema Layer (schemas/): Pydantic data contracts.

### 📝 Data Structure Contract

Frontend Content Schema (must be strictly matched):

```js
{
title: string,           // Required
published: Date,         // Required
description?: string,
tags?: string[],
first_level_category: string,    // Required, primary category
second_level_category: string,   // Required, secondary category
author?: string,
draft?: boolean,
cover?: string,
sourceLink?: string,
licenseName?: string,
licenseUrl?: string,
readingMetadata?: { time: number, wordCount: number }
}
  
```

### 📝 Database Structure

SQLite Database: webTest\backend\data\dataBase.db

```sql
CREATE TABLE users (
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT NOT NULL UNIQUE,
hashed_password TEXT NOT NULL
);
  
```

### 📝 Environment Configuration

Key Paths:

- Astro Content Directory: D:\Coding\Wrote_Codes\webTest\yukina\src\contents\posts
- Database Path: D:\Coding\Wrote_Codes\webTest\backend\data\dataBase.db
- Rebuild Command: Execute pnpm run build in the ../yukina/ directory.

### 🚀 Deployment Target

Docker Multi-platform Deployment:

- Development Environment: PC (x86) + Docker Compose + Hot-Reloading
- Production Environment: Raspberry Pi 4B (ARM64) + Docker Images

### Core Tech Stack:

- FastAPI + SQLAlchemy + JWT Authentication
- python-frontmatter (for processing Markdown frontmatter)
- Docker + Docker Compose
