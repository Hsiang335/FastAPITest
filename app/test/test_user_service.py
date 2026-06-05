from app.services.user_service import UserService
from app.repositories.fake_repo import FakeUserRepo


def test_register():

    service = UserService(FakeUserRepo())

    result = service.register_user(
        None,
        "tom",
        "123456"
    )

    assert result["username"] == "tom"