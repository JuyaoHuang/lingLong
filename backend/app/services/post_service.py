"""
文章管理业务逻辑服务 - Article management business logic service
处理Markdown文件的CRUD操作和Astro项目重新构建 - Handles CRUD operations for Markdown files and Astro project rebuilding
"""
import os
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional
import frontmatter
from datetime import datetime

from ..core.config import settings


def get_all_posts_metadata() -> List[Dict[str, Any]]:
    """
    获取所有文章元数据（不包含正文内容） - Get metadata of all articles (without content body)

    功能说明：
    - 遍历所有markdown文件，仅读取frontmatter元数据
    - 不读取文章正文内容，提高性能，减少内存占用
    - 用于管理面板文章列表显示

    Returns:
        List of article metadata, each element contains frontmatter data and slug

    Note:
        Only reads frontmatter, not content body, for article list display
        Better performance, reduces memory usage
    """
    posts_metadata = []
    posts_dir = Path(settings.ASTRO_CONTENT_PATH)

    # 确保文章目录存在 - Ensure posts directory exists
    if not posts_dir.exists():
        return posts_metadata

    # 遍历所有.md文件 - Iterate through all .md files
    for md_file in posts_dir.glob("*.md"):
        try:
            # 读取文件内容 - Read file content
            with open(md_file, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)

            # 提取slug（文件名，不包含扩展名） - Extract slug (filename without extension)
            slug = md_file.stem

            # Build metadata dictionary with proper date conversion
            metadata = {
                "slug": slug,
                **post.metadata  # Expand all frontmatter data
            }

            # 确保published字段是Date对象 - Ensure published field is Date object
            if 'published' in metadata:
                published = metadata['published']
                if isinstance(published, str):
                    # 如果是字符串，尝试解析为日期
                    try:
                        metadata['published'] = datetime.strptime(published, '%Y-%m-%d').date()
                    except ValueError:
                        # 如果解析失败，使用当前日期
                        metadata['published'] = datetime.now().date()
                elif not isinstance(published, (datetime, type(datetime.now().date()))):
                    # 如果不是日期类型，使用当前日期
                    metadata['published'] = datetime.now().date()

            posts_metadata.append(metadata)

        except Exception as e:
            print(f"Error reading file {md_file}: {e}")
            continue

    # Sort by publication date in descending order (newest first)
    posts_metadata.sort(
        key=lambda x: x.get('published', datetime.min.date()),
        reverse=True
    )

    return posts_metadata


def get_post_by_slug(slug: str) -> Optional[Dict[str, Any]]:
    """
    根据Slug获取单篇文章的完整内容 - Get complete content of a single article by slug

    功能说明：
    - 根据文章的唯一标识符slug获取完整文章数据
    - 包含文章内容和所有frontmatter字段
    - 用于文章编辑和详情显示

    Args:
        slug: Unique identifier of the article (filename without extension)

    Returns:
        Dictionary containing complete article data, or None if file doesn't exist

    Note:
        Returned dictionary contains:
        - slug: Article identifier
        - content: Article body content
        - All frontmatter fields
    """
    posts_dir = Path(settings.ASTRO_CONTENT_PATH)
    md_file = posts_dir / f"{slug}.md"

    # 检查文件是否存在--Check if file exists
    if not md_file.exists():
        return None

    try:
        # 读取文件内容--Read file content
        with open(md_file, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)

        # 通过适当的日期转换构建完整的数据--Build complete data with proper date conversion
        result = {
            "slug": slug,
            "content": post.content,
            **post.metadata
        }

        if 'published' in result:
            published = result['published']
            if isinstance(published, str):
                try:
                    result['published'] = datetime.strptime(published, '%Y-%m-%d').date()
                except ValueError:
                    result['published'] = datetime.now().date()
            elif not isinstance(published, (datetime, type(datetime.now().date()))):
                result['published'] = datetime.now().date()

        return result

    except Exception as e:
        print(f"Error reading article {slug}: {e}")
        return None


def create_post(post_data: Dict[str, Any]) -> bool:
    """
    创建新文章

    参数：
    post_data：文章数据，必须包含标题和内容

    返回值：
    创建成功则返回 True，失败则返回 False

    流程：
        1. 根据标题生成 URL 友好的 slug
        2. 构建完整的 Markdown 内容（frontmatter + 内容）
        3. 写入文件
        4. 触发 Astro 重建
    Create new article

    Args:
        post_data: Article data, must contain title and content

    Returns:
        True if creation successful, False if failed

    Process:
        1. Generate URL-friendly slug from title
        2. Build complete Markdown content (frontmatter + content)
        3. Write to file
        4. Trigger Astro rebuild
    """
    try:
        # 提取必填字段--Extract required fields
        title = post_data.get('title', '').strip()
        content = post_data.get('content', '').strip()

        if not title:
            print("Error: Article title cannot be empty")
            return False

        # 生成 slug（使用标题作为文件名，替换特殊字符）--Generate slug (use title as filename, replace special characters)
        slug = _generate_slug(title)

        # 准备前言数据,过滤掉 None 值以避免 Zod 校验错误--Prepare frontmatter data, filter out None values to avoid Zod validation errors
        frontmatter_data = {k: v for k, v in post_data.items() if k != 'content' and v is not None}

        # 确保发布日期存在且格式正确--Ensure publication date exists and is properly formatted
        if 'published' not in frontmatter_data:
            frontmatter_data['published'] = datetime.now().date()
        else:
            # 将日期转换为前置内容的日期对象(不是字符串)--Convert date to date object for frontmatter (not string!)
            published = frontmatter_data['published']
            if isinstance(published, str):
                try:
                    frontmatter_data['published'] = datetime.strptime(published, '%Y-%m-%d').date()
                except ValueError:
                    frontmatter_data['published'] = datetime.now().date()
            elif hasattr(published, 'strftime'):
                pass
            else:
                frontmatter_data['published'] = datetime.now().date()
        post = frontmatter.Post(content)
        post.metadata = frontmatter_data

        posts_dir = Path(settings.ASTRO_CONTENT_PATH)
        posts_dir.mkdir(parents=True, exist_ok=True)

        md_file = posts_dir / f"{slug}.md"

        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))

        print(f"Article created successfully: {md_file}")

        # 根据环境决定是否触发 Astro rebuild
        if settings.ENVIRONMENT == "production":
            trigger_astro_rebuild()
        else:
            print("Development mode: Astro dev server will auto-detect file changes")

        return True

    except Exception as e:
        print(f"Error creating article: {e}")
        return False


