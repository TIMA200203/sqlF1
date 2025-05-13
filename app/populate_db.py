import random
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models import Base, Group, Course, Student
from faker import Faker
from settings import settings


fake = Faker()

DATABASE_URI = settings.DATABASE_URI
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(engine)


def generate_random_name():

    first_name = fake.first_name()
    last_name = fake.last_name()
    return first_name, last_name


def generate_random_course_name():

    subject = fake.word().capitalize()
    level = random.choice(["Basic", "Advanced", "Intermediate"])
    return f"{subject} {level}"


def populate_db():
    print("Start")

    session = SessionLocal()

    try:

        print("видалення старих записів")
        session.execute(text('TRUNCATE students, groups, courses RESTART IDENTITY CASCADE'))
        session.commit()

        print("генерація груп")

        groups = [Group(name=f"GR-{i:02d}") for i in range(1, 11)]
        session.add_all(groups)
        session.commit()

        print("генерація курсів")
        courses = []
        for _ in range(10): 
            course_name = generate_random_course_name()
            existing_course = session.query(Course).filter(Course.name == course_name).first()
            if not existing_course:
                course = Course(name=course_name, description=f"Learn about {course_name.lower()}")
                courses.append(course)
        session.add_all(courses)
        session.commit()

        print("генерація студентів")
        students = []
        for _ in range(200):
            first_name, last_name = generate_random_name()
            group_id = random.choice([g.id for g in groups])
            student = Student(first_name=first_name, last_name=last_name, group_id=group_id)
            students.append(student)

        session.add_all(students)
        session.commit()

        students = session.query(Student).all()
        for student in students:
            num_courses = random.randint(1, 3)
            student.courses = random.sample(courses, num_courses)

        session.commit()

        print("успішно")

    except Exception as e:
        print(f"помилка: {e}")
        session.rollback()

    finally:
        session.close()


if __name__ == "__main__":

    populate_db()
