class FakeUserRepo:

    def create(self, db, username=None, password=None):
        return {
            "id": 1,
            "username": username
        }

    def get_by_username(self, db, username):
        return None
