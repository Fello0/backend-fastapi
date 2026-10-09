from config.database import SessionLocal, engine, Base
from models.user import User

Base.metadata.create_all(bind=engine)
db = SessionLocal()

users = [
    User(id=1, username="admin1", password="password123"), 
    User(id=2, username="admin2", password="password123"), 
    User(id=3, username="auditor1", password="password123"), 
    User(id=4, username="cliente1", password="password123"), 
]

for u in users:
    if not db.query(User).filter_by(id=u.id).first():
        db.add(u)

db.commit()
db.close()
print("Base de datos poblada con éxito.")