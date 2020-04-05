from authentication.settings import SECRET
from models.models import db, User
from sqlalchemy.orm import sessionmaker

server_secret = SECRET

class AuthBackend(object):
    """Implementing an auth backend class with at least two methods.
    """
    Session = sessionmaker(bind=db)
    session = Session()

    

    def authenticate_user(self, username, password):
        """Authenticate User by username and password.

        Returns:
            A dict representing User Record or None.
        """
        result = session.query(User).filter_by(user_name=username)
        if result and password == result.password:
            return result
        return None

    def get_user(self, user_id):
        """Retrieve User By ID.

        Returns:
            A dict representing User Record or None.
        """
        pass

