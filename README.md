# 李智鑫 · Zhixin Li — 学术个人主页

面向 GitHub Pages 的中英文学术主页。中文为默认首页，英文页面位于 `english/`，同时保留与参考主页一致的 `chinese/` 路径。

内容整理日期：2026年10月23日。

## 页面内容

- 个人简介、现任职务及研究关键词
- 近期动态、研究方向与参与的科研项目（仅列题目和项目类型）
- 2025年及以后发表的6篇代表论文、论文链接及已有公开代码链接
- 专著《金融科技安全导论》、2025年及以后授权的专利、获奖荣誉、学术服务和教学育人；学术报告暂留空
- 工作邮箱、办公室及 DBLP / ORCID / GitHub 链接

所有页面为静态 HTML，无需数据库、账号、API 密钥或外部前端依赖。页面可以直接在浏览器打开；禁用 JavaScript 后仍可阅读全部内容。年份筛选是可选增强功能。

## 直接查看

在本文件所在文件夹双击 `index.html`。顶部的 English / 中文可以切换语言；也可以直接打开 `english/index.html`。

## 发布到 GitHub Pages

目标账号：`Jack-lizhiXin`。

按 GitHub 用户主页命名规则，新建公开仓库 `jack-lizhixin.github.io`。将本目录中的页面、`assets/`、`chinese/`、`english/` 等文件放到仓库根目录，确保 `index.html` 直接位于根目录，不要额外套一层文件夹。

在仓库 **Settings → Pages → Build and deployment** 中：

1. Source 选择 **Deploy from a branch**。
2. Branch 选择 **main**，目录选择 **/(root)**。
3. 点击 **Save**，等待 Pages 发布完成。

配置完成并发布成功后的预期地址为：

- 中文首页：`https://jack-lizhixin.github.io/`
- 中文路径：`https://jack-lizhixin.github.io/chinese/`
- 英文页面：`https://jack-lizhixin.github.io/english/`

这些是目标地址；本文件不代表仓库已创建或网站已上线。以 GitHub Pages 的实际发布状态为准。

### 可选：命令行发布

若本机已经安装 Git 和 GitHub CLI，并已登录 `Jack-lizhiXin`，可以运行：

```bash
bash scripts/publish_github.sh
```

脚本会核对登录账号、新建上述专用公开仓库并提交本目录中列明的主页文件，再设置 Pages。若同名仓库已存在，脚本停止，避免覆盖已有内容。首次使用 GitHub CLI 时请在自己的终端通过 `gh auth login` 完成 GitHub 登录。

## 后续维护

内容集中保存在两份 JSON 文件：

| 文件 | 用途 |
| --- | --- |
| `content/profile.json` | 中英文简介、动态、研究、任职、奖项、服务、教学和联系方式 |
| `content/publications.json` | 论文标题、作者、年份、出版信息、DOI和公开链接 |
| `assets/zhixin-li.png` | 本人提供的个人照片 |
| `assets/style.css` | 页面样式和手机适配 |
| `assets/site.js` | 论文筛选和当前阅读栏目高亮 |

修改 JSON 后运行以下命令重新生成三个页面和 BibTeX，然后提交更新后的文件：

```bash
python3 scripts/build_site.py
```

也可以直接改 HTML，但下一次运行生成脚本时，HTML会由JSON内容重新生成，因此建议优先修改JSON。

## 内容与来源

基本身份参照 [复旦大学金融科技研究院个人页](https://fintech.fudan.edu.cn/info/1005/1367.htm)，个人照片由本人提供；研究关键词、现任职务、奖项、会议服务和办公室信息采用本人最新确认的材料。英文机构、项目及课程名称为对应中文名称的译法。

论文的完整题名、作者顺序与发表信息通过出版方、作者公开论文和 [DBLP作者页](https://dblp.org/pid/82/7406-3.html) 核对。每篇论文附有 DOI；FedDDIM 的奖项采用本人确认材料。已授权专利仅列2025年及以后授权条目，依据授权公告文本及专利记录列示，均附核对链接。新增《中国工程科学》论文的作者、年份及书目信息依据期刊官网核对。科研项目仅展示题目与项目类型，不包含金额、项目编号、职责、执行状态或任务细节。专著仅列本人指定的《金融科技安全导论》，不补充未核实的作者或出版信息。学术报告条目暂留空。

布局参考黄萱菁老师主页的学术信息组织方式；HTML、CSS和交互代码为本页独立编写，没有复制参考网站源码或照片。个人照片及论文相关内容的权利归原权利人所有。

GitHub Pages 官方说明：[创建个人站点](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)、[配置发布来源](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)。
