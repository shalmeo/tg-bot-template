from tgbot.config import DbConfig


def get_connection_string(db: DbConfig, async_fallback: bool = False) -> str:
    result = (
        f"postgresql+asyncpg://{db.login}:{db.password}@{db.host}:{db.port}/{db.name}"
    )
    
    if async_fallback:
        result += "?async_fallback=True"

    return result