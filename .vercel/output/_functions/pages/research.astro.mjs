import { f as createComponent, k as renderComponent, r as renderTemplate, m as maybeRenderHead } from '../chunks/astro/server_BxZCO6wu.mjs';
import 'piccolore';
import { $ as $$Layout } from '../chunks/Layout_BQNZwAUg.mjs';
/* empty css                                    */
export { renderers } from '../renderers.mjs';

const $$Research = createComponent(($$result, $$props, $$slots) => {
  const directions = [
    { title: "Spectral graph theory", desc: "Using spectral perspectives to understand graph structure, operators, and learning behavior." },
    { title: "UQ for graph dynamics", desc: "Studying uncertainty quantification, inference, and intervention in graph-driven dynamical systems." },
    { title: "Cross-network graph dynamics", desc: "Understanding how heterogeneous networks interact, couple, and evolve together over time." },
    { title: "General theory for graph dynamics", desc: "Searching for broader principles that unify dynamics, interaction, and controllability on graphs." }
  ];
  const works = [
    { venue: "ACM CSUR 2023", title: "Unified GNN framework", desc: "Survey and tutorial-building effort toward unifying spectral and spatial graph learning." },
    { venue: "AAAI 2024", title: "Influence on graphs", desc: "Graph Bayesian Optimization, source localization, and influence maximization for dynamic and multiplex networks." },
    { venue: "SIGSPATIAL 2020", title: "Spatiotemporal and urban forecasting", desc: "Graph-temporal forecasting for traffic and mobility, including award-winning work on urban intelligence." },
    { venue: "Nature Communications 2019", title: "Materials and scientific discovery", desc: "Graph/ML-enabled discovery for solid-state lithium-ion conductors and related science-facing systems." }
  ];
  return renderTemplate`${renderComponent($$result, "Layout", $$Layout, { "title": "Research | Zhiqian Chen", "data-astro-cid-odi5jzfj": true }, { "default": ($$result2) => renderTemplate` ${maybeRenderHead()}<main class="container" data-astro-cid-odi5jzfj> <nav class="top-nav" aria-label="Sections" data-astro-cid-odi5jzfj> <a href="/" data-astro-cid-odi5jzfj>Home</a> <a href="/research" aria-current="page" data-astro-cid-odi5jzfj>Research</a> <a href="/people" data-astro-cid-odi5jzfj>People</a> <a href="/teach" data-astro-cid-odi5jzfj>Teach</a> <a href="https://zhiqian.ai" target="_blank" rel="noopener" data-astro-cid-odi5jzfj>Zhiqian.ai <i class="fas fa-ghost nav-ghost" data-astro-cid-odi5jzfj></i></a> </nav> <section class="hero" data-astro-cid-odi5jzfj> <h1 data-astro-cid-odi5jzfj>Research</h1> <p data-astro-cid-odi5jzfj>I study graph-structured intelligence for dynamic, uncertain, and interconnected systems, with current emphasis on theory, cross-network dynamics, and AI systems.</p> </section> <section class="section" data-astro-cid-odi5jzfj> <h2 data-astro-cid-odi5jzfj>Current Directions</h2> <div class="cards two" data-astro-cid-odi5jzfj> ${directions.map((d) => renderTemplate`<article class="card" data-astro-cid-odi5jzfj> <h3 data-astro-cid-odi5jzfj>${d.title}</h3> <p data-astro-cid-odi5jzfj>${d.desc}</p> </article>`)} </div> </section> <section class="section" data-astro-cid-odi5jzfj> <h2 data-astro-cid-odi5jzfj>Selected Work</h2> <div class="cards two" data-astro-cid-odi5jzfj> ${works.map((w) => renderTemplate`<article class="card" data-astro-cid-odi5jzfj> <span class="tag" data-astro-cid-odi5jzfj>${w.venue}</span> <h3 data-astro-cid-odi5jzfj>${w.title}</h3> <p data-astro-cid-odi5jzfj>${w.desc}</p> </article>`)} </div> </section> </main> ` })} `;
}, "/Users/zc/.openclaw/workspace/imczq-astro/src/pages/research.astro", void 0);

const $$file = "/Users/zc/.openclaw/workspace/imczq-astro/src/pages/research.astro";
const $$url = "/research";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$Research,
  file: $$file,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
