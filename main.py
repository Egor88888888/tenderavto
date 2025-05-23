#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.config import Config
from src.database import Database
from src.parsers.zakupki_parser import ZakupkiParser
from src.notifiers.telegram_bot import TelegramNotifier
from src.analyzers.document_analyzer import DocumentAnalyzer
from src.generators.proposal_generator import ProposalGenerator
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def monitor_tenders():
    """Мониторинг новых тендеров"""
    logger.info("🔍 Запуск мониторинга тендеров")
    
    config = Config()
    db = Database(config.DB_PATH)
    parser = ZakupkiParser()
    telegram = TelegramNotifier(config.TELEGRAM_TOKEN, config.TELEGRAM_CHAT_ID)
    
    tenders = parser.search(
        keywords=config.SEARCH_KEYWORDS,
        min_price=config.MIN_PRICE,
        max_price=config.MAX_PRICE
    )
    
    logger.info(f"📋 Найдено тендеров: {len(tenders)}")
    
    new_count = 0
    for tender in tenders:
        if db.save_tender(tender):
            new_count += 1
            logger.info(f"✅ Новый тендер: {tender['tender_id']}")
            telegram.notify_new_tender(tender)
            time.sleep(1)
    
    logger.info(f"💾 Добавлено новых тендеров: {new_count}")

def analyze_documents():
    """Анализ документов новых тендеров"""
    logger.info("📄 Запуск анализа документов")
    
    config = Config()
    db = Database(config.DB_PATH)
    analyzer = DocumentAnalyzer()
    
    new_tenders = db.get_new_tenders()
    logger.info(f"📊 Тендеров для анализа: {len(new_tenders)}")
    
    for tender in new_tenders:
        try:
            analysis = analyzer.analyze_tender(tender)
            db.save_analysis(tender['tender_id'], analysis)
            logger.info(f"✅ Проанализирован: {tender['tender_id']}")
        except Exception as e:
            logger.error(f"❌ Ошибка анализа {tender['tender_id']}: {e}")

def generate_proposals():
    """Генерация коммерческих предложений"""
    logger.info("📝 Генерация коммерческих предложений")
    
    config = Config()
    db = Database(config.DB_PATH)
    generator = ProposalGenerator(config.COMPANY_DATA)
    
    analyzed_tenders = db.get_analyzed_tenders()
    
    for tender in analyzed_tenders:
        proposal = generator.generate(tender)
        db.save_proposal(tender['tender_id'], proposal)
        logger.info(f"✅ КП создано: {tender['tender_id']}")

def check_statuses():
    """Проверка статусов заявок"""
    logger.info("📊 Проверка статусов заявок")
    
    config = Config()
    db = Database(config.DB_PATH)
    parser = ZakupkiParser()
    telegram = TelegramNotifier(config.TELEGRAM_TOKEN, config.TELEGRAM_CHAT_ID)
    
    applications = db.get_active_applications()
    
    for app in applications:
        try:
            status = parser.check_status(app['url'])
            if status != app['status']:
                db.update_status(app['tender_id'], status)
                telegram.notify_status_change(app['tender_id'], app['status'], status)
        except Exception as e:
            logger.error(f"❌ Ошибка проверки статуса: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python main.py [monitor|analyze|generate|check]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    commands = {
        "monitor": monitor_tenders,
        "analyze": analyze_documents,
        "generate": generate_proposals,
        "check": check_statuses
    }
    
    if command in commands:
        commands[command]()
    else:
        print(f"❌ Неизвестная команда: {command}")
        sys.exit(1)
