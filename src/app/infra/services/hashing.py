import hashlib

from app.config import PasswordConfig


class PasswordService:
    def __init__(self, config: PasswordConfig) -> None:
        self.config = config

    def hash(self, string: str) -> str:
        hash_obj = hashlib.new(self.config.hash_alg)
        hash_obj.update(string.encode("utf8"))
        return hash_obj.hexdigest()

    def verify(self, string: str, hashed_string: str) -> bool:
        return self.hash(string) == hashed_string
