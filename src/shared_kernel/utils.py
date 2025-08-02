import uuid


def euuid(text: str) -> uuid.UUID:
    return uuid.uuid5(uuid.NAMESPACE_URL, text)
