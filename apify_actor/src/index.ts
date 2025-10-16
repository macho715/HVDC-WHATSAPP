import { Actor } from "apify";
import { startWhatsapp } from "./whatsapp.js";
import { PocInput } from "./types.js";
import { postJSON } from "./util.js";

const WEBHOOK_URL = process.env.WEBHOOK_URL!;
const SESSION_KV_KEY = process.env.SESSION_KV_KEY || "baileys_session";
const PAIR_MODE = (process.env.PAIR_MODE || "qr") as "qr" | "code";

await Actor.init();

const input = (await Actor.getInput<PocInput>()) ?? {};
const allowed = (input.allowedGroupIds || "").split(",").map(s => s.trim()).filter(Boolean);
const keyword = input.keywordFilter ? new RegExp(input.keywordFilter, "i") : null;
const forward = input.forwardToWebhook !== false;

const store = await Actor.openKeyValueStore();
const sessionDir = `/tmp/${SESSION_KV_KEY}`;

// (옵션) KV에서 세션 파일 복구/백업 로직 추가 가능

await startWhatsapp({
  sessionPath: sessionDir,
  pairMode: PAIR_MODE,
  onMessage: async (m, groupId) => {
    const msg = m.message;
    if (!msg || !groupId) return;

    if (allowed.length && !allowed.includes(groupId)) return;

    const text =
      (msg?.conversation) ||
      (msg?.extendedTextMessage?.text) ||
      (msg?.imageMessage?.caption) || "";

    if (keyword && !keyword.test(text)) return;

    const payload = {
      groupId,
      messageId: m.key?.id,
      from: m.key?.participant || m.key?.remoteJid,
      ts: typeof m.messageTimestamp === 'number' ? m.messageTimestamp : m.messageTimestamp?.toNumber?.() ?? Date.now()/1000,
      text,
      hasMedia: Boolean(msg?.imageMessage || msg?.documentMessage || msg?.videoMessage)
    };

    await Actor.pushData(payload);
    if (forward && WEBHOOK_URL) {
      await postJSON(WEBHOOK_URL, { event: "wa.message", data: payload });
    }
  }
});

// 장시간 런 유지
await Actor.setStatusMessage("WA socket running");
await Actor.exit();

