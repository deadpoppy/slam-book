# 从 SLAM 到空间智能：传统几何、3DGS 与具身智能地图

> **在线阅读：[https://deadpoppy.github.io/slam-book/](https://deadpoppy.github.io/slam-book/)**

一本关于 SLAM（同时定位与地图构建）、3D Gaussian Splatting 与具身智能地图的系统性中文技术书籍。

---

## 📖 书籍简介

本书的核心问题：**当机器人不再满足于"知道自己在哪里"，而是要拥有可定位、可理解、可查询、可规划、可交互、可长期更新的空间记忆时，SLAM 必须变成什么？**

全书共 **6 篇 24 章 + 附录**，涵盖：

| 篇章 | 内容 |
|------|------|
| **导论** | 从 SLAM 到 Spatial AI 的范式转移 |
| **第一篇** | 传统 SLAM 的最小必要知识（滤波、图优化、视觉/激光/语义 SLAM） |
| **第二篇** | 学习增强 SLAM 与神经地图（DROID-SLAM、NeRF-SLAM） |
| **第三篇** | 3D Gaussian Splatting SLAM（2024–2026 主战场） |
| **第四篇** | 视觉几何基础模型与 SLAM 重构（DUSt3R、MASt3R、VGGT） |
| **第五篇** | 开放词汇语义地图与具身智能 |
| **第六篇** | 2026 之后的方向、系统落地与写作框架 |
| **附录** | 核心论文清单、写作模板、技术主线图、10 个关键判断 |

---

## 🌐 在线阅读

**直接点击访问：** 👉 [https://deadpoppy.github.io/slam-book/](https://deadpoppy.github.io/slam-book/)

本站基于 [Mozilla PDF.js](https://github.com/mozilla/pdf.js) 构建，提供：
- 📑 左侧目录/大纲导航（支持 PDF 书签）
- 🔍 全文搜索（Ctrl + F）
- 🔎 缩放、翻页、适应宽度/页面
- 📱 移动端适配
- 🖨️ 打印与下载

---

## 🚀 部署方案演进

本项目尝试了多种将大型 Markdown 书籍部署为静态网站的技术路线：

### 方案一：MkDocs + Material
- 使用 `pymdownx.arithmatex` + MathJax 3 渲染数学公式
- 按章节自动拆分，生成导航侧边栏
- **问题**：MathJax 客户端渲染在中文环境下偶尔不稳定，部分公式显示为原始 LaTeX 代码

### 方案二：md2html 模板
- 基于 [md2html](https://github.com/haidang1810/md2html) 的自包含 HTML 模板
- 每章生成独立 HTML 页面，含深色/浅色模式、滚动进度条
- **问题**：对于 700+ KB、含大量数学公式的书籍，纯 HTML 方案的公式渲染和排版一致性仍难保证

### ✅ 最终方案：PDF.js（当前采用）
- 将 Markdown 导出为 PDF（保留完整排版和公式）
- 使用 Mozilla PDF.js 在浏览器中渲染
- **优点**：排版与纸质书完全一致，公式零失真，支持搜索/缩放/目录
- **部署方式**：将 PDF + PDF.js 静态文件推送至 `gh-pages` 分支

---

## 🛠️ 本地部署与更新

### 更新 PDF 内容

如果你有新的 PDF 文件，替换根目录（或 `pdfjs-site/`）下的 `slam2embody.pdf`，然后重新推送 `gh-pages`：

```bash
# 克隆仓库
git clone https://github.com/deadpoppy/slam-book.git
cd slam-book

# 替换 PDF 文件
cp /path/to/your/new-book.pdf pdfjs-site/slam2embody.pdf

# 重新部署到 gh-pages
cd pdfjs-site
git init
git add .
git commit -m "Update PDF"
git remote add origin git@github.com:deadpoppy/slam-book.git
git push --force origin main:gh-pages
```

### GitHub Pages 设置

本仓库使用 `gh-pages` 分支部署，GitHub Pages 配置如下：
- **Source**: Deploy from a branch → `gh-pages` / `/` (root)
- **Custom domain**: 无（使用默认 `username.github.io/repo-name`）

如需绑定自定义域名，在仓库 **Settings → Pages** 中配置，并在 `pdfjs-site/` 下添加 `CNAME` 文件。

---

## 📁 仓库结构

```
slam-book/
├── README.md                          # 本文件
├── slam_book.agent.final.md           # 原始完整 Markdown 源文件
├── slam-book-site/                    # MkDocs 项目（历史方案）
│   ├── docs/                          # 拆分后的章节 Markdown
│   ├── mkdocs.yml                     # MkDocs 配置
│   └── .github/workflows/ci.yml       # GitHub Actions 自动部署
├── md2html-site/                      # md2html 方案（历史方案）
│   ├── index.html                     # 首页
│   └── slam_book_sec*.html            # 各章节 HTML
├── pdfjs-site/                        # ✅ 当前生产环境
│   ├── index.html                     # 入口页（嵌入 PDF.js viewer）
│   ├── slam2embody.pdf               # 书籍 PDF
│   ├── build/                         # PDF.js 核心库
│   └── web/                           # PDF.js 阅读器界面
└── split_book.py                      # Markdown 自动拆分脚本
```

---

## 📚 原始素材

- **Markdown 源文件**：由作者编写，单文件约 680 KB，7280 行
- **拆分章节**：`/Users/milo/Downloads/Kimi_Agent_SLAM到空间智能/`（25 个章节文件 + outline）
- **PDF 导出**：`slam2embody.pdf`（6.4 MB，纯文字+公式，无图片）

---

## 📝 协议

本书内容由作者原创，本站仅提供阅读载体与技术部署。

---

> **快捷入口**：[🌐 立即在线阅读](https://deadpoppy.github.io/slam-book/)
