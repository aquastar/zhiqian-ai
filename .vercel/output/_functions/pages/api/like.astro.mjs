import { kv } from '@vercel/kv';
export { renderers } from '../../renderers.mjs';

async function checkRateLimit(ip) {
  const key = `like_rate:${ip}`;
  const count = await kv.incr(key);
  if (count === 1) {
    await kv.expire(key, 3600);
  }
  return count <= 5;
}
const POST = async ({ request }) => {
  const headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
  };
  const ip = request.headers.get("x-forwarded-for")?.split(",")[0].trim() || request.headers.get("x-real-ip") || "unknown";
  const allowed = await checkRateLimit(ip).catch(() => true);
  if (!allowed) {
    return new Response(JSON.stringify({ ok: false, error: "Too many likes" }), { status: 429, headers });
  }
  const row = { ts: (/* @__PURE__ */ new Date()).toISOString(), source: "homepage" };
  await kv.lpush("likes", JSON.stringify(row));
  return new Response(JSON.stringify({ ok: true }), { status: 200, headers });
};
const OPTIONS = async () => {
  return new Response(null, {
    status: 204,
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type"
    }
  });
};

const _page = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
  __proto__: null,
  OPTIONS,
  POST
}, Symbol.toStringTag, { value: 'Module' }));

const page = () => _page;

export { page };
