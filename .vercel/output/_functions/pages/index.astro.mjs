import { f as createComponent, k as renderComponent, r as renderTemplate, m as maybeRenderHead, h as addAttribute, u as unescapeHTML, l as renderScript } from '../chunks/astro/server_BxZCO6wu.mjs';
import 'piccolore';
import { $ as $$Layout } from '../chunks/Layout_BQNZwAUg.mjs';
/* empty css                                 */
export { renderers } from '../renderers.mjs';

const $$Index = createComponent(async ($$result, $$props, $$slots) => {
  const updates = [
    { type: "paper", date: "01/2026", text: "Our co-simulation of power network and transportation network has been accepted by <strong>WebConf (WWW) 2026</strong>." },
    { type: "tutorial", date: "01/2026", text: "Will give a tutorial on uncertainty quantification on graph dynamics at <strong>WSDM 2026</strong>." },
    { type: "honor", date: "11/2025", text: "Recognized as a <strong>Research Fellow</strong> at the Social Science Research Center, Mississippi State University." },
    { type: "grant", date: "08/2025", text: "Received <strong>Turing AI Gift</strong> funding for LLM research." },
    { type: "grant", date: "06/2025", text: "Received <strong>NSF CAREER Award</strong> for unification and interactions across heterogeneous graph dynamics." },
    { type: "award", date: "05/2025", text: "Received <strong>Ottilie Schillig Teaching Award</strong> (AI teaching gamification with Lego Edu Kit)." },
    { type: "tutorial", date: "02/2025", text: "Tutorial: Uncertainty Quantification for Dynamical Networks (<strong>WSDM 2025</strong>)." },
    { type: "tutorial", date: "10/2024", text: "Tutorial series on unifying spectral and spatial GNNs (<strong>CIKM 2024</strong> / <strong>SIAM MDS 2024</strong>)." },
    { type: "grant", date: "08/2024", text: "Received <strong>NSF CNS/MSI</strong> fund (co-PI) for speech recognition in English and Spanish with graph learning + LLMs." },
    { type: "grant", date: "07/2024", text: "Received <strong>NSF CNS/CIRC</strong> fund (PI) to develop research infrastructure for graph dynamics." },
    { type: "paper", date: "07/2024", text: "1 paper accepted at <strong>IJCAI 2024</strong> and 2 papers accepted at <strong>EMBC 2024</strong>." },
    { type: "grant", date: "06/2024", text: "Started spatial epidemiology of animal disease collaboration under <strong>USDA-ARS</strong> funded project." },
    { type: "grant", date: "04/2024", text: "Received <strong>NSF EDU/ITEST</strong> fund (co-PI) for AI education research." },
    { type: "grant", date: "01/2024", text: "Received <strong>NSF IIS/III REU Supplement</strong> (PI) for undergraduate research." },
    { type: "paper", date: "12/2023", text: "Two papers accepted by <strong>AAAI 2024</strong> on Graph Bayesian Optimization." },
    { type: "grant", date: "12/2023", text: "Launched cross-disciplinary <strong>Graph AI Working Group</strong> (supported by BCoE)." },
    { type: "grant", date: "08/2023", text: "Received support from <strong>USDA-ARS</strong> funded project (co-PI) on disease genetics." },
    { type: "paper", date: "12/2022", text: "Paper accepted by <strong>SIAM SDM 2023</strong>: higher-order decomposition for influence maximization." },
    { type: "grant", date: "04/2022", text: "Received <strong>NSF IIS/III</strong> fund (PI) for interpretable graph dynamics." },
    { type: "tutorial", date: "05/2021", text: "Tutorial on spreading models for epidemics at <strong>SDM 2021</strong> (GNN/RNN/SIR/PDE)." },
    { type: "award", date: "09/2020", text: "<strong>Best Paper Award</strong> at <strong>ACM SIGSPATIAL 2020</strong>." },
    { type: "paper", date: "12/2019", text: "<strong>Nature Communications</strong> paper selected in Top 50 Chemistry & Materials Sciences articles." }
  ];
  const openProblems = [
    "How can we build a general theory for graph dynamics across heterogeneous networks?",
    "When and where do uncertainty, interaction, and intervention become identifiable in coupled systems?",
    "How should we model LLMs and neural architectures as graph-structured dynamic systems?",
    "What does reliable software/hardware co-design look like for modern AI inference and control?"
  ];
  const githubProjects = [
    "XGraph-Team/Spectral-Graph-Survey",
    "XGraph-Team/Fusion-GAN",
    "XGraph-Team/XFlow",
    "XGraph-Team/SumoXPypsa"
  ];
  const githubCards = await Promise.all(
    githubProjects.map(async (slug) => {
      const url = `https://api.github.com/repos/${slug}`;
      try {
        const res = await fetch(url, { headers: { "User-Agent": "imczq-astro" } });
        if (!res.ok) throw new Error(`GitHub ${res.status}`);
        const repo = await res.json();
        return {
          slug,
          name: repo.name,
          owner: repo.owner?.login ?? "XGraph-Team",
          desc: {
            "Spectral-Graph-Survey": "Survey-driven entry point to spectral graph theory, graph signals, and modern graph learning.",
            "Fusion-GAN": "Music generation project on genre fusion with adversarial dual learning.",
            "XFlow": "Python library for graph flow simulation, diffusion, and network dynamics experiments.",
            "SumoXPypsa": "Coupled transportation-power simulation stack behind the WWW 2026 line of work."
          }[repo.name] || repo.description || "Repository details coming soon.",
          href: repo.html_url,
          stars: repo.stargazers_count ?? 0,
          language: repo.language || "Mixed",
          updated: "",
          customDesc: {
            "Spectral-Graph-Survey": "Survey-driven entry point to spectral graph theory, graph signals, and modern graph learning.",
            "Fusion-GAN": "Music generation project on genre fusion with adversarial dual learning.",
            "XFlow": "Python library for graph flow simulation, diffusion, and network dynamics experiments.",
            "SumoXPypsa": "Coupled transportation-power simulation stack behind the WWW 2026 line of work."
          }[repo.name] || ""
        };
      } catch {
        const [owner, name] = slug.split("/");
        return {
          slug,
          name,
          owner,
          desc: "Repository details temporarily unavailable.",
          href: `https://github.com/${slug}`,
          stars: null,
          language: "",
          updated: ""
        };
      }
    })
  );
  const ghostEntries = [
    { title: "Tech Note #1", meta: "Placeholder", desc: "Short technical writing will land here." },
    { title: "Research Note #1", meta: "Placeholder", desc: "Working notes, paper thoughts, and prototypes." },
    { title: "Build Log #1", meta: "Placeholder", desc: "Small writeups on tools, systems, and experiments." }
  ];
  const workGallery = [
    { src: "https://imczq.com/media/research_statement_hucb80f2447a0a6a816bf6ea6adae9c7ee_371656_1200x1200_fit_q75_h2_lanczos_3.webp", alt: "Research statement visual" },
    { src: "https://imczq.com/project/unifying/featured_hu352832247ca9de48ec6cd5688ca312ae_768239_540x0_resize_q75_h2_lanczos.webp", alt: "Unified framework for graphs" },
    { src: "https://imczq.com/project/gbo/featured_hud696c5486f3d729ebf5ee1ceaffacccd_128059_540x0_resize_q75_h2_lanczos_3.webp", alt: "Graph Bayesian Optimization" }
  ];
  const selectedWorks = [
    { name: "Unified GNN framework", status: "Direction", venue: "ACM CSUR 2023", output: "Survey and tutorial-building effort toward unifying spectral and spatial graph learning.", image: "https://imczq.com/project/unifying/featured_hu352832247ca9de48ec6cd5688ca312ae_768239_540x0_resize_q75_h2_lanczos.webp" },
    { name: "Influence on graphs", status: "Project", venue: "AAAI 2024", output: "Graph Bayesian Optimization, source localization, and influence maximization for dynamic and multiplex networks.", image: "https://imczq.com/project/gbo/featured_hud696c5486f3d729ebf5ee1ceaffacccd_128059_540x0_resize_q75_h2_lanczos_3.webp" },
    { name: "Spatiotemporal and urban forecasting", status: "Awarded", venue: "SIGSPATIAL 2020", output: "Graph-temporal forecasting for traffic and mobility, including award-winning work on urban intelligence.", image: "https://imczq.com/project/20_kalman_gis/featured_hu6d4d4db39f7ac31cad16d8b437bab632_85075_540x0_resize_q75_h2_lanczos_3.webp" },
    { name: "Materials and scientific discovery", status: "Science", venue: "Nature Communications 2019", output: "Graph/ML-enabled discovery for solid-state lithium-ion conductors and related science-facing systems.", image: "https://imczq.com/project/17_fusiongan_icdm/featured_hu79af7702fdd7ef1f1d4d79a2bd7a81f7_90601_540x0_resize_q75_h2_lanczos_3.webp" },
    { name: "Interdisciplinary AI infrastructure", status: "Systems", venue: "WWW 2026", output: "Cross-domain graph infrastructure spanning epidemiology, agriculture, transportation, and engineering.", image: "https://imczq.com/project/23_sim_sdm/featured_hu47ed903882ca2a20b0bbd31dfd70f9ab_135606_540x0_resize_q75_h2_lanczos_3.webp" }
  ];
  return renderTemplate`${renderComponent($$result, "Layout", $$Layout, { "title": "Zhiqian Chen | Homepage Prototype", "data-astro-cid-j7pv25f6": true }, { "default": async ($$result2) => renderTemplate` ${maybeRenderHead()}<main class="container" id="top" data-astro-cid-j7pv25f6> <nav class="top-nav card" aria-label="Sections" data-astro-cid-j7pv25f6> <a href="/" aria-current="page" data-astro-cid-j7pv25f6>Home</a> <a href="/research" data-astro-cid-j7pv25f6>Research</a> <a href="/people" data-astro-cid-j7pv25f6>People</a> <a href="/teach" data-astro-cid-j7pv25f6>Teach</a> <a href="https://zhiqian.ai" target="_blank" rel="noopener" data-astro-cid-j7pv25f6>Zhiqian.ai <i class="fas fa-ghost nav-ghost" data-astro-cid-j7pv25f6></i></a> </nav> <section class="grid-3" data-astro-cid-j7pv25f6> <aside class="left-col" data-astro-cid-j7pv25f6> <article class="card module profile" data-astro-cid-j7pv25f6> <img class="avatar" src="https://imczq.com/authors/admin/avatar_huff586cc3096ffa7a7257f5a661abe783_130497_270x270_fill_q75_lanczos_center.jpg" alt="Zhiqian Chen" data-astro-cid-j7pv25f6> <h1 class="name-en" data-astro-cid-j7pv25f6>Chen, Zhiqian</h1> <p class="name-zh" data-astro-cid-j7pv25f6>陈枳扦
<span class="name-tip" tabindex="0" aria-label="Name meaning note" data-astro-cid-j7pv25f6>?
<span class="tip-pop" data-astro-cid-j7pv25f6>物理含义：根据五行八卦算的</span> </span> </p> <p class="role" data-astro-cid-j7pv25f6>Assistant Professor · Mississippi State University</p> <p class="bio" data-astro-cid-j7pv25f6>I am an Assistant Professor of Computer Science &amp; Engineering at Mississippi State University, focusing on graph-structured intelligence for dynamic, uncertain, and knowledge-rich systems (see <a href="#research" data-astro-cid-j7pv25f6>details of my research interests</a>). I obtained my Ph.D. at Virginia Tech in 2020, under the supervision of Dr. Chang-Tien Lu. For students interested in me, check <a href="#connect-form" data-astro-cid-j7pv25f6>ways to work with me</a>. If interested in my courses, please check the <a href="#teach" data-astro-cid-j7pv25f6>course syllabi</a>.</p> <div class="icons" aria-label="social links" data-astro-cid-j7pv25f6> <a href="https://imczq.com/cv.pdf" title="CV" data-astro-cid-j7pv25f6><i class="ai ai-cv" data-astro-cid-j7pv25f6></i></a> <a href="https://scholar.google.com/citations?hl=en&user=NC3-O6UAAAAJ" title="Google Scholar" data-astro-cid-j7pv25f6><i class="ai ai-google-scholar" data-astro-cid-j7pv25f6></i></a> <a href="https://github.com/aquastar" title="GitHub" data-astro-cid-j7pv25f6><i class="fab fa-github" data-astro-cid-j7pv25f6></i></a> <a href="https://twitter.com/imczq" title="X/Twitter" data-astro-cid-j7pv25f6><i class="fab fa-square-x-twitter" data-astro-cid-j7pv25f6></i></a> <a href="https://www.linkedin.com/in/zhiqian-chen-ai/" title="LinkedIn" data-astro-cid-j7pv25f6><i class="fab fa-linkedin" data-astro-cid-j7pv25f6></i></a> <a href="https://www.zhihu.com/people/aquastar" title="Zhihu" data-astro-cid-j7pv25f6><i class="fab fa-zhihu" data-astro-cid-j7pv25f6></i></a> <a href="https://www.xiaohongshu.com/user/profile/64769efb000000001c029738" title="Xiaohongshu" data-astro-cid-j7pv25f6><i class="fas fa-book" data-astro-cid-j7pv25f6></i></a> <a href="https://orcid.org/0000-0003-4112-9647" title="ORCID" data-astro-cid-j7pv25f6><i class="fab fa-orcid" data-astro-cid-j7pv25f6></i></a> <a href="mailto:zchen@cse.msstate.edu" title="Email" data-astro-cid-j7pv25f6><i class="fas fa-envelope" data-astro-cid-j7pv25f6></i></a> </div> </article> <article class="card module" data-astro-cid-j7pv25f6> <div class="module-head" data-astro-cid-j7pv25f6> <h2 data-astro-cid-j7pv25f6>Recent Updates</h2> </div> <ul class="updates" data-astro-cid-j7pv25f6> ${updates.map((u) => renderTemplate`<li data-astro-cid-j7pv25f6> <span${addAttribute(`tag ${u.type}`, "class")} data-astro-cid-j7pv25f6>${u.type}</span> <span class="date-strong" data-astro-cid-j7pv25f6>${u.date}</span><span class="meta-inline" data-astro-cid-j7pv25f6>${unescapeHTML(u.text)}</span> </li>`)} </ul> </article> </aside> <section class="center-col" data-astro-cid-j7pv25f6> <article class="card module rich hero-module" id="research" data-astro-cid-j7pv25f6> <h2 data-astro-cid-j7pv25f6>Research Statement</h2> <p class="lead" data-astro-cid-j7pv25f6>I am interested in graph-structured intelligence for dynamic, uncertain, and knowledge-rich systems.</p> <div class="direction-visual" data-astro-cid-j7pv25f6> <img${addAttribute(workGallery[0].src, "src")}${addAttribute(workGallery[0].alt, "alt")} data-astro-cid-j7pv25f6> </div> <div class="statement-copy" data-astro-cid-j7pv25f6> <p data-astro-cid-j7pv25f6>My recent work spans <strong data-astro-cid-j7pv25f6>spectral graph theory</strong>, <strong data-astro-cid-j7pv25f6>uncertainty quantification for graph dynamics</strong>, <strong data-astro-cid-j7pv25f6>cross-network graph dynamics</strong>, and the search for a <strong data-astro-cid-j7pv25f6>general theory for graph dynamics</strong>. Across these directions, I care about models that are predictive, interpretable, and theoretically grounded.</p> <p data-astro-cid-j7pv25f6>I have worked on projects in transportation, spatial epidemiology, social systems, circuits, and AI systems, and I often collaborate across disciplines to connect graph-based methods with real-world dynamic processes.</p> </div> </article> <article class="card module rich" id="selected-work" data-astro-cid-j7pv25f6> <h2 data-astro-cid-j7pv25f6>Selected Directions + Works</h2> <div class="work-montage" data-astro-cid-j7pv25f6> ${selectedWorks.map((p) => renderTemplate`<article class="montage-card" data-astro-cid-j7pv25f6> <img${addAttribute(p.image, "src")}${addAttribute(p.name, "alt")} data-astro-cid-j7pv25f6> <div class="montage-overlay" data-astro-cid-j7pv25f6> <div class="work-tags" data-astro-cid-j7pv25f6> <span class="badge venue" data-astro-cid-j7pv25f6>${p.venue}</span> </div> <h3 data-astro-cid-j7pv25f6>${p.name}</h3> <p data-astro-cid-j7pv25f6>${p.output}</p> </div> </article>`)} </div> </article> <article class="card module rich" id="people" data-astro-cid-j7pv25f6> <h2 data-astro-cid-j7pv25f6>People</h2> <p data-astro-cid-j7pv25f6>I work with students and collaborators from CSE, data science, and interdisciplinary application domains.</p> <p data-astro-cid-j7pv25f6>If you are interested in graph dynamics, UQ, spectral methods, LLM/Transformers, or AI education, please reach out through the collaboration form.</p> </article> </section> <aside class="right-col" data-astro-cid-j7pv25f6> <article class="card module accent open-problems-card" id="open-problems" data-astro-cid-j7pv25f6> <h2 data-astro-cid-j7pv25f6>Open Problems</h2> <div class="open-problems-quote" data-astro-cid-j7pv25f6> <span class="quote-mark" data-astro-cid-j7pv25f6>“</span> <ul class="selected-list compact-list" data-astro-cid-j7pv25f6> ${openProblems.map((item) => renderTemplate`<li data-astro-cid-j7pv25f6>${item}</li>`)} </ul> </div> </article> <article class="card module" id="github-projects" data-astro-cid-j7pv25f6> <h2 data-astro-cid-j7pv25f6>Tutorial-related Repos</h2> <div class="stack dense" data-astro-cid-j7pv25f6> ${githubCards.map((repo) => renderTemplate`<a class="mini-card repo-card"${addAttribute(repo.href, "href")} target="_blank" rel="noopener" data-astro-cid-j7pv25f6> <div class="row repo-top" data-astro-cid-j7pv25f6> <div class="repo-title-wrap" data-astro-cid-j7pv25f6> <h3 data-astro-cid-j7pv25f6>${repo.name}</h3> </div> <i class="fab fa-github repo-icon" data-astro-cid-j7pv25f6></i> </div> <p data-astro-cid-j7pv25f6>${repo.desc}</p> <div class="repo-meta" data-astro-cid-j7pv25f6> <span data-astro-cid-j7pv25f6>@${repo.owner}</span> ${repo.language && renderTemplate`<span data-astro-cid-j7pv25f6>${repo.language}</span>`} ${repo.stars !== null && renderTemplate`<span data-astro-cid-j7pv25f6>★ ${repo.stars}</span>`} </div> </a>`)} </div> </article> <article class="card module ghost-card" id="ghost-entries" data-astro-cid-j7pv25f6> <h2 data-astro-cid-j7pv25f6>Tech Notes</h2> <div class="stack dense" data-astro-cid-j7pv25f6> ${ghostEntries.map((entry) => renderTemplate`<div class="mini-card note-card placeholder" data-astro-cid-j7pv25f6> <div class="row" data-astro-cid-j7pv25f6><h3 data-astro-cid-j7pv25f6>${entry.title}</h3><span class="repo-pill muted" data-astro-cid-j7pv25f6>${entry.meta}</span></div> <p data-astro-cid-j7pv25f6>${entry.desc}</p> </div>`)} </div> </article> <article class="card module" id="connect-form" data-astro-cid-j7pv25f6> <h2 data-astro-cid-j7pv25f6>Quick message to me</h2> <p data-astro-cid-j7pv25f6>Send me a short note directly.</p> <form id="collab-form" class="form" data-astro-cid-j7pv25f6> <input id="f-email" name="email" type="email" placeholder="Email" required data-astro-cid-j7pv25f6> <textarea id="f-message" name="message" placeholder="Message" rows="4" required data-astro-cid-j7pv25f6></textarea> <button class="btn full" type="submit" id="form-submit-btn" data-astro-cid-j7pv25f6>Send Inquiry</button> </form> <p id="form-status" class="small" data-astro-cid-j7pv25f6></p> </article> <article class="card module" data-astro-cid-j7pv25f6> <h2 data-astro-cid-j7pv25f6>Like this page</h2> <p data-astro-cid-j7pv25f6>Anonymous likes only.</p> <button id="like-btn" class="btn full like-btn" type="button" data-astro-cid-j7pv25f6> <span id="like-emoji" data-astro-cid-j7pv25f6>👍</span> <span id="like-label" data-astro-cid-j7pv25f6>Like</span> <span id="like-count-badge" class="like-badge" style="display:none" data-astro-cid-j7pv25f6></span> </button> <p id="like-status" class="small" data-astro-cid-j7pv25f6></p> </article> </aside> </section> </main> ${renderScript($$result2, "/Users/zc/.openclaw/workspace/imczq-astro/src/pages/index.astro?astro&type=script&index=0&lang.ts")} ` })} `;
}, "/Users/zc/.openclaw/workspace/imczq-astro/src/pages/index.astro", void 0);

const $$file = "/Users/zc/.openclaw/workspace/imczq-astro/src/pages/index.astro";
const $$url = "";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$Index,
  file: $$file,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
