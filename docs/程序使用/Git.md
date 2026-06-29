## 克隆Github的项目到本地

```bash
// git clone 仓库地址
git clone https://github.com/v5v5v5v/docsify.git
```

## 设置

```bash
// 永久拉取默认使用 rebase，避免分叉报错：
git config --global pull.rebase true
// 用的终端、命令行等不走代理，使用以下设置
git config --global http.proxy http://127.0.0.1:7897
```

## 如何推送到Github

```bash
// 第一次推送
// 初始化
git init
// 添加到暂存区
git add .
// 提交并注释
git commit -m "first commit"
// 仓库地址
git remote add origin <你的GitHub仓库地址>
// 推送到哪个分支  git push git@github.com:TheJavaRookie/docsify.git
git push -u origin main 

// 后续推送
git add .
git commit -m "first commit"
git push
```

## 命令太长了，使用alias

1.    `!` 让 Git 把后面的内容当作 shell 来执行
          
      ```shell
      git config --global alias.tui '!git add 文件地址 && git commit -m "update" && git push'
      ```

1.    `git tui`就可以使用

1.    查看所有alias

      ```bash
      git config --global --get-regexp alias
      ```


## 常用命令

```bash
# 初始化,安装时执行一次就够
git init
# 克隆,克隆下来的包含文件夹(文件夹 == 项目名)
git clone 远程仓库地址
# 添加单个文件到暂存区
git add 文件名
# 添加全部文件到暂存区
git add --all 
# 提交,描述修改了什么
git commit -m 描述信息
# 简化远程仓库
git remote add 自定义名 远程仓库地址
# 查看远程仓库
git remote -v
# 查看远程分支
git branch -a
# 拉取,不包含文件夹(项目名)
git pull 远程仓库地址
# 推送
git push 远程仓库地址
```

