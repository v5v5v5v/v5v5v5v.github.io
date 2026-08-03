// 模拟浏览器环境验证 docs/JS/time-updater-git.js 的替换逻辑
const fs = require('fs');

// ---- mock 浏览器全局 ----
global.window = {
  location: { hash: '#/乱七八糟/测试' },
  $docsify: {
    timeUpdater: { formatUpdated: '{YYYY}年{MM}月{DD}号 {HH}:{mm}:{ss}' },
    plugins: []
  }
};

// 执行插件（IIFE 注册到 window.$docsify.plugins）
const code = fs.readFileSync('docs/JS/time-updater-git.js', 'utf8');
eval(code);

// 取注册的 plugin 函数，注入 mock hook 拿到 afterEach
let afterEach = null;
const plugin = window.$docsify.plugins[0];
plugin({
  afterEach(fn) { afterEach = fn; }
});

if (typeof afterEach !== 'function') {
  console.error('FAIL: afterEach 未注册');
  process.exit(1);
}

const cases = [
  { hash: '#/乱七八糟/测试', expect: '2026年08月03号 20:11:25', desc: '中文路径普通页' },
  { hash: '#/', expect: '2026年06月16号 19:09:38', desc: '首页 README' },
  { hash: '#/图片笔记/小区&商场%20-%20地图', expect: '2026年07月08号 17:30:42', desc: '特殊字符路径(需解码)' },
  { hash: '#/不存在的页面', expect: '', desc: '未知页面(占位符清空)' },
  { hash: '#/程序使用/Git', expect: '2026年06月29号 22:59:54', desc: 'Git 页面' }
];

let pass = 0;
for (const c of cases) {
  window.location.hash = c.hash;
  const html = '正文内容\n\n<div align="center">更新时间: {docsify-updated}</div>';
  const out = afterEach(html);
  const ok = out.includes(`更新时间: ${c.expect}`);
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${c.desc}  (${c.hash}) -> ${out.includes('更新时间:') ? out.split('更新时间: ')[1].split('<')[0] : '未替换'}`);
  if (ok) pass++;
}
console.log(`\n结果: ${pass}/${cases.length} 通过`);
process.exit(pass === cases.length ? 0 : 1);
