import requests
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import time
import logging

logger = logging.getLogger(__name__)

class BaseParser(ABC):
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    @abstractmethod
    def search(self, keywords: List[str], min_price: float, max_price: float) -> List[Dict]:
        """Поиск тендеров"""
        pass
    
    @abstractmethod
    def parse_tender_page(self, url: str) -> Dict:
        """Парсинг страницы тендера"""
        pass
    
    def get_page(self, url: str, retries: int = 3) -> Optional[str]:
        """Получить HTML страницы"""
        for i in range(retries):
            try:
                response = self.session.get(url, timeout=30)
                if response.status_code == 200:
                    return response.text
                time.sleep(2 ** i)
            except Exception as e:
                logger.error(f"Ошибка загрузки {url}: {e}")
                if i == retries - 1:
                    raise
        return None
