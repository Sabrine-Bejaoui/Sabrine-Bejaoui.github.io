"""Static site generator for Sabrine Bejaoui's portfolio.

Run:  python build.py
Writes the EN pages at the site root and the FR pages under /fr/.
Content lives in content.py; this file only holds the templates.
"""
import html
import os

from content import SITE, T, PROJECTS, SKILLS, EXPERIENCE, EDUCATION

ROOT = os.path.dirname(os.path.abspath(__file__))
E = html.escape

ICONS = {
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4 7 8 6 8-6"/></svg>',
    "in": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9.5h4V21H3zM9.5 9.5h3.8v1.6h.06c.53-1 1.83-2.06 3.77-2.06 4.03 0 4.77 2.65 4.77 6.1V21h-4v-5.1c0-1.22-.02-2.79-1.7-2.79-1.7 0-1.96 1.33-1.96 2.7V21h-4z"/></svg>',
    "gh": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-3.16 19.49c.5.09.68-.22.68-.48v-1.7c-2.78.6-3.37-1.34-3.37-1.34-.45-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.9 1.53 2.35 1.09 2.92.83.09-.65.35-1.09.64-1.34-2.22-.25-4.56-1.11-4.56-4.95 0-1.09.39-1.98 1.03-2.68-.1-.25-.45-1.27.1-2.65 0 0 .84-.27 2.75 1.02a9.5 9.5 0 0 1 5 0c1.91-1.29 2.75-1.02 2.75-1.02.55 1.38.2 2.4.1 2.65.64.7 1.03 1.59 1.03 2.68 0 3.85-2.34 4.7-4.57 4.94.36.31.68.92.68 1.86v2.75c0 .27.18.58.69.48A10 10 0 0 0 12 2z"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M12 21s-7-6.1-7-11.5a7 7 0 0 1 14 0C19 14.9 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>',
    "dl": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M12 4v11m0 0-4.5-4.5M12 15l4.5-4.5M5 19h14"/></svg>',
    "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M5 12h14m-5-5 5 5-5 5"/></svg>',
}


def url(lang, kind, slug=None):
    """Site-root-relative path (no leading slash) for a page."""
    base = "" if lang == "en" else "fr/"
    if kind == "home":
        return base
    seg = "projects" if lang == "en" else "projets"
    return f"{base}{seg}/{slug}/"


def rel(depth):
    return "../" * depth


def head(lang, title, desc, path, alt_path, depth):
    p = rel(depth)
    other = "fr" if lang == "en" else "en"
    return f"""<!doctype html>
<html lang="{lang}" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="author" content="Sabrine Bejaoui">
<link rel="canonical" href="{SITE['url']}{path}">
<link rel="alternate" hreflang="{lang}" href="{SITE['url']}{path}">
<link rel="alternate" hreflang="{other}" href="{SITE['url']}{alt_path}">
<link rel="alternate" hreflang="x-default" href="{SITE['url']}{path if lang == 'en' else alt_path}">
<meta property="og:type" content="website">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{SITE['url']}{path}">
<meta property="og:image" content="{SITE['url']}assets/img/og.png">
<meta property="og:locale" content="{'en_US' if lang == 'en' else 'fr_FR'}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#FAF8F4">
<link rel="icon" href="{p}assets/img/favicon.svg" type="image/svg+xml">
<link rel="preload" href="{p}assets/fonts/instrument-sans-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{p}assets/fonts/newsreader-latin-500-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{p}assets/css/site.css">
</head>
<body>
<a class="skip" href="#main">{E(T[lang]['skip'])}</a>
"""


def header(lang, depth, alt_href, home_anchor_prefix):
    t = T[lang]
    p = rel(depth)
    a = home_anchor_prefix
    nav = "".join(
        f'<li><a href="{a}#{sid}">{E(label)}</a></li>' for sid, label in t["nav"]
    )
    if lang == "en":
        sw = f'<span aria-current="true">EN</span><a href="{alt_href}" hreflang="fr" lang="fr" data-lang-switch="fr" aria-label="Version française">FR</a>'
    else:
        sw = f'<a href="{alt_href}" hreflang="en" lang="en" data-lang-switch="en" aria-label="English version">EN</a><span aria-current="true">FR</span>'
    home = p + url(lang, "home")
    return f"""<header class="site-header">
  <div class="wrap nav">
    <a class="brand" href="{home or './'}"><span class="mono">SB</span><span>Sabrine Bejaoui</span></a>
    <button class="menu-btn" aria-label="{E(t['menu'])}" aria-expanded="false" aria-controls="nav-links"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
    <ul class="nav-links" id="nav-links">{nav}<li><div class="lang" role="group" aria-label="{E(t['lang_label'])}">{sw}</div></li></ul>
  </div>
</header>
"""


