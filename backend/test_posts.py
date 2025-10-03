"""
Test script to debug posts API issue
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from pathlib import Path
from app.core.config import settings

def test_posts_reading():
    """Test reading posts with current settings"""
    print("=== Testing Posts Reading ===")
    print(f"ASTRO_CONTENT_PATH: {settings.ASTRO_CONTENT_PATH}")
    print(f"Path exists: {os.path.exists(settings.ASTRO_CONTENT_PATH)}")

    posts_dir = Path(settings.ASTRO_CONTENT_PATH)
    print(f"Posts directory: {posts_dir}")
    print(f"Directory exists: {posts_dir.exists()}")

    md_files = list(posts_dir.glob("*.md"))
    print(f"Found {len(md_files)} markdown files:")
    for f in md_files:
        print(f"  - {f.name}")

    print("\n=== Testing Service Function ===")
    try:
        from app.services.post_service import get_all_posts_metadata
        posts = get_all_posts_metadata()
        print(f"Service returned {len(posts)} posts:")
        for post in posts:
            print(f"  - {post.get('title', 'No title')} (slug: {post.get('slug', 'No slug')})")
    except Exception as e:
        print(f"Error calling service: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_posts_reading()