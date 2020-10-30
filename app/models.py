# UserMixin has all the methods and properties that flask-login needs for the UserModel
from flask_login import UserMixin

from .firestore_service import get_user

class UserData:
    def __init__(self, username, password):
        self.username = username
        self.password = password


class UserModel(UserMixin):
    # Everytime we need to create a new UserModel the constructor must have a username and a password...
    # ,,, so that's why we implement the class UserData to make sure that we have all the required information.
    def __init__(self, user_data):
        """
        :param user_data: UserData
        """
        self.id = user_data.username
        self.password = user_data.password
    

    # This static method will be recevived by user_loader, the user_loader will execute this query sending...
    # ...the user_id to this method to request the user's document of the database in firestore and then, it...
    # ...will return the UserModel. This UserModel will be used by flask-login as current user.
    # By using this method as static we can access to it without creating an instance of this class. And...
    # ...that's also the reason why this method doesn't receive 'self' as parameter.
    @staticmethod
    def query(user_id):
        user_doc = get_user(user_id)
        user_data = UserData(
            username=user_doc.id,
            password=user_doc.to_dict()['password']
        )

        return UserModel(user_data)

