from dataclasses import dataclass

from environs import Env


@dataclass
class DbConfig:
    login: str
    password: str
    host: str
    port: str
    name: str


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    use_redis: bool


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
        ),
        db=DbConfig(
            login=env.str('DB_LOGIN'),
            password=env.str('DB_PASS'),
            host=env.str('DB_HOST'),
            port=env.str('DB_PORT'),
            name=env.str('DB_NAME'),
        ),
        misc=Miscellaneous()
    )
