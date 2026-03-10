import { kv } from '@vercel/kv';
export { renderers } from '../../renderers.mjs';

const ADMIN_TOKEN = process.env.ADMIN_TOKEN || "5a318bf0e66e4fb24356e9c0241391d8";
const GET = async ({ request }) => {
  const headers = { "Content-Type": "application/json" };
  const token = request.headers.get("x-admin-token") || "";
  if (token !== ADMIN_TOKEN) {
    return new Response(JSON.stringify({ ok: false, error: "Unauthorized" }), { status: 401, headers });
  }
  const [rawInquiries, rawLikes] = await Promise.all([
    kv.lrange("inquiries", 0, 199),
    kv.lrange("likes", 0, 499)
  ]);
  const parse = (arr) => arr.map((item) => {
    if (typeof item === "string") {
      try {
        return JSON.parse(item);
      } catch {
        return item;
      }
    }
    return item;
  });
  return new Response(
    JSON.stringify({ ok: true, inquiries: parse(rawInquiries), likes: parse(rawLikes) }),
    { status: 200, headers }
  );
};

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  GET
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