def footer(lang):
    t = T[lang]
    return f"""<footer>
  <div class="wrap">
    <span>© 2026 Sabrine Bejaoui · Bizerte, Tunisia</span>
    <span>{E(t['footer'])}</span>
  </div>
</footer>
<div class="lb" role="dialog" aria-modal="true" aria-label="{E(t['viewer'])}">
  <button class="x" aria-label="{E(t['close'])}">×</button>
  <button class="prev" aria-label="{E(t['prev'])}">‹</button>
  <figure><img src="" alt=""><figcaption></figcaption></figure>
  <button class="nx" aria-label="{E(t['next'])}">›</button>
</div>
<script src="{{P}}assets/js/site.js" defer></script>
</body>
</html>
"""


def write(path, content):
    full = os.path.join(ROOT, path, "index.html") if not path.endswith(".html") else os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


def home(lang):
    t = T[lang]
    other = "fr" if lang == "en" else "en"
    depth = 0 if lang == "en" else 1
    p = rel(depth)
    path = url(lang, "home")
    alt_path = url(other, "home")
    alt_href = p + alt_path if alt_path else (p or "./")
    out = head(lang, t["title"], t["desc"], path, alt_path, depth)
    out += header(lang, depth, alt_href, "")
    cv = p + f"assets/cv/Sabrine_Bejaoui_CV_{lang.upper()}.pdf"

    facts = "".join(f"<div><dt>{E(k)}</dt><dd>{E(v)}</dd></div>" for k, v in t["facts"])
    out += f"""<main id="main">
<section class="hero" id="home" aria-labelledby="hero-title">
  <div class="wrap hero-grid">
    <div>
      <span class="eyebrow">{E(t['hero_eyebrow'])}</span>
      <h1 id="hero-title">{t['hero_title']}</h1>
      <p class="lead">{E(t['hero_lead'])}</p>
      <span class="status"><i aria-hidden="true"></i>{E(t['status'])}</span>
      <div class="actions">
        <a class="btn btn-primary" href="#projects">{E(t['cta_projects'])} {ICONS['arrow']}</a>
        <a class="btn btn-ghost" href="{cv}" download>{ICONS['dl']} {E(t['cta_cv'])}</a>
        <a class="btn btn-ghost" href="#contact">{E(t['cta_contact'])}</a>
      </div>
    </div>
    <dl class="facts">{facts}</dl>
  </div>
</section>
"""
    # About
    about_p = "".join(f"<p>{E(x)}</p>" for x in t["about_left"])
    about_r = "".join(f"<p>{E(x)}</p>" for x in t["about_right"])
    interests = "".join(f"<li>{E(x)}</li>" for x in t["interests"])
    out += f"""<section class="band" id="about" aria-labelledby="about-title">
  <div class="wrap">
    <div class="sec-head reveal"><div><span class="eyebrow">{E(t['about_eyebrow'])}</span><h2 id="about-title">{E(t['about_title'])}</h2></div></div>
    <div class="about-grid reveal">
      <div>{about_p}</div>
      <div>{about_r}<ul class="pill-list" aria-label="{E(t['interests_label'])}">{interests}</ul></div>
    </div>
  </div>
</section>
"""
    # Projects
    cards = ""
    for pr in PROJECTS:
        c = pr[lang]
        href = p + url(lang, "project", pr["slug"])
        thumb = p + f"assets/img/{pr['cover'].get(lang, pr['cover']['en'])}-t.webp"
        stack = "".join(f"<li>{E(s)}</li>" for s in pr["stack_short"])
        extra = ""
        if pr.get("repo"):
            extra = f'<a href="{pr["repo"]}" rel="noopener" target="_blank">{E(t["repo_" + pr["repo_kind"]])} ↗</a>'
        cards += f"""<article class="project reveal">
  <a class="shot" href="{href}" tabindex="-1" aria-hidden="true"><img src="{thumb}" alt="" width="800" height="500" loading="lazy" decoding="async"></a>
  <div>
    <span class="tag">{E(c['tag'])}</span>
    <h3><a href="{href}" style="color:inherit;text-decoration:none">{E(c['name'])}</a></h3>
    <p>{E(c['summary'])}</p>
    <ul class="stack" aria-label="{E(t['tech_label'])}">{stack}</ul>
    <div class="links"><a href="{href}">{E(t['case_study'])} →</a>{extra}</div>
  </div>
</article>
"""
    out += f"""<section id="projects" aria-labelledby="projects-title">
  <div class="wrap">
    <div class="sec-head reveal"><div><span class="eyebrow">{E(t['projects_eyebrow'])}</span><h2 id="projects-title">{E(t['projects_title'])}</h2><p>{E(t['projects_intro'])}</p></div></div>
    <div class="projects">{cards}</div>
  </div>
</section>
"""
    # Skills
    groups = ""
    for g in SKILLS:
        items = "".join(
            f'<li class="used">{E(s)}</li>' for s in g["used"]
        ) + "".join(f"<li>{E(s)}</li>" for s in g["known"])
        groups += f'<div class="skill reveal"><h3>{E(g[lang])}</h3><ul>{items}</ul></div>'
    out += f"""<section class="band" id="skills" aria-labelledby="skills-title">
  <div class="wrap">
    <div class="sec-head reveal"><div><span class="eyebrow">{E(t['skills_eyebrow'])}</span><h2 id="skills-title">{E(t['skills_title'])}</h2><p>{E(t['skills_intro'])}</p></div>
      <div class="legend"><span class="l-used">{E(t['legend_used'])}</span><span>{E(t['legend_known'])}</span></div></div>
    <div class="skills">{groups}</div>
  </div>
</section>
"""
    # Experience & education
    def tl(items):
        s = ""
        for it in items:
            c = it[lang]
            bullets = "".join(f"<li>{E(b)}</li>" for b in c.get("bullets", []))
            bl = f"<ul>{bullets}</ul>" if bullets else ""
            s += f'<li><span class="when">{E(c["when"])}</span><h3>{E(c["title"])}</h3><div class="org">{E(c["org"])}</div>{bl}</li>'
        return s

    out += f"""<section id="experience" aria-labelledby="exp-title">
  <div class="wrap cols">
    <div class="reveal"><span class="eyebrow">{E(t['exp_eyebrow'])}</span><h2 id="exp-title">{E(t['exp_title'])}</h2><ol class="timeline">{tl(EXPERIENCE)}</ol></div>
    <div class="reveal"><span class="eyebrow">{E(t['edu_eyebrow'])}</span><h2>{E(t['edu_title'])}</h2><ol class="timeline">{tl(EDUCATION)}</ol></div>
  </div>
</section>
"""
    out += f"""<section class="band" id="contact" aria-labelledby="contact-title">
  <div class="wrap contact">
    <div class="reveal">
      <span class="eyebrow">{E(t['contact_eyebrow'])}</span>
      <h2 id="contact-title">{E(t['contact_title'])}</h2>
      <p class="lead" style="margin-top:16px">{E(t['contact_lead'])}</p>
      <div class="actions"><a class="btn btn-primary" href="mailto:{SITE['email']}">{ICONS['mail']} {E(t['write'])}</a><a class="btn btn-ghost" href="{cv}" download>{ICONS['dl']} {E(t['cta_cv'])}</a></div>
    </div>
    <ul class="contact-list reveal">
      <li><a href="mailto:{SITE['email']}">{ICONS['mail']}<span><small>Email</small>{SITE['email']}</span></a></li>
      <li><a href="{SITE['linkedin']}" rel="noopener" target="_blank">{ICONS['in']}<span><small>LinkedIn</small>linkedin.com/in/sabrinebejaoui</span></a></li>
      <li><a href="{SITE['github']}" rel="noopener" target="_blank">{ICONS['gh']}<span><small>GitHub</small>github.com/Sabrine-Bejaoui</span></a></li>
      <li><button type="button" class="phone-reveal" data-p="{'|'.join(SITE['phone_parts'])}">{ICONS['phone']}<span><small>{E(t['phone_label'])}</small><span class="pv">{E(t['phone_show'])}</span></span></button></li>
      <li><a href="#contact" aria-disabled="true" tabindex="-1" style="cursor:default">{ICONS['pin']}<span><small>{E(t['location_label'])}</small>{E(t['location'])}</span></a></li>
    </ul>
  </div>
</section>
</main>
"""
    out += footer(lang).replace("{P}", p)
    write(path, out)


