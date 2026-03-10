import { renderers } from './renderers.mjs';
import { c as createExports, s as serverEntrypointModule } from './chunks/_@astrojs-ssr-adapter_B2pkkb-f.mjs';
import { manifest } from './manifest_BwWwOmmm.mjs';

const serverIslandMap = new Map();;

const _page0 = () => import('./pages/_image.astro.mjs');
const _page1 = () => import('./pages/admin.astro.mjs');
const _page2 = () => import('./pages/api/admin.astro.mjs');
const _page3 = () => import('./pages/api/inquiry.astro.mjs');
const _page4 = () => import('./pages/api/like.astro.mjs');
const _page5 = () => import('./pages/people.astro.mjs');
const _page6 = () => import('./pages/research.astro.mjs');
const _page7 = () => import('./pages/teach.astro.mjs');
const _page8 = () => import('./pages/index.astro.mjs');
const pageMap = new Map([
    ["node_modules/astro/dist/assets/endpoint/generic.js", _page0],
    ["src/pages/admin.astro", _page1],
    ["src/pages/api/admin.ts", _page2],
    ["src/pages/api/inquiry.ts", _page3],
    ["src/pages/api/like.ts", _page4],
    ["src/pages/people.astro", _page5],
    ["src/pages/research.astro", _page6],
    ["src/pages/teach.astro", _page7],
    ["src/pages/index.astro", _page8]
]);

const _manifest = Object.assign(manifest, {
    pageMap,
    serverIslandMap,
    renderers,
    actions: () => import('./noop-entrypoint.mjs'),
    middleware: () => import('./_noop-middleware.mjs')
});
const _args = {
    "middlewareSecret": "76fec442-3a23-4129-bdd6-0071d1d48737",
    "skewProtection": false
};
const _exports = createExports(_manifest, _args);
const __astrojsSsrVirtualEntry = _exports.default;
const _start = 'start';
if (Object.prototype.hasOwnProperty.call(serverEntrypointModule, _start)) ;

export { __astrojsSsrVirtualEntry as default, pageMap };
