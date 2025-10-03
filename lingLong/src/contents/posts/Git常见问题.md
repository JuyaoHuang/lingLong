---
title: "Git常见问题"
published: 2025-10-03
tags: ['git']
first_level_category: "编程"
second_level_category: "Git"
author: "Alen"
draft: false
---

# Git常见问题

## C1--分支无共同git历史

### Q1: entirely different commit histories 

​	原仓库没有dev分支，在原仓库创建Pull request只能提交B仓库的main分支，但是修改的代码都在B仓库的dev分支。将B仓库的dev分支pull request到原仓库的main分支会出现上面的错误

**核心问题：** 正如 GitHub 错误信息所说，fork 的仓库 **origin_fork** 的 dev 分支，和原仓库 **origin** 的 main 分支，**没有任何共同的 Git 历史**。

**用一个比喻来解释这个问题**

- 正确的流程（共享历史）：

  ​	你拿到一本书（git clone），翻到第 50 页，在上面做了笔记和修改（git commit），然后把这一页撕下来给原作者，说：“请把我的修改更新到你的书里”。原作者能清晰地看到你是在他第 50 页的基础上做的修改，所以他可以比较和合并。

- 你现在的情况（不同历史）：

  ​	你自己从一张白纸开始，写了一本全新的书（git init），只是这本书的内容恰好和原作者的书很像。现在你把你这本书的第 50 页撕下来给原作者，说：“请把我的修改更新到你的书里”。原作者会彻底困惑，因为你这一页的“历史”和他书里的任何一页都对不上。他无法进行比较，因为你们没有一个共同的起点。

这就是 GitHub 报错 entirely different commit histories 的原因。

#### 解决方案：将代码“移植”到拥有正确历史的分支上

1. 在电脑上创建一新的文件夹 A

2. 克隆原仓库 origin ----- **新的本地仓库叫做 local_repo**

3. **现在这个仓库有了一个正确的 git历史**

4. cd origin 后，创建一个新的分支 dev

   ```bash
   git checkout -b dev
   ```

5. 此时，dev 分支的代码和 **orgin** 仓库的 main 分支代码一样

6. 接下来，从原先 fork的仓库 **origin_fork** 的 dev分支获取已经提交（原本就要提交给 **origin**仓库）的代码

7. 先将 **orgin_fork**作为另一个上游仓库

   ```bash
   git remote add my_fork <你的 origin_fork 仓库的 URL>
   ```

8. 从新的远程地址下载仓库的代码，**但不合并**

   ```bash
   git fetch my_fork
   ```

9. 将当前文件夹里的所有文件，使用 my_fork 这个远程仓库的 dev分支里的文件覆盖

   ```bash
   git checkout my_fork/dev -- .
   ```

   " . "代表当前目录

10. **现在新的本地仓库 local_repo有了完整的git历史和正确的代码**

11. 创建一个新的、干净的提交

    ```bash
    git add .
    git commit -m "your commmit"
    ```

12. 推送到 fork的远程仓库**origin_fokr**

    ```bash
    git push --force my_fork dev
    ```

    - **警告**：这会**永久覆盖** B 仓库 dev 分支之前的历史

13. 建立 Pull request

------

**如果你不想覆盖掉原来的远程仓库 origi_fork的 dev分支（保留着你要 pull的代码）**，那么在**第 12.步**：

```bash
git push --force my_fork dev:other_dev
```

这会在 **origin_fork** 仓库新建一个 other_dev分支，将你的代码推送到此处

## C2--分支合并

### Q1:常规合并

1. 更新要合并的分支，保证分支都是最新的

   ```bash
   git checkout main
   git pull origin main
   
   git checkout dev
   git pull origin dev
   ```

2. 检查 dev分支是否存在潜在冲突

   - 为了确保最终合并到 main 分支时绝对不会有任何冲突，一个专业的做法是**先将 main 分支的最新更改合并到 dev 分支**。

   - 在 dev分支上运行

     ```bash
     git merge main
     ```

   - 分析结果：

     - 如果没有任何输出或提示 "Already up to date."  => dev 分支已经包含了 main 的所有历史，最终合并时将会非常顺畅。
     - 如果出现了合并冲突 (Merge Conflicts)  =>这意味着在 dev 分支这个“工作区”里发现了问题。

3. 如果没有合并冲突，执行

   ```bash
   git checkout main
   git merge dev
   ```

   进行合并

4. 推送到上游仓库（可选）

   ```bash
   git push origin main
   ```

### Q2: 不同历史的合并

执行 `git merge master`时报错:

```bash
fatal: refusing to merge unrelated histories
```

#### 问题根源：两个“独立”的历史提交点

​	本地的 master 分支和 dev 分支，在 Git 看来，是两个**完全不相干**的项目。它们没有一个共同的初始提交点（没有共同的祖先）。

通常发生在以下情况：

1. 在一个分支上 git init 之后，又用 git checkout --orphan <新分支> 创建了一个全新的、无历史的“孤儿”分支。
2. 在不同的文件夹里分别初始化了项目，然后尝试将它们合并。

#### 解决方案：统一历史

如果 dev分支的开发已经完成而且稳定，那么强行让 **master** 分支放弃它自己的历史，完全变成和 **dev** 分支一模一样

即用 dev分支直接覆盖 master分支

1. 切换到 dev分支

   ```
   git checkout dev
   ```

2. 确保 dev与远程仓库同步

   ```bash
   git push origin dev
   ```

3. 切换到 master分支

4. 执行 reset指令

   ```bash
   git reset --hard dev
   ```

   - 忘记 master 分支现在的一切，把 master 的指针，**直接、强行地**移动到 dev 分支当前指向的那个提交上
   - --hard 参数会同时更新工作区的文件，让它们也变得和 dev 分支完全一样。

5. 运行`git log --oneline`检查情况

6. 执行

   ```
   git push origin master:master --force
   ```

   强制推送本地 master分支覆盖远程仓库的 master分支



## C3--删除上游仓库

1. 查看要删除的上游仓库的本地名

   ```bash
   git remote -v
   ```

2. 执行删除命令

   ```bash
   git remote remove upstream_fork
   ```

## C4--默认上游仓库设置

### 好处

​	未来在 master 分支上工作时，可以输入简化的命令，如 git pull 和 git push，而无需每次都指定 origin master。Git 会自动知道你想从 origin/master 拉取，或推送到 origin/master。

------



1. 切换到想要设置的本地分支上

   ```bash
   git checkout master
   ```

2. 执行设置上游的指令

   ```bash
   git branch --set-upstream-to=origin/master
   ```

   - git branch: 这是用于管理分支的命令。
   - --set-upstream-to=origin/master: 这是核心参数，用于建立“跟踪”（tracking）关系。
   - origin：本地给上游仓库名称的重命名
   - master：上游仓库的某个分支名

3. 使用

   ```bash
   git status
   ```

   验证
