import hashlib
import re


class Password:
    EASY = 1
    MEDIUM = 2
    HARD = 3
    __salt = ""
    KEY = 'VscoCl2gPxQlX1HuGfiia3Iq8lQk9EqKRbu5SReL4HQ='

    def __init__(self, salt=None):
        if salt:
            self.__salt = salt

    def saltEncriptPassword(self, passw):
        return hashlib.sha256(str(self.__salt + passw).encode('utf-8')).hexdigest()

    @staticmethod
    def twoEncription(passw):
        from cryptography.fernet import Fernet
        cipher_suite = Fernet(Password.KEY)
        return cipher_suite.encrypt(str.encode(passw)).decode("utf-8")

    @staticmethod
    def twoDecription(passw):
        # python3.7 -m  pip install cryptography
        from cryptography.fernet import Fernet
        cipher_suite = Fernet(Password.KEY)
        return cipher_suite.decrypt(str.encode(passw)).decode("utf-8")

    @staticmethod
    def validate_pass(password, difficulty=None):

        if len(password) < 6:
            return "رمز عبور باید حداقل ۶ کاراکتر باشد!"

        if difficulty == Password.MEDIUM and password.isdigit():
            return "لطفا با ترکیب اعداد و حروف رمز عبور پیچیده تری برای خود انتخاب نمایید!"
        if difficulty == Password.HARD and (password.isupper() or password.islower() or password.isdigit()):
            return "لطفا با ترکیب اعداد و حروف و کاراکتر های خاص، رمز عبور پیچیده تری برای خود انتخاب نمایید!"

        return None