def project_page(pr, idx, lang):
    t = T[lang]
    c = pr[lang]
    other = "fr" if lang == "en" else "en"
    depth = 2 if lang == "en" else 3
    p = rel(depth)
    path = url(lang, "project", pr["slug"])
    alt_path = url(other, "project", pr["slug"])
    out = head(lang, f"{c['name']} — Sabrine Bejaoui", c["summary"], path, alt_path, depth)
    home_href = p + url(lang, "home")
    out += header(lang, depth, p + alt_path, home_href or "./")
    cover = pr["cover"].get(lang, pr["cover"]["en"])

    meta = "".join(f"<div><dt>{E(k)}</dt><dd>{E(v)}</dd></div>" for k, v in c["meta"])
    out += f"""<main id="main">
<div class="wrap">
  <p class="crumb"><a href="{home_href or './'}#projects">← {E(t['all_projects'])}</a></p>
  <div class="p-hero">
    <span class="eyebrow">{E(c['tag'])}</span>
    <h1>{E(c['name'])}</h1>
    <p class="lead">{E(c['summary'])}</p>
    <dl class="p-meta">{meta}</dl>
  </div>
  <figure class="cover reveal" style="margin:0"><img src="{p}assets/img/{cover}.webp" alt="{E(c['cover_alt'])}" fetchpriority="high"></figure>
  {f'<p class="note">{E(c["cover_note"])}</p>' if c.get("cover_note") else ''}
"""
    for sec in c["sections"]:
        body = ""
        for block in sec["blocks"]:
            kind = block[0]
            if kind == "p":
                body += f"<p>{E(block[1])}</p>"
            elif kind == "ul":
                body += "<ul>" + "".join(f"<li>{E(x)}</li>" for x in block[1]) + "</ul>"
            elif kind == "flow":
                body += '<ol class="flow">' + "".join(f"<li>{E(x)}</li>" for x in block[1]) + "</ol>"
            elif kind == "features":
                body += '<ul class="features">' + "".join(
                    f"<li><strong>{E(a)}</strong>{E(b)}</li>" for a, b in block[1]
                ) + "</ul>"
            elif kind == "table":
                hdr, rows = block[1], block[2]
                th = "".join(f"<th scope='col'>{E(h)}</th>" for h in hdr)
                trs = "".join(
                    "<tr>" + "".join(
                        f"<td{' class=n' if i else ''}>{E(v)}</td>" for i, v in enumerate(r)
                    ) + "</tr>" for r in rows
                )
                body += f'<div class="table-wrap"><table class="metrics"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'
            elif kind == "note":
                body += f'<p class="note">{E(block[1])}</p>'
        out += f'<div class="split reveal"><h2>{E(sec["title"])}</h2><div class="prose">{body}</div></div>\n'

    # gallery
    gal = ""
    for key, cap in c["gallery"]:
        img = key.get(lang, key["en"]) if isinstance(key, dict) else key
        gal += f"""<li><button type="button" data-full="{p}assets/img/{img}.webp" data-caption="{E(cap)}" aria-label="{E(t['enlarge'])}: {E(cap)}"><figure><div class="frame"><img src="{p}assets/img/{img}-t.webp" alt="{E(cap)}" width="800" height="500" loading="lazy" decoding="async"></div><figcaption>{E(cap)}</figcaption></figure></button></li>"""
    out += f"""<div class="split reveal" id="gallery"><h2>{E(t['screens'])}</h2><div><ul class="gallery">{gal}</ul>{f'<p class="note">{E(c["gallery_note"])}</p>' if c.get("gallery_note") else ''}</div></div>
"""
    stack = "".join(f"<li>{E(s)}</li>" for s in pr["stack_full"])
    links = ""
    if pr.get("repo"):
        links = f'<p style="margin-top:18px"><a class="btn btn-ghost" href="{pr["repo"]}" rel="noopener" target="_blank">{ICONS["gh"]} {E(t["repo_" + pr["repo_kind"]])}</a></p>'
    out += f"""<div class="split reveal"><h2>{E(t['tech'])}</h2><div><ul class="stack" style="margin-top:0">{stack}</ul>{links}</div></div>
"""
    prev_pr = PROJECTS[(idx - 1) % len(PROJECTS)]
    next_pr = PROJECTS[(idx + 1) % len(PROJECTS)]
    out += f"""<nav class="next" aria-label="{E(t['more_projects'])}">
  <a href="{p + url(lang, 'project', prev_pr['slug'])}">← {E(prev_pr[lang]['name'])}</a>
  <a href="{p + url(lang, 'project', next_pr['slug'])}">{E(next_pr[lang]['name'])} →</a>
</nav>
</div>
</main>
"""
    out += footer(lang).replace("{P}", p)
    write(path, out)


def extras():
    pages = [url(l, "home") for l in ("en", "fr")] + [
        url(l, "project", pr["slug"]) for pr in PROJECTS for l in ("en", "fr")
    ]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm += "".join(f"  <url><loc>{SITE['url']}{x}</loc></url>\n" for x in pages)
    sm += "</urlset>\n"
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sm)
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE['url']}sitemap.xml\n")
    nf = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Page not found — Sabrine Bejaoui</title><link rel="icon" href="/assets/img/favicon.svg"><link rel="stylesheet" href="/assets/css/site.css"></head>
<body><main class="wrap" style="padding:120px 28px"><span class="eyebrow">404</span><h1>Page not found · Page introuvable</h1><p class="lead" style="margin-top:16px">The page you are looking for does not exist. · La page demandée n'existe pas.</p><div class="actions"><a class="btn btn-primary" href="/">English</a><a class="btn btn-ghost" href="/fr/">Français</a></div></main></body></html>"""
    with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8") as f:
        f.write(nf)


if __name__ == "__main__":
    for lang in ("en", "fr"):
        home(lang)
        for i, pr in enumerate(PROJECTS):
            project_page(pr, i, lang)
    extras()
    print("built")
