#!/usr/bin/env node
/*
 * Build du blog : convertit les posts Markdown (blog/posts/*.md)
 * en pages HTML avec le theme du portfolio.
 * Usage : npm run blog   (node blog/build.js)
 */
const fs = require("fs");
const path = require("path");
const { marked } = require("marked");

const ROOT = path.resolve(__dirname, "..");
const POSTS_DIR = path.join(__dirname, "posts");
const OUT_DIR = __dirname; // blog/

const SITE = {
  name: "Farid Slimani",
  desc: "Expert Odoo — blog, conseils et bonnes pratiques",
};

function slugify(s) {
  return s
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "");
}

function readFrontMatter(raw) {
  const m = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?/);
  if (!m) throw new Error("front matter manquant");
  const meta = {};
  for (const line of m[1].split(/\r?\n/)) {
    const kv = line.match(/^([a-zA-Z]+):\s*(.*)$/);
    if (!kv) continue;
    let val = kv[2].trim();
    if (val.startsWith("[") && val.endsWith("]")) {
      val = val
        .slice(1, -1)
        .split(",")
        .map((s) => s.trim().replace(/^"|"$/g, ""))
        .filter(Boolean);
    } else {
      val = val.replace(/^"|"$/g, "");
    }
    meta[kv[1]] = val;
  }
  return { meta, body: raw.slice(m[0].length) };
}

function loadPosts() {
  return fs
    .readdirSync(POSTS_DIR)
    .filter((f) => f.endsWith(".md"))
    .map((f) => {
      const raw = fs.readFileSync(path.join(POSTS_DIR, f), "utf8");
      const { meta, body } = readFrontMatter(raw);
      return {
        ...meta,
        body,
        html: marked.parse(body),
        slug: slugify(meta.title || f.replace(/\.md$/, "")),
      };
    })
    .sort((a, b) => (a.date < b.date ? 1 : -1));
}

function page(title, desc, body, active = "blog") {
  return `<!DOCTYPE html>
<html lang="fr" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${title} — ${SITE.name}</title>
  <meta name="description" content="${desc}">
  <meta name="theme-color" content="#0B1220">
  <meta property="og:title" content="${title}">
  <meta property="og:description" content="${desc}">
  <meta property="og:type" content="website">
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%234F46E5'/%3E%3Ctext x='32' y='42' font-family='Arial,sans-serif' font-size='26' font-weight='bold' fill='white' text-anchor='middle'%3EFS%3C/text%3E%3C/svg%3E">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Sora:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  <link rel="stylesheet" href="../styles.css">
</head>
<body class="bg-slate-50 text-slate-800 font-sans antialiased">
  <div id="scrollProgress" aria-hidden="true"></div>
  <nav class="fixed w-full bg-white/85 backdrop-blur-md z-50 border-b border-slate-200/70">
    <div class="container-x">
      <div class="flex justify-between items-center h-16">
        <a href="../index.html" class="flex items-center gap-2 group">
          <span class="w-9 h-9 rounded-xl bg-gradient-to-br from-indigo-600 to-violet-600 text-white flex items-center justify-center font-bold font-display text-sm shadow-md shadow-indigo-600/30">FS</span>
          <span class="font-display font-bold text-slate-900 tracking-tight group-hover:text-primary transition">Farid Slimani</span>
        </a>
        <div class="hidden md:flex items-center space-x-6 text-sm font-medium">
          <a href="../index.html#about" class="nav-link hover:text-primary transition">À propos</a>
          <a href="../index.html#services" class="nav-link hover:text-primary transition">Services</a>
          <a href="../index.html#projects" class="nav-link hover:text-primary transition">Projets</a>
          <a href="../index.html#odoo-apps" class="nav-link hover:text-primary transition">Odoo Apps</a>
          <a href="index.html" class="${active === "blog" ? "nav-link active" : "nav-link"} hover:text-primary transition">Blog</a>
          <a href="../index.html#contact" class="btn-outline-primary px-5 py-2 text-sm">Contact</a>
        </div>
        <button id="menuBtn" class="md:hidden text-xl text-slate-700" aria-label="Ouvrir le menu"><i class="fas fa-bars"></i></button>
      </div>
    </div>
    <div id="mobileMenu" class="hidden md:hidden bg-white/95 backdrop-blur border-t border-slate-200 p-4 space-y-3 shadow-xl">
      <a href="../index.html#about" class="block py-1.5 hover:text-primary transition">À propos</a>
      <a href="../index.html#services" class="block py-1.5 hover:text-primary transition">Services</a>
      <a href="../index.html#projects" class="block py-1.5 hover:text-primary transition">Projets</a>
      <a href="../index.html#odoo-apps" class="block py-1.5 hover:text-primary transition">Odoo Apps</a>
      <a href="index.html" class="block py-1.5 ${active === "blog" ? "text-primary font-semibold" : ""} hover:text-primary transition">Blog</a>
      <a href="../index.html#contact" class="block py-2.5 mt-2 text-center bg-gradient-to-r from-indigo-600 to-violet-600 text-white rounded-lg">Contact</a>
    </div>
  </nav>

  <main>${body}</main>

  <footer class="bg-slate-950 text-slate-400 py-8">
    <div class="container-x flex flex-col md:flex-row justify-between items-center gap-4">
      <p>&copy; 2026 ${SITE.name} — Tous droits réservés</p>
      <div class="flex space-x-5">
        <a href="https://www.linkedin.com/in/farid-slimani/" target="_blank" rel="noopener" class="w-10 h-10 rounded-full border border-slate-700 flex items-center justify-center hover:border-indigo-400 hover:text-white hover:-translate-y-0.5 transition" aria-label="LinkedIn"><i class="fab fa-linkedin-in"></i></a>
        <a href="https://apps.odoo.com/apps/modules/browse?search=slimani" target="_blank" rel="noopener" class="w-10 h-10 rounded-full border border-slate-700 flex items-center justify-center hover:border-indigo-400 hover:text-white hover:-translate-y-0.5 transition" aria-label="Odoo Apps"><i class="fa-solid fa-cubes"></i></a>
        <a href="mailto:tech5262@gmail.com" class="w-10 h-10 rounded-full border border-slate-700 flex items-center justify-center hover:border-indigo-400 hover:text-white hover:-translate-y-0.5 transition" aria-label="Email"><i class="fa-solid fa-envelope"></i></a>
      </div>
    </div>
  </footer>

  <button id="toTop" aria-label="Retour en haut" class="fixed bottom-6 right-6 z-50 w-11 h-11 rounded-full bg-gradient-to-br from-indigo-600 to-violet-600 text-white shadow-lg shadow-indigo-600/30 flex items-center justify-center hover:-translate-y-1 transition"><i class="fas fa-arrow-up"></i></button>

  <script>
    const menuBtn = document.getElementById('menuBtn');
    const mobileMenu = document.getElementById('mobileMenu');
    if (menuBtn && mobileMenu) menuBtn.addEventListener('click', () => mobileMenu.classList.toggle('hidden'));
    const progress = document.getElementById('scrollProgress');
    const toTop = document.getElementById('toTop');
    if (progress && toTop) {
      window.addEventListener('scroll', () => {
        const h = document.documentElement.scrollHeight - window.innerHeight;
        progress.style.width = h > 0 ? (window.scrollY / h) * 100 + '%' : '0%';
        toTop.classList.toggle('show', window.scrollY > 600);
      });
      toTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
    }
  </script>
</body>
</html>`;
}

