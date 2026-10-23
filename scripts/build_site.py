#!/usr/bin/env python3
"""Build the bilingual static homepage with the Python standard library."""
from pathlib import Path
from html import escape
import json
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
PROFILE = json.loads((ROOT / "content/profile.json").read_text(encoding="utf-8"))
PAPERS = json.loads((ROOT / "content/publications.json").read_text(encoding="utf-8"))

LABELS = {
    "zh": {"about": "个人简介", "news": "近期动态", "research": "研究方向", "projects": "科研项目", "publications": "代表论文", "patents": "已授权专利", "honors": "获奖荣誉", "service": "学术服务", "teaching": "教学与育人", "talks": "学术报告", "contact": "联系方式", "email": "电子邮箱", "office": "办公室", "institution": "所在单位", "scholarly": "学术主页", "all": "全部", "earlier": "2024及以前", "skip": "跳至正文", "language": "English", "top": "返回顶部", "official": "研究院个人页", "updated": "更新于", "keywords": "研究关键词", "paper": "论文", "code": "代码", "code_data": "代码与数据", "read": "相关报道", "bibliography": "完整书目见 DBLP", "download_bib": "下载 BibTeX", "filter": "按发表年份筛选论文"},
    "en": {"about": "About", "news": "News", "research": "Research", "projects": "Projects", "publications": "Publications", "patents": "Granted Patents", "honors": "Honors", "service": "Service", "teaching": "Teaching", "talks": "Talks", "contact": "Contact", "email": "Email", "office": "Office", "institution": "Affiliation", "scholarly": "Profiles", "all": "All", "earlier": "2024 & earlier", "skip": "Skip to content", "language": "中文", "top": "Back to top", "official": "Institutional profile", "updated": "Updated", "keywords": "Research interests", "paper": "Paper", "code": "Code", "code_data": "Code & data", "read": "Event report", "bibliography": "Full bibliography on DBLP", "download_bib": "Download BibTeX", "filter": "Filter publications by year"}
}


def esc(value):
    return escape(str(value), quote=True)


def anchor(url, label, extra=""):
    if not (url.startswith(("https://", "mailto:", "#")) or ":" not in url):
        raise ValueError(f"Unsupported URL scheme: {url}")
    return f'<a href="{esc(url)}"{extra}>{esc(label)}</a>'


def section(key, title, content):
    return f'<section class="section" id="{key}" aria-labelledby="heading-{key}"><h2 class="section-heading" id="heading-{key}">{esc(title)}</h2>{content}</section>'


def details(items, labels):
    rows = []
    for item in items:
        year = f'<span class="item-year">{esc(item["year"])}</span>' if item.get("year") else ""
        link = " " + anchor(item["url"], item.get("link_label", labels["read"])) if item.get("url") else ""
        rows.append(f'<li><h3>{year}{esc(item["title"])}</h3><p>{esc(item["text"])}{link}</p></li>')
    return '<ul class="detail-list">' + "\n".join(rows) + '</ul>'


def publications(lang, labels, prefix):
    filters = ''.join(f'<button class="year-filter" type="button" data-year="{year}" aria-pressed="{str(year == "all").lower()}" aria-controls="publication-list">{esc(label)}</button>' for year, label in [("all", labels["all"])] + [(str(year), str(year)) for year in sorted({p["year"] for p in PAPERS}, reverse=True)])
    count = f'显示 {len(PAPERS)} 篇代表论文' if lang == 'zh' else f'{len(PAPERS)} selected publications'
    toolbar = f'<div class="publication-toolbar"><div class="year-filters" role="group" aria-label="{esc(labels["filter"])}">{filters}</div><span id="publication-count" role="status" aria-live="polite" data-zh-template="显示 {{n}} 篇代表论文" data-en-template="{{n}} selected publications">{count}</span></div>'
    rows = []
    for p in PAPERS:
        doi_url = 'https://doi.org/' + p['doi']
        authors = ', '.join(f'<strong>{esc(a)}</strong>' if a == 'Zhixin Li' else esc(a) for a in p['authors'])
        links = [anchor(doi_url, 'DOI')]
        for link in p.get('links', []):
            if link['url'] == doi_url:
                continue
            display = {'Paper': labels['paper'], 'Code': labels['code'], 'Code & data': labels['code_data']}.get(link['label'], link['label'])
            links.append(anchor(link['url'], display))
        topic = p.get('topic_' + lang, '')
        note = f'<span class="pub-award">{esc(p["note_" + lang])}</span>' if p.get('note_' + lang) else ''
        rows.append(f'<li class="publication" data-year="{p["year"]}" id="paper-{esc(p["id"])}"><span class="pub-venue">{esc(p["venue"])}</span><h3 class="pub-title">{anchor(doi_url, p["title"])}</h3><p class="pub-authors">{authors}</p><p class="pub-meta">{esc(p["citation"])}</p><p class="pub-meta">{esc(topic)}</p><p class="pub-links">{" ".join(links)}{note}</p></li>')
    bibliography = f'<p class="section-note">{anchor(PROFILE["dblp"], labels["bibliography"])} · {anchor(prefix + "publications.bib", labels["download_bib"], " download")}</p>'
    return bibliography + toolbar + '<ol class="publication-list" id="publication-list">' + '\n'.join(rows) + '</ol>'


