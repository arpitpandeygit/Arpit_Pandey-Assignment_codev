import pybreaker
from sqlalchemy.exc import SQLAlchemyError
from app.repository.db import SessionLocal
from app.models.user import User

db_circuit_breaker = pybreaker.CircuitBreaker(
    fail_max=3,
    reset_timeout=30
)

class UserRepository:

    @db_circuit_breaker
    def create_user(self, user: User):
        db = SessionLocal()
        try:
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        except SQLAlchemyError:
            db.rollback()
            raise
        finally:
            db.close()

    def get_user(self, user_id: str):
        db = SessionLocal()
        try:
            return db.query(User).filter(User.user_id == user_id).first()
        finally:
            db.close()

