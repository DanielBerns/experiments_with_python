import logging

logger = logging.getLogger()

db = {}

class BravoException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        logger.error(message)

def create(key: str, value: dict[str, str]) -> None:
    test = db.get(key, None)
    if test is None:
        db[key] = value
    else:
        message = f"create error: {key}"
        raise BravoException(message)

def read(key: str) -> dict[str, str] | None:
    return db.get(key, None)

def update(key: str, value: dict[str, str]) -> None:
    test = db.get(key, None)
    if test is None:
        message = f"update error: {key}"
        raise BravoException(message)
    else:
        db[key] = value

def delete(key: str) -> None:
    test = db.get(key, None)
    if test is None:
        message = f"delete error: {key}"
        raise BravoException(message)
    else:
        del db[key]

