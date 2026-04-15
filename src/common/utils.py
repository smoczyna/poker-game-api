import re
from passlib.handlers.pbkdf2 import pbkdf2_sha512
import model.constants as constants

__author__ = 'smok'

class Utils(object):

    @staticmethod
    def verify_hashed_password(password, hashed_password):
        """
        verifies hashed password
        """
        return pbkdf2_sha512.verify(password, hashed_password)

    @staticmethod
    def hash_password(password):
        return pbkdf2_sha512.encrypt(password)


    @staticmethod
    def is_email_valid(email):
        email_matcher = re.compile("^[\w-]+@([\w-]+\.)+[\w]+$")
        return True if email_matcher.match(email) else False

    @staticmethod
    def get_card_name(rank, suit):
        return constants.CARD_NAME_PATTERN.format(rank, suit).lower()

