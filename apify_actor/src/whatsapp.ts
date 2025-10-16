import makeWASocket, {
  useMultiFileAuthState,
  DisconnectReason,
  jidNormalizedUser,
  WASocket
} from "@whiskeysockets/baileys";
import pino from "pino";
import { proto } from "@whiskeysockets/baileys";

export type StartWAOpts = {
  sessionPath: string;                 // Apify key-value에 mirror or local fs
  onMessage: (m: proto.IWebMessageInfo, groupId?: string) => Promise<void>;
  pairMode: "qr" | "code";
};

export const startWhatsapp = async ({ sessionPath, onMessage, pairMode }: StartWAOpts) => {
  const logger = pino({ level: "info" });
  const { state, saveCreds } = await useMultiFileAuthState(sessionPath);

  let sock: WASocket = makeWASocket({
    printQRInTerminal: pairMode === "qr",
    auth: state,
    logger
  });

  sock.ev.on("creds.update", saveCreds);

  sock.ev.on("connection.update", (u) => {
    const { connection, lastDisconnect, qr } = u;
    if (qr && pairMode === "qr") logger.info({ qr }, "Scan QR to login");
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

  // 메시지 수신
  sock.ev.on("messages.upsert", async ({ messages, type }) => {
    for (const webMsg of messages) {
      const key = webMsg.key;
      const jid = key?.remoteJid || "";
      const isGroup = jid.endsWith("@g.us");
      if (!isGroup) continue;

      await onMessage(webMsg, jid);
    }
  });
};

