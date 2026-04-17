from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Table, Date, Integer, Column
from datetime import date


class Base(DeclarativeBase):
	pass


class Group(Base):
    __tablename__ = "groups"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    
    lessons: Mapped[list["Lesson"]] = relationship(back_populates="group")
    
class Subject(Base):
    __tablename__ = "subjects"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)

lesson_teachers = Table(
    "lesson_teachers",
    Base.metadata,
    Column("lesson_id", ForeignKey("lessons.id"), primary_key=True),
    Column("teacher_id", ForeignKey("teachers.id"), primary_key=True),
)

class Teacher(Base):
    __tablename__  = "teachers"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    
    lessons: Mapped[list["Lesson"]] = relationship(
        secondary=lesson_teachers,
        back_populates="teachers"
    )

class Lesson(Base):
    __tablename__ = "lessons"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    group_id: Mapped[int] = mapped_column(Integer, ForeignKey("groups.id"))
    subject_id: Mapped[int] = mapped_column(Integer, ForeignKey("subjects.id"))
    
    date: Mapped[date] = mapped_column(Date, nullable=False)
    time: Mapped[str] = mapped_column(String(20), nullable=False)
    
    type: Mapped[str] = mapped_column(String(10), nullable=False)
    place: Mapped[str | None] = mapped_column(String(50), nullable=True)
    
    
    teachers: Mapped[list["Teacher"]] = relationship(
        secondary=lesson_teachers,
        back_populates="lessons"
    )
    group: Mapped["Group"] = relationship(back_populates="lessons")
    subject: Mapped["Subject"] = relationship()

