import { request } from "undici";

export const postJSON = async (url: string, body: unknown) => {
  const res = await request(url, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(body),
  });
  if (res.statusCode >= 400) throw new Error(`Webhook ${res.statusCode}`);
};

