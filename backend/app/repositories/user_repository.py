from sqlalchemy.orm import Session
from app.models import User

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def save_user(db: Session, email: str, login: str, first_name: str, last_name: str, password: str):
    user = User(email=email, login=login, first_name=first_name, last_name=last_name, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user