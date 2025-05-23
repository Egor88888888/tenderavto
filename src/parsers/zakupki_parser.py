from .base_parser import BaseParser
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import time
import logging
import re

logger = logging.getLogger(__name__)

class ZakupkiParser(BaseParser):
    BASE_URL = "https://zakupki.gov.ru"
    
    def search(self, keywords: List[str], min_price: float, max_price: float) -> List[Dict]:
        """Поиск на zakupki.gov.ru"""
        tenders = []
        
        for keyword in keywords:
            logger.info(f"🔍 Поиск: {keyword}")
            
            search_url = f"{self.BASE_URL}/epz/order/extendedsearch/results.html"
            params = {
                'searchString': keyword,
                'morphology': 'on',
                'pageNumber': '1',
                'sortDirection': 'false',
                'recordsPerPage': '_20',
                'showLotsInfoHidden': 'false',
                'priceFromGeneral': str(int(min_price)),
                'priceToGeneral': str(int(max_price))
            }
            
            try:
                html = self.get_page(search_url + self._build_query(params))
                if html:
                    soup = BeautifulSoup(html, 'html.parser')
                    items = soup.select('.search-registry-entry-block')
                    
                    for item in items:
                        tender = self._parse_search_item(item)
                        if tender:
                            tenders.append(tender)
                
                time.sleep(3)
                
            except Exception as e:
                logger.error(f"❌ Ошибка поиска '{keyword}': {e}")
        
        return tenders
    
    def _build_query(self, params: Dict) -> str:
        """Построение строки запроса"""
        return '?' + '&'.join([f"{k}={v}" for k, v in params.items()])
    
    def _parse_search_item(self, item) -> Optional[Dict]:
        """Парсинг элемента поиска"""
        try:
            number_elem = item.select_one('.registry-entry__header-mid__number a')
            if not number_elem:
                return None
            
            tender_id = number_elem.text.strip().replace('№', '').strip()
            url = self.BASE_URL + number_elem.get('href', '')
            
            title_elem = item.select_one('.registry-entry__body-value')
            title = title_elem.text.strip() if title_elem else ''
            
            customer_elem = item.select_one('.registry-entry__body-href')
            customer = customer_elem.text.strip() if customer_elem else ''
            
            price_elem = item.select_one('.price-block__value')
            price_text = price_elem.text.strip() if price_elem else '0'
            price = self._parse_price(price_text)
            
            deadline_elem = item.select_one('.data-block__value')
            deadline = deadline_elem.text.strip() if deadline_elem else ''
            
            return {
                'tender_id': tender_id,
                'platform': 'zakupki.gov.ru',
                'title': title,
                'customer': customer,
                'price': price,
                'deadline': deadline,
                'url': url
            }
            
        except Exception as e:
            logger.error(f"❌ Ошибка парсинга: {e}")
            return None
    
    def _parse_price(self, price_text: str) -> float:
        """Парсинг цены"""
        try:
            clean = re.sub(r'[^\d,]', '', price_text)
            clean = clean.replace(',', '.')
            return float(clean) if clean else 0
        except:
            return 0
    
    def parse_tender_page(self, url: str) -> Dict:
        """Парсинг страницы тендера"""
        html = self.get_page(url)
        if not html:
            return {}
        
        soup = BeautifulSoup(html, 'html.parser')
        
        documents = []
        for link in soup.select('a[href*=".pdf"], a[href*=".doc"], a[href*=".docx"]'):
            doc_url = link.get('href', '')
            if not doc_url.startswith('http'):
                doc_url = self.BASE_URL + doc_url
            
            documents.append({
                'name': link.text.strip(),
                'url': doc_url
            })
        
        return {
            'documents': documents,
            'status': self._extract_status(soup)
        }
    
    def _extract_status(self, soup) -> str:
        """Извлечение статуса"""
        status_elem = soup.select_one('.cardMainInfo__state')
        if status_elem:
            status_text = status_elem.text.strip().lower()
            if 'завершен' in status_text:
                return 'completed'
            elif 'отменен' in status_text:
                return 'cancelled'
            elif 'подача заявок' in status_text:
                return 'accepting'
        return 'unknown'
    
    def check_status(self, url: str) -> str:
        """Проверка статуса тендера"""
        data = self.parse_tender_page(url)
        return data.get('status', 'unknown')
