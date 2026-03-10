import { kv } from '@vercel/kv';
export { renderers } from '../../renderers.mjs';

const POST = async ({ request }) => {
  const headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
  };
  try {
    const body = await request.json().catch(() => ({}));
    const { name, email, role, message } = body;
    if (!name || !email || !message) {
      return new Response(JSON.stringify({ ok: false, error: "Missing required fields" }), { status: 400, headers });
    }
    const row = {
      ts: (/* @__PURE__ */ new Date()).toISOString(),
      name: String(name).slice(0, 200),
      email: String(email).slice(0, 200),
      role: String(role || "").slice(0, 100),
      message: String(message).slice(0, 2e3)
    };
    await kv.lpush("inquiries", JSON.stringify(row));
    return new Response(JSON.stringify({ ok: true }), { status: 200, headers });
  } catch (e) {
    return new Response(JSON.stringify({ ok: false, error: String(e) }), { status: 500, headers });
  }
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
