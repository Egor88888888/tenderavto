import requests
import logging
from typing import Dict

logger = logging.getLogger(__name__)

class TelegramNotifier:
    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{token}"
    
    def send_message(self, text: str, parse_mode: str = 'Markdown'):
        """Отправка сообщения"""
        if not self.token or not self.chat_id:
            logger.warning("⚠️ Telegram не настроен")
            return
        
        try:
            response = requests.post(
                f"{self.api_url}/sendMessage",
                json={
                    'chat_id': self.chat_id,
                    'text': text,
                    'parse_mode': parse_mode,
                    'disable_web_page_preview': True
                }
            )
            
            if response.status_code != 200:
                logger.error(f"❌ Ошибка Telegram: {response.text}")
        except Exception as e:
            logger.error(f"❌ Ошибка отправки: {e}")
    
    def notify_new_tender(self, tender: Dict):
        """Уведомление о новом тендере"""
        message = f"""
🔔 *Новый тендер!*

📋 *Номер:* {tender['tender_id']}
💼 *Заказчик:* {tender.get('customer', 'Не указан')}
📝 *Название:* {tender['title'][:200]}...
💰 *Цена:* {tender.get('price', 0):,.2f} руб.
⏰ *Дедлайн:* {tender.get('deadline', 'Не указан')}

🔗 [Открыть тендер]({tender['url']})
"""
        self.send_message(message)
    
    def notify_status_change(self, tender_id: str, old_status: str, new_status: str):
        """Уведомление об изменении статуса"""
        emoji = {
            'won': '🎉',
            'lost': '❌',
            'cancelled': '⚠️'
        }.get(new_status, '📊')
        
        message = f"""
{emoji} *Изменение статуса!*

📋 Тендер: {tender_id}
📊 Старый статус: {old_status}
📊 Новый статус: {new_status}
"""
        self.send_message(message)
