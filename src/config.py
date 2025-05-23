import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # База данных
    DB_PATH = os.getenv('DB_PATH', 'data/tenders.db')
    
    # Telegram
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')
    
    # Email
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    EMAIL_USER = os.getenv('EMAIL_USER', '')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
    EMAIL_TO = os.getenv('EMAIL_TO', '')
    
    # Поиск
    SEARCH_KEYWORDS = os.getenv('SEARCH_KEYWORDS', 'разработка,IT,программирование').split(',')
    MIN_PRICE = float(os.getenv('MIN_PRICE', '100000'))
    MAX_PRICE = float(os.getenv('MAX_PRICE', '5000000'))
    
    # Данные компании
    COMPANY_DATA = {
        'name': os.getenv('COMPANY_NAME', 'ООО "Ваша Компания"'),
        'inn': os.getenv('COMPANY_INN', '0000000000'),
        'experience': int(os.getenv('COMPANY_EXPERIENCE', '5')),
        'team_size': int(os.getenv('COMPANY_TEAM', '10')),
        'contact_person': os.getenv('CONTACT_PERSON', 'Иванов И.И.'),
        'phone': os.getenv('CONTACT_PHONE', '+7 (999) 999-99-99'),
        'email': os.getenv('CONTACT_EMAIL', 'tender@company.ru')
    }