def render(lang, prefix, canonical_path):
    p, labels = PROFILE[lang], LABELS[lang]
    title = '李智鑫 | 复旦大学 · 个人主页' if lang == 'zh' else 'Zhixin Li | Fudan University'
    language_href = prefix + ('english/index.html' if lang == 'zh' else 'chinese/index.html')
    nav_keys = ['about', 'research', 'publications', 'honors', 'service', 'teaching', 'contact']
    nav = ''.join(anchor('#' + key, labels[key]) for key in nav_keys)
    intro = ''.join(f'<p class="{"lead" if i == 0 else "bio-paragraph"}">{esc(text)}</p>' for i, text in enumerate(p['intro']))
    about = f'<section class="section" id="about" aria-labelledby="heading-about"><p class="eyebrow">{esc(p["affiliation"])}</p><h1 id="heading-about">{esc(p["name"])} <span>{esc(p["other_name"])}</span></h1>{intro}<p class="section-note"><strong>{esc(labels["keywords"])}</strong><br>{esc(p["keywords"])}</p></section>'
    news = '<ul class="news-list">' + ''.join(f'<li><time>{esc(n["date"])}</time><div>{anchor(n["href"], n["text"])}</div></li>' for n in p['news']) + '</ul>'
    research = '<ul class="research-list">' + ''.join(f'<li><h3>{esc(r["title"])}</h3><p>{esc(r["text"])}</p></li>' for r in p['research']) + '</ul>'
    contact = f'<p>{esc(p["contact_note"])}</p><dl class="contact-list"><dt>{esc(labels["email"])}</dt><dd>{anchor("mailto:" + PROFILE["email"], PROFILE["email"])}</dd><dt>{esc(labels["office"])}</dt><dd>{esc(p["office"])}</dd><dt>{esc(labels["institution"])}</dt><dd>{esc(p["affiliation"])}</dd><dt>{esc(labels["scholarly"])}</dt><dd>{anchor(PROFILE["dblp"], "DBLP")} · {anchor(PROFILE["orcid"], "ORCID")} · {anchor(PROFILE["github"], "GitHub")}</dd></dl>'
    content = about + section('news', labels['news'], news) + section('research', labels['research'], research) + section('projects', labels['projects'], details(p['projects'], labels)) + section('publications', labels['publications'], publications(lang, labels, prefix))
    for key in ['patents', 'honors', 'service', 'teaching', 'talks']:
        content += section(key, labels[key], details(p[key], labels))
    content += section('contact', labels['contact'], contact)
    structured = {"@context": "https://schema.org", "@type": "Person", "name": "Zhixin Li", "alternateName": "李智鑫", "jobTitle": PROFILE['en']['title'], "affiliation": {"@type": "Organization", "name": "Fudan University"}, "email": PROFILE['email'], "url": PROFILE['site_url'] + '/', "sameAs": [PROFILE['dblp'], PROFILE['orcid'], PROFILE['github'], PROFILE['institution_page']]}
    structured_json = json.dumps(structured, ensure_ascii=False).replace('</', '<\\/')
    photo_alt = '李智鑫' if lang == 'zh' else 'Zhixin Li'
    return f'''<!doctype html>
<html lang="{'zh-CN' if lang == 'zh' else 'en'}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{esc(p['description'])}">
  <meta name="author" content="Zhixin Li">
  <meta name="theme-color" content="#173b69">
  <meta name="color-scheme" content="light">
  <meta property="og:type" content="profile">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(p['description'])}">
  <meta property="og:url" content="{esc(PROFILE['site_url'] + canonical_path)}">
  <title>{esc(title)}</title>
  <link rel="canonical" href="{esc(PROFILE['site_url'] + canonical_path)}">
  <link rel="alternate" hreflang="zh-CN" href="{PROFILE['site_url']}/chinese/">
  <link rel="alternate" hreflang="en" href="{PROFILE['site_url']}/english/">
  <link rel="alternate" hreflang="x-default" href="{PROFILE['site_url']}/">
  <link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="{prefix}assets/style.css">
  <script type="application/ld+json">{structured_json}</script>
  <script src="{prefix}assets/site.js" defer></script>
</head>
<body data-lang="{lang}" id="top">
  <a class="skip-link" href="#main-content">{esc(labels['skip'])}</a>
  <header class="site-header"><div class="header-inner">
    <a class="site-brand" href="{prefix}index.html">李智鑫 <span>Zhixin Li</span></a>
    <nav class="site-nav" aria-label="{'主导航' if lang == 'zh' else 'Main navigation'}">{nav}</nav>
    <a class="language-switch" href="{language_href}" lang="{'en' if lang == 'zh' else 'zh-CN'}" hreflang="{'en' if lang == 'zh' else 'zh-CN'}">{esc(labels['language'])}</a>
  </div></header>
  <div class="page-shell">
    <aside class="profile" aria-label="{'个人信息' if lang == 'zh' else 'Profile'}">
      <img class="profile-photo" src="{prefix}assets/zhixin-li.png" width="1002" height="982" alt="{photo_alt}" fetchpriority="high">
      <h2 class="profile-name">{esc(p['name'])}</h2>
      <p class="profile-name-en">{esc(p['other_name'])}</p>
      <p class="profile-position">{esc(p['title'])}</p>
      <p class="profile-meta">{'<br>'.join(esc(x) for x in p['affiliation_lines'])}</p>
      <ul class="profile-links">
        <li>{anchor('mailto:' + PROFILE['email'], PROFILE['email'])}</li>
        <li>{anchor(PROFILE['institution_page'], labels['official'])}</li>
        <li>{anchor(PROFILE['dblp'], 'DBLP')}</li>
        <li>{anchor(PROFILE['orcid'], 'ORCID')}</li>
        <li>{anchor(PROFILE['github'], 'GitHub')}</li>
      </ul>
      <p class="profile-location">Shanghai, China</p>
    </aside>
    <main id="main-content">{content}</main>
  </div>
  <footer class="site-footer"><div>© 2026 Zhixin Li · Fudan University</div><div>{esc(labels['updated'])} {PROFILE['updated']} · {anchor('#top', labels['top'])}</div></footer>
</body>
</html>
'''


