#!/usr/bin/env python3
"""生成 docs/JS/time-updater-git.js。

原理：Cloudflare Pages 不返回 Last-Modified 响应头，docsify 内置的
{docsify-updated} 占位符无法被替换（GitHub Pages 返回的也只是部署时间，
并不准确）。本脚本用 `git log -1 --format=%cI` 取每个 markdown 文件的
真实最后提交时间，注入到插件 JS 中，两个平台行为一致。

用法：在仓库根目录运行 `python3 scripts/generate-time-updater.py`
（需在 git 仓库内，CI 与本地通用）。
"""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "JS" / "time-updater-git.js"

# 插件运行时逻辑模板；占位符 __UPDATED_MAP_DATA__ 会被替换为 JSON 数据
JS_TEMPLATE = """// 更新时间插件（git 提交时间版）——由 scripts/generate-time-updater.py 自动生成，请勿手改
(function () {
  var updatedMap = window.__UPDATED_MAP__ || __UPDATED_MAP_DATA__;

  function pad(n) { return n < 10 ? '0' + n : '' + n; }

  function formatTime(iso, format) {
    if (!iso) return '';
    var d = new Date(iso);
    if (isNaN(d.getTime())) return '';
    var tokens = {
      YYYY: String(d.getFullYear()),
      MM: pad(d.getMonth() + 1),
      DD: pad(d.getDate()),
      HH: pad(d.getHours()),
      mm: pad(d.getMinutes()),
      ss: pad(d.getSeconds())
    };
    var fmt = format || '{YYYY}/{MM}/{DD}';
    return fmt.replace(/\{([^}]+)\}/g, function (_, key) {
      return tokens[key] !== undefined ? tokens[key] : _;
    });
  }

  function currentMdPath() {
    var hash = window.location.hash || '#/';
    var path = hash.replace(/^#\\//, '');
    path = path.split('?')[0].split('#')[0];
    try { path = decodeURIComponent(path); } catch (e) {}
    if (!path) path = 'README.md';
    if (!/\\.md$/i.test(path)) path += '.md';
    return path;
  }

  function plugin(hook) {
    hook.afterEach(function (html) {
      if (html.indexOf('{docsify-updated}') === -1) return html;
      var cfg = window.$docsify && window.$docsify.timeUpdater;
      var time = formatTime(updatedMap[currentMdPath()], cfg && cfg.formatUpdated);
      return html.replace(/{docsify-updated}/g, time);
    });
  }

  window.$docsify = window.$docsify || {};
  window.$docsify.plugins = (window.$docsify.plugins || []).concat(plugin);
})();
"""


def md_commit_times() -> dict:
    """返回 { 相对 docs/ 的 md 路径: git 最后提交时间(ISO 8601) }"""
    files = subprocess.check_output(
        ["git", "-c", "core.quotepath=false", "ls-files", "docs/"],
        text=True,
    ).splitlines()
    data = {}
    for f in files:
        if not f.endswith(".md"):
            continue
        ts = subprocess.check_output(
            ["git", "log", "-1", "--format=%cI", "--", f], text=True
        ).strip()
        if ts:
            data[f[len("docs/"):]] = ts
    # 兜底：仓库最新提交时间（防止个别文件因 shallow clone 查不到历史）
    if not data:
        latest = subprocess.check_output(
            ["git", "log", "-1", "--format=%cI"], text=True
        ).strip()
        for f in files:
            if f.endswith(".md"):
                data[f[len("docs/"):]] = latest
    return data


def main() -> None:
    data = md_commit_times()
    js = JS_TEMPLATE.replace(
        "__UPDATED_MAP_DATA__", json.dumps(data, ensure_ascii=False, indent=2)
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(js, encoding="utf-8")
    print(f"已生成 {OUT}（{len(data)} 个 markdown 文件）")


if __name__ == "__main__":
    main()
