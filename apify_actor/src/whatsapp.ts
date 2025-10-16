import makeWASocket, {
  useMultiFileAuthState,
  DisconnectReason,
  jidNormalizedUser,
  WASocket
} from "@whiskeysockets/baileys";
import pino from "pino";
import { proto } from "@whiskeysockets/baileys";
import QRCode from "qrcode";

export type StartWAOpts = {
  sessionPath: string;
  onMessage: (m: proto.IWebMessageInfo, groupId?: string) => Promise<void>;
  pairMode: "qr" | "code";
};

export const startWhatsapp = async ({ sessionPath, onMessage, pairMode }: StartWAOpts) => {
  const logger = pino({ level: "info" });
  const { state, saveCreds } = await useMultiFileAuthState(sessionPath);

  let sock: WASocket = makeWASocket({
    auth: state,
    logger
  });

  sock.ev.on("creds.update", saveCreds);

  sock.ev.on("connection.update", async (u) => {
    const { connection, lastDisconnect, qr } = u;
    
    // 최신 방식: 이벤트로 넘어온 QR 문자열을 직접 렌더링
    if (qr && pairMode === "qr") {
      try {
        // 터미널 ASCII QR (가독성 좋음)
        const ascii = await QRCode.toString(qr, { type: "terminal", small: true });
        logger.info("\n================= Scan this QR =================\n" + ascii + "\n================================================\n");
      } catch (e) {
        logger.warn({ err: String(e) }, "Failed to render QR in terminal");
        logger.info({ qr }, "QR string (fallback)");
      }
    }
    
    if (connection === "close") {
      const reason = (lastDisconnect?.error as any)?.output?.statusCode;
      if (reason !== DisconnectReason.loggedOut) {
        logger.warn({ reason }, "Reconnecting...");
        startWhatsapp({ sessionPath, onMessage, pairMode }).catch(console.error);
      } else {
        logger.error("Logged out.");
      }
    } else if (connection === "open") {
      logger.info("WhatsApp connected");
    }
  });

  sock.ev.on("messages.upsert", async ({ messages }) => {
    for (const m of messages) {
      if (!m.message || m.key.fromMe) continue;
      const groupId = m.key.remoteJid?.endsWith("@g.us") ? m.key.remoteJid : undefined;
      await onMessage(m, groupId);
    }
  });

  return sock;
};

