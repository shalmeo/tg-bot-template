def make_connection_string(db):
    string = f"postgresql+asyncpg://{db.login}:{db.password}@{db.host}:{db.port}/{db.name}"
    return string