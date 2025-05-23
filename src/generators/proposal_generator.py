from typing import Dict
from datetime import datetime
import json

class ProposalGenerator:
    def __init__(self, company_data: Dict):
        self.company_data = company_data
    
    def generate(self, tender: Dict) -> Dict:
        """Генерация коммерческого предложения"""
        analysis = json.loads(tender.get('analysis', '{}'))
        
        hours = analysis.get('estimated_hours', 320)
        hourly_rate = 3500
        base_price = hours * hourly_rate
        our_price = base_price * 0.85
        
        proposal_text = f"""
КОММЕРЧЕСКОЕ ПРЕДЛОЖЕНИЕ

Дата: {datetime.now().strftime('%d.%m.%Y')}
Тендер №: {tender['tender_id']}

Уважаемые коллеги!

{self.company_data['name']} рада предложить свои услуги по реализации проекта:
"{tender['title']}"

О КОМПАНИИ:
- {self.company_data['experience']} лет на рынке
- Команда из {self.company_data['team_size']} специалистов
- Сертификаты качества ISO 9001:2015

ПРЕДЛАГАЕМОЕ РЕШЕНИЕ:
Мы предлагаем комплексный подход к реализации проекта с использованием 
современных технологий и методологий разработки.

ЭТАПЫ РАБОТ:
1. Анализ и проектирование - 10 дней
2. Разработка - {int(hours/8*0.6)} дней
3. Тестирование - {int(hours/8*0.2)} дней
4. Внедрение - {int(hours/8*0.1)} дней

СТОИМОСТЬ: {our_price:,.2f} руб. (включая НДС)
СРОК: {int(hours/8)} рабочих дней

КОНТАКТЫ:
{self.company_data['contact_person']}
Тел: {self.company_data['phone']}
Email: {self.company_data['email']}

С уважением,
{self.company_data['name']}
"""
        
        return {
            'text': proposal_text,
            'price': our_price
        }
