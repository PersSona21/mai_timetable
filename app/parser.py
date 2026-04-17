import os
from dotenv import load_dotenv
from selectolax.lexbor import LexborHTMLParser
import httpx



class Parser:
    
    def __init__(self, url: str):
        self.url = url
        
    
    def parse(self) -> list[dict]:
        html = self._fetch()
        tree = LexborHTMLParser(html)
        return self._get_schedule(tree)

    def _fetch(self):
        with httpx.Client(timeout=None) as client:
            client.get(self.url)
            response = client.get(self.url)
            response.raise_for_status()
            return response.text
    
    def _get_schedule(self, tree: LexborHTMLParser) -> list[dict]:
        """
        Возвращает список, состоящий из словарей с данными про пары
        """
        schedule = []
        for day in tree.css(".step-item"):
            date_node = day.css_first(".step-title")
            # меняем непрерывный пробел на обычный
            date = date_node.text(strip=True).replace('\xa0', ' ') if date_node else None
            # В пропускаем информацию о дне
            for lesson in day.css(".mb-4")[1:]:
                # название предмета
                title_node = lesson.css_first("p")
                
                # убираем тип занятия после названия предмета 
                title = " ".join(title_node.text(strip=True, separator=' ').split()[:-1]) if title_node else None

                # тип занятия (ЛК / ПЗ / ЛР)
                type_node = lesson.css_first(".badge")
                lesson_type = type_node.text(strip=True) if type_node else None

                # все li внутри блока
                li_nodes = lesson.css("ul li")

                # время (первый li)
                time = li_nodes[0].text(strip=True) if li_nodes else None

                # преподаватели (все <a>)
                teachers = [
                    a.text(strip=True)
                    for a in lesson.css("ul li a")
                ]

                # аудитория (последний li)
                place = li_nodes[-1].text(strip=True) if li_nodes else None

                schedule.append({
                    "date": date,
                    "title": title,
                    "type": lesson_type,
                    "time": time,
                    "teachers": teachers,
                    "place": place
                })
        return schedule