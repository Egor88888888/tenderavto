import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Инициализация базы данных"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript('''
                CREATE TABLE IF NOT EXISTS tenders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tender_id TEXT UNIQUE NOT NULL,
                    platform TEXT NOT NULL,
                    title TEXT NOT NULL,
                    customer TEXT,
                    start_price REAL,
                    deadline TEXT,
                    status TEXT DEFAULT 'new',
                    url TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE TABLE IF NOT EXISTS tender_analysis (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tender_id TEXT UNIQUE,
                    analysis TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (tender_id) REFERENCES tenders(tender_id)
                );
                
                CREATE TABLE IF NOT EXISTS proposals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tender_id TEXT,
                    proposal_text TEXT,
                    price REAL,
                    status TEXT DEFAULT 'draft',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (tender_id) REFERENCES tenders(tender_id)
                );
            ''')
    
    def save_tender(self, tender: Dict) -> bool:
        """Сохранение тендера"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT OR IGNORE INTO tenders 
                    (tender_id, platform, title, customer, start_price, deadline, url)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    tender['tender_id'],
                    tender['platform'],
                    tender['title'],
                    tender.get('customer', ''),
                    tender.get('price', 0),
                    tender.get('deadline', ''),
                    tender['url']
                ))
                return conn.total_changes > 0
        except Exception as e:
            logger.error(f"Ошибка сохранения: {e}")
            return False
    
    def get_new_tenders(self) -> List[Dict]:
        """Получить новые тендеры"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('''
                SELECT * FROM tenders 
                WHERE status = 'new' 
                ORDER BY created_at DESC
            ''')
            return [dict(row) for row in cursor.fetchall()]
    
    def save_analysis(self, tender_id: str, analysis: Dict):
        """Сохранить анализ"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT OR REPLACE INTO tender_analysis 
                (tender_id, analysis) VALUES (?, ?)
            ''', (tender_id, json.dumps(analysis, ensure_ascii=False)))
    
    def get_analyzed_tenders(self) -> List[Dict]:
        """Получить проанализированные тендеры"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('''
                SELECT t.*, a.analysis 
                FROM tenders t
                JOIN tender_analysis a ON t.tender_id = a.tender_id
                WHERE t.tender_id NOT IN (SELECT tender_id FROM proposals)
            ''')
            return [dict(row) for row in cursor.fetchall()]
    
    def save_proposal(self, tender_id: str, proposal: Dict):
        """Сохранить КП"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO proposals 
                (tender_id, proposal_text, price) 
                VALUES (?, ?, ?)
            ''', (tender_id, proposal['text'], proposal['price']))
    
    def get_active_applications(self) -> List[Dict]:
        """Получить активные заявки"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('''
                SELECT t.*, p.status as app_status 
                FROM tenders t
                JOIN proposals p ON t.tender_id = p.tender_id
                WHERE p.status NOT IN ('won', 'lost', 'cancelled')
            ''')
            return [dict(row) for row in cursor.fetchall()]
    
    def update_status(self, tender_id: str, status: str):
        """Обновить статус"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                UPDATE proposals 
                SET status = ? 
                WHERE tender_id = ?
            ''', (status, tender_id))
