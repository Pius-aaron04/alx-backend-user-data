#!/usr/bin/env python3
"""Auth App Db class definition.
"""

from bcrypt import hashpw
from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound, InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import TypeVar
from user import User

from user import Base


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds user data to db.
        """

        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        self._session.refresh(new_user)

        return new_user

    def find_user_by(self, **kwargs):
        """Finds users with matching attributes in kwargs.
        Return
          - list of user instances matching kwargs
        Exceptions
          - Raises NoResultFound if no matching values
          - InvalidRequestError when wrong query arguments are passed
        """

        try:
            user = self._session.query(User).filter_by(**kwargs).first()
        except Exception:
            raise InvalidRequestError

        if not user:
            raise NoResultFound

        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Updates user data"""

        user = self.find_user_by(id=user_id)
        for k, v in kwargs.items():
            if k not in user.__table__.columns.keys():
                raise ValueError
            setattr(user, k, v)
