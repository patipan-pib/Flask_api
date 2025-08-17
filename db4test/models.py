from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, unique=True)

# connect MySQL
# DATABASE_URL = "mysql+pymysql://testuser:testpass@localhost:3308/dbtest"
DATABASE_URL = "mysql+pymysql://testuser:testpass@db:3306/dbtest"
engine = create_engine(DATABASE_URL, echo=True)

# สร้างตารางถ้ายังไม่มี
Base.metadata.create_all(engine)

# SessionLocal ใช้ใน Flask
SessionLocal = sessionmaker(bind=engine)

session = SessionLocal()

# ตรวจสอบว่า table ว่างหรือไม่
existing_users = session.query(User).count()
if existing_users == 0:
    users = [
        User(name="Alice", age=25),
        User(name="Bob", age=30),
        User(name="Charlie", age=35)
    ]
    session.add_all(users)
    session.commit()
    print("3 sample users added to database")
else:
    print(f"{existing_users} user(s) already exist")

session.close()