function buildIndex(posts) {
  const cards = posts
    .map(
      (p) => `
      <a href="${p.slug}.html" class="card card-hover p-7 block fade-in group">
        <div class="flex flex-wrap gap-2 mb-3">
          <span class="magic-tag">${p.date || ""}</span>
          ${(p.tags || [])
            .map((t) => `<span class="magic-tag">${t}</span>`)
            .join("")}
        </div>
        <h3 class="font-display text-xl font-bold text-slate-900 group-hover:text-primary transition">${p.title}</h3>
        <p class="text-sm text-slate-600 mt-3">${p.excerpt || ""}</p>
      </a>`
    )
    .join("");

  const body = `
    <section class="pt-28 pb-24 bg-white">
      <div class="container-x max-w-4xl">
        <div class="fade-in">
          <span class="section-eyebrow">Blog</span>
          <h1 class="mt-3 font-display text-3xl md:text-4xl font-bold text-slate-900">${SITE.desc}</h1>
          <p class="text-slate-600 mt-3">Conseils, retours d'expérience et bonnes pratiques autour d'Odoo et de la transformation numérique.</p>
        </div>
        <div class="mt-12 space-y-6">${cards}</div>
      </div>
    </section>`;

  fs.writeFileSync(path.join(OUT_DIR, "index.html"), page("Blog", SITE.desc, body));
}

function buildPost(p) {
  const tags = (p.tags || []).map((t) => `<span class="magic-tag">${t}</span>`).join("");
  const body = `
    <section class="pt-28 pb-24 bg-white">
      <div class="container-x max-w-3xl">
        <a href="index.html" class="text-sm text-primary hover:underline"><i class="fas fa-arrow-left mr-1"></i> Retour au blog</a>
        <div class="mt-6 fade-in">
          <div class="flex flex-wrap gap-2 mb-4">${tags}</div>
          <h1 class="font-display text-3xl md:text-4xl font-bold text-slate-900 leading-tight">${p.title}</h1>
          <p class="text-slate-500 text-sm mt-3">Publié le ${p.date || ""}</p>
        </div>
        <article class="blog-content mt-10 fade-in">${p.html}</article>
      </div>
    </section>`;
  fs.writeFileSync(path.join(OUT_DIR, `${p.slug}.html`), page(p.title, p.excerpt || "", body));
}

function main() {
  const posts = loadPosts();
  buildIndex(posts);
  posts.forEach(buildPost);
  console.log(`Blog construit : ${posts.length} article(s) -> ${OUT_DIR}`);
}

main();