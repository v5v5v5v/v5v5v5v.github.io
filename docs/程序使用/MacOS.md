## 终端命令

```bash
// 清屏 快捷键 win + L
clear
// 历史记录
history
```

## 访达指定文件夹

1.   访问指定地址文件夹：导航栏 > 前往 > 前往文件夹，快捷键`CTRL + SHIFT + G`

## 关闭Apple验证

>   打开文件时，会碰到无法验证，丢垃圾桶的情况

1.   打开终端，运行以下代码

     ```bash
     sudo spctl --master-disable
     ```

2.   输入密码，回车

3.   打开**设置** --> **隐私与安全** --> 划到最下面，选择任何来源

4.   如果要重新开启，输入以下代码

     ```bash
     sudo spctl --master-enable
     ```

## xattr的使用(解除DMG文件的隔离)

1.   查看
     ```bash
     xattr 程序名
     ```
2.   删除隔离属性
     ```bash
     xattr -d com.apple.quarantine 程序名
     ```

## alias终端命令

>   常用命令起一个短名字，方便你少打字、少记参数，以下方式**永久生效**

1.   打开终端，查看是否存在`.zshrc`文件

     ```bash
     cat ~/.zshrc
     ```

2.   **未存在**，创建并打开`.zshrc`文件

     ```bash
     // open -e 文件 = 强制用系统自带 TextEdit（文本编辑）打开文件
     touch ~/.zshrc && open -e ~/.zshrc
     ```

3.   编辑简写命令

     ```bash
     alias 别名='原命令' // 如 alias ll='ls -al'
     ```

4.   让命令生效

     ```bash
     source ~/.zshrc
     ```

5.   查看所有的简写命令

     ```bash
     alias
     ```

## DeekSeek-Tui的使用

```bash
常用启动方式

# 默认 TUI（你现在的模式）
codewhale

# 指定工作目录
codewhale --cwd ~/MyXcodeProject

# 一次性提问（非交互）
codewhale exec "这段 SwiftUI 代码怎么优化？"

# MCP stdio 服务（供外部工具调用）
codewhale mcp-server

# HTTP 运行时 API
codewhale app-server --http
```

## 好用的软件

|   名称    |       说明       |
| :-------: | :--------------: |
|   IINA    |   播放视频软件   |
| PlayCover | 在Mac上玩iOS游戏 |
| Snipaste  |     截图软件     |

## Homebrew

### 常用的命令

```bash
# 安装
brew install <包名> 
# 查看
brew list --cask
# 更新
brew upgrade <包名>         # 只升级指定包
# 卸载
brew uninstall --cask <包名> 
# 查看配置（安装路径、缓存路径等）
brew config               
```

### 命令大全

```bash
一、安装与卸载

brew install <包名>        # 安装命令行工具（formula）
brew install --cask <包名>  # 安装 GUI 应用（cask）
brew uninstall <包名>       # 卸载 formula
brew uninstall --cask <包名> # 卸载 cask
brew reinstall <包名>       # 重装（保留配置）

二、查询与搜索

brew search <关键词>        # 搜索可安装的包
brew info <包名>            # 查看包的详细信息（版本、依赖、安装路径等）
brew list                   # 列出所有已安装的 formula
brew list --cask            # 列出所有已安装的 cask
brew list --versions        # 列出已安装包及其版本号
brew deps <包名>            # 查看某个包的依赖
brew uses <包名>            # 查看哪些包依赖了此包（被谁需要）
brew leaves                 # 列出没有被其他包依赖的顶层包（手动安装的）

三、更新与升级

brew update                 # 更新 Homebrew 自身 + 拉取最新包索引
brew upgrade                # 升级所有已安装的包
brew upgrade <包名>         # 只升级指定包
brew outdated               # 查看哪些包有新版本可升级
brew pin <包名>             # 锁定某个包，不随 brew upgrade 升级
brew unpin <包名>           # 解除锁定

────────────────────────────────────────────────────────────

四、清理与维护

brew cleanup                # 清理所有旧版本（保留最新版）
brew cleanup -n             # 预览会清理什么，不实际执行（dry-run）
brew cleanup <包名>         # 只清理指定包的旧版本
brew autoremove             # 删除不再被任何包依赖的孤立依赖
brew doctor                 # 诊断 Homebrew 环境是否有问题

五、服务管理（针对带后台服务的包，如 nginx、mysql、redis）

brew services list          # 查看所有通过 brew 管理的服务状态
brew services start <包名>  # 启动服务
brew services stop <包名>   # 停止服务
brew services restart <包名># 重启服务

────────────────────────────────────────────────────────────

六、仓库与源管理

brew tap <仓库名>           # 添加第三方仓库（如 brew tap leoafarias/fvm）
brew untap <仓库名>         # 移除仓库
brew tap                    # 列出已添加的仓库

────────────────────────────────────────────────────────────

七、自身管理

brew --version              # 查看 Homebrew 版本
brew config                 # 查看 Homebrew 配置（安装路径、缓存路径等）
brew --repo                 # 查看 Homebrew 自身安装路径
```

## 访达显示隐藏文件

快捷键：`Command + Shift + .`（句号）

## 关于本机

1.   M 系列基本选 `arm64`，Intel 系列选 `x64/amd64`
