import { f as createComponent, k as renderComponent, r as renderTemplate, m as maybeRenderHead } from '../chunks/astro/server_BxZCO6wu.mjs';
import 'piccolore';
import { $ as $$Layout } from '../chunks/Layout_BQNZwAUg.mjs';
/* empty css                                  */
export { renderers } from '../renderers.mjs';

const $$People = createComponent(($$result, $$props, $$slots) => {
  const currentPhD = ["Marouane Benbrahim", "Tamanna Rashme", "Amin George", "Josh Waldbieser", "Xinyuan Chen", "Zijian Zhang", "Jiashan Wu", "Rocker D'Antonio"];
  const currentMS = ["Sai Harika Gade", "Pavan Dharma Adapa"];
  const graduated = ["Zonghan Zhang", "Matthew Rester", "Henry Smith", "Samuel Prabhakar", "Rajeev Jogi", "Piero Bracamonte", "Suman Adhikari", "Ramyasri Veerapaneni", "Aymane Jouhari"];
  return renderTemplate`${renderComponent($$result, "Layout", $$Layout, { "title": "People | Zhiqian Chen", "data-astro-cid-b6gi252y": true }, { "default": ($$result2) => renderTemplate` ${maybeRenderHead()}<main class="container" data-astro-cid-b6gi252y> <nav class="top-nav" aria-label="Sections" data-astro-cid-b6gi252y> <a href="/" data-astro-cid-b6gi252y>Home</a> <a href="/research" data-astro-cid-b6gi252y>Research</a> <a href="/people" aria-current="page" data-astro-cid-b6gi252y>People</a> <a href="/teach" data-astro-cid-b6gi252y>Teach</a> <a href="https://zhiqian.ai" target="_blank" rel="noopener" data-astro-cid-b6gi252y>Zhiqian.ai <i class="fas fa-ghost nav-ghost" data-astro-cid-b6gi252y></i></a> </nav> <section class="hero" data-astro-cid-b6gi252y> <h1 data-astro-cid-b6gi252y>People</h1> <p data-astro-cid-b6gi252y>Current students, recent alumni, and regular lab rhythm.</p> </section> <section class="section" data-astro-cid-b6gi252y> <h2 data-astro-cid-b6gi252y>Current Advisees</h2> <div class="people-grid" data-astro-cid-b6gi252y> ${currentPhD.map((name) => renderTemplate`<div class="person" data-astro-cid-b6gi252y><strong data-astro-cid-b6gi252y>${name}</strong><span data-astro-cid-b6gi252y>Ph.D. Student</span></div>`)} ${currentMS.map((name) => renderTemplate`<div class="person" data-astro-cid-b6gi252y><strong data-astro-cid-b6gi252y>${name}</strong><span data-astro-cid-b6gi252y>M.S. Student</span></div>`)} </div> </section> <section class="section" data-astro-cid-b6gi252y> <h2 data-astro-cid-b6gi252y>Recent Alumni</h2> <div class="people-grid" data-astro-cid-b6gi252y> ${graduated.map((name) => renderTemplate`<div class="person" data-astro-cid-b6gi252y><strong data-astro-cid-b6gi252y>${name}</strong><span data-astro-cid-b6gi252y>Graduate / Alumni</span></div>`)} </div> </section> <section class="section" data-astro-cid-b6gi252y> <h2 data-astro-cid-b6gi252y>Spring 2026 Friday Meeting Schedule</h2> <div class="schedule-box" data-astro-cid-b6gi252y> <p data-astro-cid-b6gi252y><strong data-astro-cid-b6gi252y>Spring 2026 group meetings</strong> start at <strong data-astro-cid-b6gi252y>2pm CST</strong>. Each presentation takes up to 30 minutes including Q&amp;A.</p> <p data-astro-cid-b6gi252y><strong data-astro-cid-b6gi252y>Feb 6:</strong> Anim, George · Chen, Xinyuan</p> <p data-astro-cid-b6gi252y><strong data-astro-cid-b6gi252y>Feb 13:</strong> Benbrahim, Marouane · Wang, Shaowen</p> <p data-astro-cid-b6gi252y><strong data-astro-cid-b6gi252y>Feb 20:</strong> D’Antonio, Rocker · Wu, Jiashan</p> <p data-astro-cid-b6gi252y><strong data-astro-cid-b6gi252y>Feb 27:</strong> Zhang, Zijian · Gogihed, Rayane</p> <p data-astro-cid-b6gi252y><strong data-astro-cid-b6gi252y>Mar 6:</strong> Jiachen Zhong · Jebbar, Abdelqoddouss</p> <p data-astro-cid-b6gi252y><strong data-astro-cid-b6gi252y>Mar 20:</strong> Gade, Sai Harika · Adapa, Pavan Dharma</p> <p data-astro-cid-b6gi252y><strong data-astro-cid-b6gi252y>Mar 27:</strong> Rashme, Tamanna · Chen, Xinyuan</p> <p data-astro-cid-b6gi252y><strong data-astro-cid-b6gi252y>Apr 10:</strong> Benbrahim, Marouane · Wang, Shaowen</p> <p data-astro-cid-b6gi252y><strong data-astro-cid-b6gi252y>Apr 17:</strong> D’Antonio, Rocker · Anim, George</p> <p data-astro-cid-b6gi252y><strong data-astro-cid-b6gi252y>Apr 24:</strong> Wu, Jiashan · Zhang, Zijian</p> <p data-astro-cid-b6gi252y><strong data-astro-cid-b6gi252y>May 1:</strong> Rashme, Tamanna · Chen, Xinyuan</p> <p data-astro-cid-b6gi252y><strong data-astro-cid-b6gi252y>May 8:</strong> Benbrahim, Marouane · Wang, Shaowen</p> <p data-astro-cid-b6gi252y><strong data-astro-cid-b6gi252y>May 15:</strong> D’Antonio, Rocker · Rashme, Tamanna</p> </div> </section> </main> ` })} `;
}, "/Users/zc/.openclaw/workspace/imczq-astro/src/pages/people.astro", void 0);

const $$file = "/Users/zc/.openclaw/workspace/imczq-astro/src/pages/people.astro";
const $$url = "/people";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$People,
  file: $$file,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