def update_post(slug: str, post_data: Dict[str, Any]) -> bool:
    """
    更新现有文章

    参数：
    slug：文章标识符
    post_data：新文章数据

    返回：
    更新成功返回 True，失败返回 False
    Update existing article

    Args:
        slug: Article identifier
        post_data: New article data

    Returns:
        True if update successful, False if failed
    """
    try:
        posts_dir = Path(settings.ASTRO_CONTENT_PATH)
        md_file = posts_dir / f"{slug}.md"

        if not md_file.exists():
            print(f"Error: Article {slug} does not exist")
            return False

        # 提取内容--Extract content
        content = post_data.get('content', '').strip()
        # 过滤掉 None 值以避免 Zod 校验错误--Filter out None values to avoid Zod validation errors
        frontmatter_data = {k: v for k, v in post_data.items() if k != 'content' and v is not None}

        # 处理前置内容的日期转换--Handle date conversion for frontmatter
        if 'published' in frontmatter_data:
            published = frontmatter_data['published']
            if isinstance(published, str):
                try:
                    frontmatter_data['published'] = datetime.strptime(published, '%Y-%m-%d').date()
                except ValueError:
                    frontmatter_data['published'] = datetime.now().date()
            elif hasattr(published, 'strftime'):
                pass
            else:
                frontmatter_data['published'] = datetime.now().date()

        post = frontmatter.Post(content)
        post.metadata = frontmatter_data

        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))

        print(f"Article updated successfully: {md_file}")

        if settings.ENVIRONMENT == "production":
            trigger_astro_rebuild()
        else:
            print("Development mode: Astro dev server will auto-detect file changes")

        return True

    except Exception as e:
        print(f"Error updating article {slug}: {e}")
        return False


def delete_post(slug: str) -> bool:
    """
    删除文章

    参数：
    slug：文章标识符

    返回值：
    删除成功则返回 True，失败则返回 False
    Delete article

    Args:
        slug: Article identifier

    Returns:
        True if deletion successful, False if failed
    """
    try:
        posts_dir = Path(settings.ASTRO_CONTENT_PATH)
        md_file = posts_dir / f"{slug}.md"

        if not md_file.exists():
            print(f"Error: Article {slug} does not exist")
            return False

        os.remove(md_file)
        print(f"Article deleted successfully: {md_file}")

        if settings.ENVIRONMENT == "production":
            trigger_astro_rebuild()
        else:
            print("Development mode: Astro dev server will auto-detect file changes")

        return True

    except Exception as e:
        print(f"Error deleting article {slug}: {e}")
        return False


def trigger_astro_rebuild():
    """
    触发 Astro 项目重建

    注意：
    在 Astro 项目目录中执行 pnpm run build 命令
    这是使文章更改生效的关键步骤
    Trigger Astro project rebuild

    Note:
        Execute pnpm run build command in Astro project directory
        This is the key step to make article changes take effect
    """
    try:
        astro_project_path = Path(settings.ASTRO_PROJECT_PATH)

        if not astro_project_path.exists():
            print(f"Error: Astro project directory does not exist: {astro_project_path}")
            return False

        print(f"Starting Astro project rebuild: {astro_project_path}")

        # 执行构建命令--Execute build command
        result = subprocess.run(
            ["pnpm", "run", "build"],
            cwd=astro_project_path,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        if result.returncode == 0:
            print("Astro project build successful")
            print("Build output:", result.stdout)
            return True
        else:
            print("Astro project build failed")
            print("Error output:", result.stderr)
            return False

    except subprocess.TimeoutExpired:
        print("Error: Build timeout (exceeded 5 minutes)")
        return False
    except Exception as e:
        print(f"Error triggering build: {e}")
        return False


def _generate_slug(title: str) -> str:
    """
    根据标题生成 URL 友好的 slug
    参数：
        title：文章标题
    返回：
        URL 友好的 slug
    备注：
        保留中文字符，仅替换特殊符号以确保文件名有效
    Generate URL-friendly slug from title

    Args:
        title: Article title

    Returns:
        URL-friendly slug

    Note:
        Keeps Chinese characters, only replaces special symbols to ensure valid filename
    """
    # 删除或替换不适合文件名的字符--Remove or replace characters not suitable for filenames
    invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']

    slug = title
    for char in invalid_chars:
        slug = slug.replace(char, '-')

    # Remove extra whitespace and hyphens
    slug = slug.strip().replace(' ', '-')

    # 删除连续的连字符--Remove consecutive hyphens
    while '--' in slug:
        slug = slug.replace('--', '-')

    # 删除前导连字符和尾随连字符--Remove leading and trailing hyphens
    slug = slug.strip('-')

    return slug or 'untitled'