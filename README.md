# Snoopy’s Little Lab

一个带有任务、会议预约、时区协同、便签、快捷链接和每日英语的私人工作台。

## 启动临时公网地址

双击 `启动网页穿透.command`，或在终端运行：

```bash
python3 serve_tunnel.py
```

程序会启动仅监听本机的服务，并通过 Cloudflare Quick Tunnel 输出一个临时
`https://....trycloudflare.com` 地址。每次重新启动后，临时地址可能变化。

常驻运行时，后端和隧道是两个独立服务。修改页面或重启后端不会中断隧道，
所以临时地址会尽量保持不变；只有隧道进程退出、电脑重启或 Cloudflare 主动断开时才会变化。

首次启动会自动生成高强度登录密码，保存在仅本机可读且不会提交到 Git 的：

```text
data/initial_login.txt
```

保存密码后可以删除这个文件。登录会话有效期为 12 小时，重新启动服务后需要重新登录。

## 修改登录密码

登录后点击首页右上角的 `Sanyli` 头像，在个人信息菜单中选择“密码管理”，即可直接修改。
新密码可以设置为正好 6 位纯数字，也可以使用至少 10 个字符的强密码。

也可以在本机终端运行：

```bash
python3 manage_password.py
```

修改后重新启动服务。也可以在启动前设置 `PLATFORM_PASSWORD` 环境变量；环境变量密码会优先于本地密码配置。

## 版本管理与构建

每次对页面进行修改并准备推送时，需递增版本号：

```bash
# 递增 patch 版本 (如 v1.0.0 -> v1.0.1) 并自动编译更新 index.html、login.html 和 dist/
python3 bump_version.py

# 也可以显式指定递增级别：
python3 bump_version.py patch   # v1.0.0 -> v1.0.1
python3 bump_version.py minor   # v1.0.0 -> v1.1.0
python3 bump_version.py major   # v1.0.0 -> v2.0.0
python3 bump_version.py 1.2.0   # 指定特定版本号

# 查看当前版本号
python3 bump_version.py --current
```

手动全量构建：

```bash
python3 assemble_final_app.py
```

`assemble_final_app.py` 会自动读取根目录 `VERSION` 并注入到主页面及登录页面底部，同时自动同步最新产物至 `dist/` 目录。

`auto_compiler.py` 会监听 `VERSION` 与生成源并自动更新 `dist`，但不会自动暂存、提交或推送任何 Git 内容。

## 数据与安全

- SQLite 数据库位于 `data/work_platform.db`，不会提交到 Git。
- 登录密码只保存 PBKDF2 哈希，不会写入网页或 Git。
- 数据库写入前最多每 6 小时自动备份一次，保留最近 10 份，位于 `data/backups/`。
- 数据接口要求登录，并限制为同源请求和 `snoopy_` 前缀的数据键。
- 多设备同时修改同一项数据时，服务端会检测版本冲突，避免静默覆盖。
- Cloudflare 临时地址适合临时个人使用。长期使用独立域名时，建议再配置 Cloudflare Access、固定 Tunnel 和访问策略。

## 测试

```bash
PYTHONPYCACHEPREFIX=/tmp/chifandahu-pycache python3 -m py_compile \
  backend_server.py serve_tunnel.py auto_compiler.py assemble_final_app.py manage_password.py

python3 scratch/test_round18_all_features.py
python3 scratch/test_english_round16_features.py
```

部分旧测试包含固定日期或旧版文案断言，不能作为当前版本的稳定回归标准。
