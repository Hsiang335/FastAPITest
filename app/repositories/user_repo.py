from app.models.user import User

class UserRepository:

    def create(self, db, username: str, password: str):
        user = User(username=username, password=password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def get_by_username(self, db, username: str):
        return db.query(User).filter(User.username == username).first()