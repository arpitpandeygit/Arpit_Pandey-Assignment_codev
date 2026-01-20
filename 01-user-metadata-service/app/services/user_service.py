from tenacity import retry, stop_after_attempt, wait_exponential_jitter
from app.repository.user_repo import UserRepository
from app.models.user import User

repo = UserRepository()

class UserService:

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential_jitter(initial=0.5, max=3)
    )
    def create_user(self, data: dict):
        existing = repo.get_user(data["user_id"])
        if existing:
            return existing  # Idempotency

        user = User(**data)
        return repo.create_user(user)

    def get_user(self, user_id: str):
        return repo.get_user(user_id)

