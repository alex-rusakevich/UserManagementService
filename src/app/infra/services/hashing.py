import hashlib
import bcrypt

from app.config import PasswordConfig


class PasswordService:
    def __init__(self, config: PasswordConfig) -> None:
        self.config = config

    def hash(self, string: str) -> str:
        alg = self.config.hash_alg

        if alg == "bcrypt":
            hash_obj = bcrypt.hashpw(string.encode("utf8"), bcrypt.gensalt())
            return hash_obj.decode("utf8")
        else:
            hash_obj = hashlib.new(self.config.hash_alg)
            hash_obj.update(string.encode("utf8"))
            return hash_obj.hexdigest()

    def verify(self, string: str, hashed_string: str) -> bool:
        alg = self.config.hash_alg

        if alg == "bcrypt":
            password_bytes = string.encode("utf-8")
            hashed_bytes = hashed_string.encode("utf-8")
            return bcrypt.checkpw(password_bytes, hashed_bytes)
        else:
            return self.hash(string) == hashed_string
