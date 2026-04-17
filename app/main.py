from parser import Parser
from database.models import Base, Subject, Teacher, Lesson, Group
from database.db import engine, session
import os
from datetime import date
from dotenv import load_dotenv


def main():
    load_dotenv()
    url = os.getenv("WEBSITE")
    group_name = os.getenv("GROUP")
    
    parser = Parser(url)
    schedule = parser.parse()
    

    # for lesson in schedule:
    #     print(lesson)

    group = Group(name=group_name)
    Base.metadata.create_all(engine)
    subject = Subject(name="Общая физика")

    # преподаватели
    t1 = Teacher(name="Ушаков Иван Владимирович")
    t2 = Teacher(name="Малышев Максим Алексеевич")

    # занятие
    lesson = Lesson(
        group=group,
        subject=subject,
        date=date(2025, 3, 23),
        time="13:00 - 14:30",
        type="ЛР",
        place="В-603"
    )
    lesson.teachers = [t1, t2]
    # session.add(lesson)
    # session.commit()

    lessons = session.query(Lesson).all()

    for lesson in lessons:
        print("Предмет:", lesson.subject.name)
        print("Группа:", lesson.group.name)
        print("Время:", lesson.time)
        print("Дата:", lesson.date)
        print("Тип:", lesson.type)
        print("Место:", lesson.place)

    print("Преподаватели:")
    for t in lesson.teachers:
        print("   -", t.name)
        
        
if __name__ == "__main__":
    main()