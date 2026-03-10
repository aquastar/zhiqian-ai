import { e as createAstro, f as createComponent, h as addAttribute, n as renderHead, o as renderSlot, r as renderTemplate } from './astro/server_BxZCO6wu.mjs';
import 'piccolore';
import 'clsx';
/* empty css                         */

const $$Astro = createAstro("https://imczq.com");
const $$Layout = createComponent(($$result, $$props, $$slots) => {
  const Astro2 = $$result.createAstro($$Astro, $$props, $$slots);
  Astro2.self = $$Layout;
  const { title = "Zhiqian Chen" } = Astro2.props;
  const umamiWebsiteId = undefined                                       ;
  const clarityId = undefined                                 ;
  return renderTemplate`<html lang="en" data-astro-cid-sckkx6r4> <head><meta charset="UTF-8"><meta name="viewport" content="width=device-width"><link rel="icon" type="image/svg+xml" href="/favicon.svg"><link rel="icon" href="/favicon.ico"><meta name="generator"${addAttribute(Astro2.generator, "content")}><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css"><link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/jpswalsh/academicons@1.9.4/css/academicons.min.css"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Josefin+Sans:wght@400;600;700&family=Montserrat:wght@400;700&display=swap"><title>${title}</title>${umamiWebsiteId}${clarityId}${renderHead()}</head> <body data-astro-cid-sckkx6r4> ${renderSlot($$result, $$slots["default"])} </body></html>`;
}, "/Users/zc/.openclaw/workspace/imczq-astro/src/layouts/Layout.astro", void 0);

export { $$Layout as $ };
