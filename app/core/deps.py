from app.repositories.user_repo import UserRepository
from app.services.user_service import UserService
from app.core.config import settings


def get_user_service():
    """Return a UserService using a repo selected by environment.

    - production: real `UserRepository`
    - development: real `UserRepository` (can be extended)
    - testing: `FakeUserRepo` from `app.test.fake_repo`
    """

    if settings.env == "testing":
        # import lazily to avoid importing test-only modules in prod
        from app.repositories.fake_repo import FakeUserRepo

        repo = FakeUserRepo()
    else:
        repo = UserRepository()

    return UserService(repo)
 