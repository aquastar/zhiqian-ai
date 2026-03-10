import { f as createComponent, k as renderComponent, r as renderTemplate, m as maybeRenderHead } from '../chunks/astro/server_BxZCO6wu.mjs';
import 'piccolore';
import { $ as $$Layout } from '../chunks/Layout_BQNZwAUg.mjs';
/* empty css                                 */
export { renderers } from '../renderers.mjs';

const $$Teach = createComponent(($$result, $$props, $$slots) => {
  const courses = [
    { tag: "Split-level", title: "CSE 4633/6633 Artificial Intelligence", desc: "Introductory AI course spanning core concepts and methods." },
    { tag: "Split-level", title: "CSE 4693/6693 Intro to Machine Learning", desc: "Foundations of machine learning for undergraduate and graduate students." },
    { tag: "Graduate", title: "CSE 8673 Machine Learning", desc: "Graduate-level machine learning with emphasis on principles and applications." },
    { tag: "Graduate", title: "CSE 8990 Graph Machine Learning", desc: "Advanced topics in graph machine learning and networked intelligence." }
  ];
  return renderTemplate`${renderComponent($$result, "Layout", $$Layout, { "title": "Teach | Zhiqian Chen", "data-astro-cid-2smuybdk": true }, { "default": ($$result2) => renderTemplate` ${maybeRenderHead()}<main class="container" data-astro-cid-2smuybdk> <nav class="top-nav" aria-label="Sections" data-astro-cid-2smuybdk> <a href="/" data-astro-cid-2smuybdk>Home</a> <a href="/research" data-astro-cid-2smuybdk>Research</a> <a href="/people" data-astro-cid-2smuybdk>People</a> <a href="/teach" aria-current="page" data-astro-cid-2smuybdk>Teach</a> <a href="https://zhiqian.ai" target="_blank" rel="noopener" data-astro-cid-2smuybdk>Zhiqian.ai <i class="fas fa-ghost nav-ghost" data-astro-cid-2smuybdk></i></a> </nav> <section class="hero" data-astro-cid-2smuybdk> <h1 data-astro-cid-2smuybdk>Teach</h1> <p data-astro-cid-2smuybdk>Current and recent courses. One course, one card.</p> </section> <section class="section" data-astro-cid-2smuybdk> <h2 data-astro-cid-2smuybdk>Course Override</h2> <div class="schedule-box" data-astro-cid-2smuybdk>
If a course is full and you still want to enroll, first check with your major professor or department to confirm your registration status. Then submit an override request here: <a href="https://www.cse.msstate.edu/capacity-override-request-form/" target="_blank" rel="noopener" data-astro-cid-2smuybdk>capacity override request form</a>.
</div> </section> <section class="section" data-astro-cid-2smuybdk> <h2 data-astro-cid-2smuybdk>Courses</h2> <div class="cards two" data-astro-cid-2smuybdk> ${courses.map((c) => renderTemplate`<article class="card" data-astro-cid-2smuybdk> <span class="tag" data-astro-cid-2smuybdk>${c.tag}</span> <h3 data-astro-cid-2smuybdk>${c.title}</h3> <p data-astro-cid-2smuybdk>${c.desc}</p> </article>`)} </div> </section> </main> ` })} `;
}, "/Users/zc/.openclaw/workspace/imczq-astro/src/pages/teach.astro", void 0);

const $$file = "/Users/zc/.openclaw/workspace/imczq-astro/src/pages/teach.astro";
const $$url = "/teach";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$Teach,
  file: $$file,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
