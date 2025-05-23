import re
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class DocumentAnalyzer:
    def analyze_tender(self, tender: Dict) -> Dict:
        """Анализ тендера (упрощенный)"""
        title = tender.get('title', '').lower()
        
        work_types = []
        if 'разработка' in title or 'создание' in title:
            work_types.append('development')
        if 'поддержка' in title or 'сопровождение' in title:
            work_types.append('support')
        if 'интеграция' in title:
            work_types.append('integration')
        
        technologies = []
        tech_keywords = {
            '1с': '1C',
            'сайт': 'Web',
            'мобильн': 'Mobile',
            'база данных': 'Database',
            'api': 'API'
        }
        
        for keyword, tech in tech_keywords.items():
            if keyword in title:
                technologies.append(tech)
        
        complexity = 'medium'
        if tender.get('price', 0) > 3000000:
            complexity = 'high'
        elif tender.get('price', 0) < 500000:
            complexity = 'low'
        
        return {
            'work_types': work_types,
            'technologies': technologies,
            'complexity': complexity,
            'estimated_hours': self._estimate_hours(complexity),
            'recommendation': 'suitable' if work_types else 'review_needed'
        }
    
    def _estimate_hours(self, complexity: str) -> int:
        """Оценка трудозатрат"""
        hours = {
            'low': 160,
            'medium': 320,
            'high': 640
        }
        return hours.get(complexity, 320)
