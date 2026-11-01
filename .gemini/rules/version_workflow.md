# 版本管理规范 (Version Bump Policy)

当对本项目进行任何修改并准备提交/推送时，必须严格遵守以下规则：

1. **版本号必须递增**：每次页面或逻辑修改、提交及推送时，必须递增 `VERSION` 版本号（默认递增 patch，例如 `v1.0.0` -> `v1.0.1`）。
2. **自动重新编译**：使用 `python3 bump_version.py` 递增版本号并自动触发 `assemble_final_app.py`，确保 `index.html`、`login.html`、`dist/index.html` 以及 `dist/login.html` 均注入最新的版本标签。
3. **保持底部版本一致**：确保首页底部与登录页底部的版本号清晰展示且完全同步。
4. **Git 提交同步**：提交时包含 `VERSION`、`index.html`、`login.html` 及 `dist/` 编译产物。
