/**
 * ⚠️ DEPRECATED - 此文件已弃用，不再使用
 *
 * 原因：后端已改用 Python 直接操作 Markdown 文件
 * 文件位置：backend/app/services/post_service.py
 *
 * 此文件保留作为备用方案和参考，但不参与实际运行。
 * 如果需要恢复 Node.js 方案，可以参考此实现。
 */

import fs from 'fs/promises';
import path from 'path';
import matter from 'gray-matter';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 文章目录路径
const POSTS_DIR = path.resolve(__dirname, '../contents/posts');

/**
 * 原子化创建文章
 * 使用临时文件 + 原子性重命名避免文件监视器冲突
 */
async function createPost(postData) {
    try {
        const { title, content, ...frontmatterData } = postData;

        if (!title || !content) {
            throw new Error('Title and content are required');
        }

        const slug = generateSlug(title);
        const filename = `${slug}.md`;
        const finalPath = path.join(POSTS_DIR, filename);
        const tempPath = path.join(POSTS_DIR, `.${filename}.tmp`);

        await fs.mkdir(POSTS_DIR, { recursive: true });

        try {
            await fs.access(finalPath);
            throw new Error(`Post with slug "${slug}" already exists`);
        } catch (error) {
            // 文件不存在，继续创建
            if (error.code !== 'ENOENT') {
                throw error;
            }
        }

        // 构建完整的frontmatter
        const fullFrontmatter = {
            published: frontmatterData.published || new Date().toISOString().split('T')[0],
            ...frontmatterData
        };

        const fileContent = matter.stringify(content, fullFrontmatter);

        // 原子化写入：先写临时文件，再重命名
        await fs.writeFile(tempPath, fileContent, 'utf8');
        await fs.rename(tempPath, finalPath);

        console.log(`Post created successfully: ${filename}`);
        return { success: true, slug, message: 'Post created successfully' };

    } catch (error) {
        console.error('Error creating post:', error.message);
        return { success: false, error: error.message };
    }
}

/**
 * 原子化更新文章
 */
async function updatePost(slug, postData) {
    try {
        const filename = `${slug}.md`;
        const finalPath = path.join(POSTS_DIR, filename);
        const tempPath = path.join(POSTS_DIR, `.${filename}.tmp`);

        try {
            await fs.access(finalPath);
        } catch (error) {
            if (error.code === 'ENOENT') {
                throw new Error(`Post with slug "${slug}" not found`);
            }
            throw error;
        }

        const { content, ...frontmatterData } = postData;

        // 如果没有提供内容，读取现有内容
        let finalContent = content;
        let finalFrontmatter = frontmatterData;

        if (!content) {
            const existingContent = await fs.readFile(finalPath, 'utf8');
            const parsed = matter(existingContent);
            finalContent = parsed.content;
            finalFrontmatter = { ...parsed.data, ...frontmatterData };
        }

        const fileContent = matter.stringify(finalContent, finalFrontmatter);

        // 原子化写入：先写临时文件，再重命名
        await fs.writeFile(tempPath, fileContent, 'utf8');
        await fs.rename(tempPath, finalPath);

        console.log(`Post updated successfully: ${filename}`);
        return { success: true, slug, message: 'Post updated successfully' };

    } catch (error) {
        console.error('Error updating post:', error.message);
        return { success: false, error: error.message };
    }
}

/**
 * 原子化删除文章
 */
async function deletePost(slug) {
    try {
        const filename = `${slug}.md`;
        const finalPath = path.join(POSTS_DIR, filename);

        try {
            await fs.access(finalPath);
        } catch (error) {
            if (error.code === 'ENOENT') {
                throw new Error(`Post with slug "${slug}" not found`);
            }
            throw error;
        }

        // 删除文件
        await fs.unlink(finalPath);

        console.log(`Post deleted successfully: ${filename}`);
        return { success: true, slug, message: 'Post deleted successfully' };

    } catch (error) {
        console.error('Error deleting post:', error.message);
        return { success: false, error: error.message };
    }
}

/**
 * 生成URL友好的slug
 * 保持与Python版本一致的逻辑
 */
function generateSlug(title) {
    const invalidChars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|'];

    let slug = title;
    for (const char of invalidChars) {
        slug = slug.replace(new RegExp(`\\${char}`, 'g'), '-');
    }

    // 移除多余的空格和连字符
    slug = slug.trim().replace(/\s+/g, '-');

    // 移除连续的连字符
    while (slug.includes('--')) {
        slug = slug.replace(/--/g, '-');
    }

    // 移除首尾连字符
    slug = slug.replace(/^-+|-+$/g, '');

    return slug || 'untitled';
}

/**
 * 命令行接口
 * 接收JSON格式的操作指令
 */
async function main() {
    try {
        const args = process.argv.slice(2);

        if (args.length === 0) {
            throw new Error('No operation specified');
        }

        const operation = args[0];
        const dataArg = args[1];

        if (!dataArg) {
            throw new Error('No data provided');
        }

        const data = JSON.parse(dataArg);
        let result;

        switch (operation) {
            case 'create':
                result = await createPost(data);
                break;
            case 'update':
                if (!data.slug) {
                    throw new Error('Slug is required for update operation');
                }
                result = await updatePost(data.slug, data);
                break;
            case 'delete':
                if (!data.slug) {
                    throw new Error('Slug is required for delete operation');
                }
                result = await deletePost(data.slug);
                break;
            default:
                throw new Error(`Unknown operation: ${operation}`);
        }

        // 输出结果供Python读取
        console.log(JSON.stringify(result));
        process.exit(result.success ? 0 : 1);

    } catch (error) {
        console.error('Script error:', error.message);
        console.log(JSON.stringify({ success: false, error: error.message }));
        process.exit(1);
    }
}

// 只有直接运行时才执行main函数
if (process.argv.length > 2) {
    main();
}

export { createPost, updatePost, deletePost, generateSlug };