def write_bibtex():
    entries = []
    for p in PAPERS:
        entry_type = 'inproceedings' if p['id'] in {'cr-aug', 'transxion', 'jailpo'} else 'article'
        venue_field = 'booktitle' if entry_type == 'inproceedings' else 'journal'
        bib_venue = {'cr-aug': 'Proceedings of the 32nd ACM SIGKDD Conference on Knowledge Discovery and Data Mining V.2', 'transxion': 'Proceedings of the 32nd ACM SIGKDD Conference on Knowledge Discovery and Data Mining V.2', 'fedddim': 'Procedia Computer Science', 'jailpo': 'Proceedings of the AAAI Conference on Artificial Intelligence'}.get(p['id'], p['venue'])
        fields = {'title': p['title'], 'author': ' and '.join(p['authors']), venue_field: bib_venue, 'year': str(p['year']), 'doi': p['doi'], 'url': 'https://doi.org/' + p['doi']}
        lines = [f'@{entry_type}{{li-{p["id"]}-{p["year"]},'] + [f'  {key} = {{{value}}},' for key, value in fields.items()] + ['}']
        entries.append('\n'.join(lines))
    (ROOT / 'publications.bib').write_text('\n\n'.join(entries) + '\n', encoding='utf-8')


if __name__ == '__main__':
    for lang, path, prefix, canonical in [('zh', 'index.html', '', '/'), ('zh', 'chinese/index.html', '../', '/chinese/'), ('en', 'english/index.html', '../', '/english/')]:
        target = ROOT / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render(lang, prefix, canonical), encoding='utf-8')
        print(path)
    write_bibtex()
    if '--preview' in sys.argv:
        preview = ROOT / 'dist'
        preview.mkdir(exist_ok=True)
        for name in ['index.html', 'publications.bib']:
            shutil.copy2(ROOT / name, preview / name)
        for name in ['assets', 'chinese', 'english']:
            shutil.copytree(ROOT / name, preview / name, dirs_exist_ok=True)
    print(f'Built 3 pages with {len(PAPERS)} publications.')
