from sqlmodel import select, Session
from models.radius_models import User

def get_user(db: Session, id: int) -> User:
    user = db.query(User).get(id)
    return user