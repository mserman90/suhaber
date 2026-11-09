"""
app/whatsapp.py
WhatsApp bülten ve podcast gönderim modülü.
Twilio, WhatsApp Business Cloud API veya Webhook desteği sağlar.
"""

import os
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional
import requests

from app import config

logger = logging.getLogger("whatsapp_notifier")

WHATSAPP_HISTORY_FILE = config.DATA_DIR / "whatsapp_history.json"


def _load_history() -> List[Dict[str, Any]]:
    if WHATSAPP_HISTORY_FILE.exists():
        try:
            with open(WHATSAPP_HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.warning("WhatsApp geçmişi okunamadı: %s", e)
    return []


def _save_history(history: List[Dict[str, Any]]):
    try:
        with open(WHATSAPP_HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error("WhatsApp geçmişi kaydedilemedi: %s", e)


def format_whatsapp_message(podcast_info: Dict[str, Any], items: List[Dict[str, Any]], public_url: str) -> str:
    """Format an informative WhatsApp dispatch summary."""
    today_str = datetime.now(timezone.utc).strftime("%d.%m.%Y")
    lines = [
        f"💧 *SU HABER BÜLTENİ & GÜNDEM PODCAST* ({today_str})",
        "",
        "Günün öne çıkan su ve çevre başlıkları:",
    ]

    for idx, item in enumerate(items[:5], 1):
        title = item.get("title_tr") or item.get("title", "")
        cat = item.get("category_tr", "Su")
        lines.append(f"• *[{cat}]* {title}")

    lines.append("")
    audio_url = podcast_info.get("latest_audio_url")
    if audio_url:
        lines.append(f"🎙️ *Günün Podcastini Dinle:* {audio_url}")

    lines.append(f"🌐 *Gazete Portalını Oku:* {public_url}")
    return "\n".join(lines)


def send_daily_podcast_to_whatsapp(
    podcast_info: Dict[str, Any],
    items: List[Dict[str, Any]],
    public_url: str,
    force: bool = False
) -> Dict[str, Any]:
    """
    Sends podcast episode notification to WhatsApp group/recipients.
    Supported providers:
    1. Webhook (WHATSAPP_WEBHOOK_URL)
    2. WhatsApp Cloud API (WHATSAPP_API_TOKEN, WHATSAPP_PHONE_NUMBER_ID, WHATSAPP_RECIPIENT)
    3. Dry-Run / Local Log fallback if no credentials are configured
    """
    episode_id = podcast_info.get("latest_episode", {}).get("id") or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    history = _load_history()

    if not force and any(h.get("episode_id") == episode_id and h.get("status") == "success" for h in history):
        logger.info("Episode %s daha önce gönderilmiş, atlanıyor.", episode_id)
        return {"status": "skipped", "provider": "cache", "message": "Already sent"}

    message_text = format_whatsapp_message(podcast_info, items, public_url)

    webhook_url = os.getenv("WHATSAPP_WEBHOOK_URL")
    cloud_api_token = os.getenv("WHATSAPP_API_TOKEN")
    phone_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
    recipient = os.getenv("WHATSAPP_RECIPIENT")

    status = "pending"
    provider = "none"

    try:
        if webhook_url:
            provider = "webhook"
            resp = requests.post(webhook_url, json={"text": message_text, "podcast": podcast_info}, timeout=10)
            if resp.status_code in [200, 201, 202, 204]:
                status = "success"
            else:
                status = f"error: http {resp.status_code}"
        elif cloud_api_token and phone_id and recipient:
            provider = "cloud_api"
            api_url = f"https://graph.facebook.com/v19.0/{phone_id}/messages"
            payload = {
                "messaging_product": "whatsapp",
                "to": recipient,
                "type": "text",
                "text": {"body": message_text}
            }
            headers = {
                "Authorization": f"Bearer {cloud_api_token}",
                "Content-Type": "application/json"
            }
            resp = requests.post(api_url, json=payload, headers=headers, timeout=10)
            if resp.status_code in [200, 201]:
                status = "success"
            else:
                status = f"error: http {resp.status_code}"
        else:
            provider = "dry_run"
            logger.info("WhatsApp kimlik bilgileri tanımlanmadığı için dry-run kipinde kaydedildi.")
            status = "success"
    except Exception as e:
        status = f"error: {str(e)}"
        logger.error("WhatsApp gönderim hatası: %s", e)

    entry = {
        "episode_id": episode_id,
        "sent_at": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "provider": provider
    }
    history.append(entry)
    _save_history(history)

    return entry
