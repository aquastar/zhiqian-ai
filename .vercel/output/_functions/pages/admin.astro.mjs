import { f as createComponent, k as renderComponent, r as renderTemplate, m as maybeRenderHead, l as renderScript } from '../chunks/astro/server_BxZCO6wu.mjs';
import 'piccolore';
import { $ as $$Layout } from '../chunks/Layout_BQNZwAUg.mjs';
/* empty css                                 */
export { renderers } from '../renderers.mjs';

const $$Admin = createComponent(async ($$result, $$props, $$slots) => {
  return renderTemplate`${renderComponent($$result, "Layout", $$Layout, { "title": "Admin | Zhiqian Homepage", "data-astro-cid-2zp6q64z": true }, { "default": async ($$result2) => renderTemplate` ${maybeRenderHead()}<main class="container" id="login-wall" data-astro-cid-2zp6q64z> <div class="login-box card" id="login-form" data-astro-cid-2zp6q64z> <h1 data-astro-cid-2zp6q64z>Admin</h1> <p class="hint" data-astro-cid-2zp6q64z>Enter admin token to continue.</p> <input type="password" id="token-input" placeholder="Token" autocomplete="current-password" data-astro-cid-2zp6q64z> <button class="btn full" id="login-btn" data-astro-cid-2zp6q64z>Enter</button> <p id="login-error" class="error" data-astro-cid-2zp6q64z></p> </div> </main> <main class="container" id="admin-panel" style="display:none" data-astro-cid-2zp6q64z> <div class="top-row" data-astro-cid-2zp6q64z> <h1 data-astro-cid-2zp6q64z>Local Admin Panel</h1> <div class="actions" data-astro-cid-2zp6q64z> <button id="refresh" class="btn" data-astro-cid-2zp6q64z>Refresh</button> <button id="logout" class="btn secondary" data-astro-cid-2zp6q64z>Logout</button> </div> </div> <p class="hint" data-astro-cid-2zp6q64z>Reads from: <code data-astro-cid-2zp6q64z>/api/admin</code></p> <section class="grid" data-astro-cid-2zp6q64z> <article class="card" data-astro-cid-2zp6q64z> <h2 data-astro-cid-2zp6q64z>Inquiries</h2> <div id="inq-count" class="meta" data-astro-cid-2zp6q64z>Loading...</div> <div id="inq-list" class="list" data-astro-cid-2zp6q64z></div> </article> <article class="card" data-astro-cid-2zp6q64z> <h2 data-astro-cid-2zp6q64z>Likes</h2> <div id="like-count" class="meta" data-astro-cid-2zp6q64z>Loading...</div> <div id="like-list" class="list" data-astro-cid-2zp6q64z></div> </article> </section> </main> ${renderScript($$result2, "/Users/zc/.openclaw/workspace/imczq-astro/src/pages/admin.astro?astro&type=script&index=0&lang.ts")} ` })} `;
}, "/Users/zc/.openclaw/workspace/imczq-astro/src/pages/admin.astro", void 0);

const $$file = "/Users/zc/.openclaw/workspace/imczq-astro/src/pages/admin.astro";
const $$url = "/admin";

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  default: $$Admin,
  file: $$file,
  url: $$url
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
