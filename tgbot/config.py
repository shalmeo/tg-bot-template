from dataclasses import dataclass

from environs import Env


@dataclass
class DbConfig:
    login: str
    password: str
    host: str
    port: int
    name: str


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    use_redis: bool


@dataclass
class Qiwi:
    p2p_token: str = None
    
@dataclass
class Webhook:
    webhook_ssl_cert: str
    webhook_ssl_priv: str
    webhook_url: str


@dataclass
class Webapp:
    webapp_host: str
    webapp_port: int


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    qiwi: Qiwi
    webhook: Webhook
    webapp: Webapp


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
            port=env.int('DB_PORT'),
            name=env.str('DB_NAME'),
        ),
        qiwi=Qiwi(
            p2p_token=env.str('P2P_TOKEN')
        ),
        webhook=Webhook(
            webhook_ssl_cert=env.str('WEBHOOK_SSL_CERT'),
            webhook_ssl_priv=env.str('WEBHOOK_SSL_PRIV'),
            webhook_url=f'https://{env.str("IP")}:{env.int("WEBHOOK_PORT")}/tgbot/{env.str("BOT_TOKEN")}'
        ),
        webapp=Webapp(
            webapp_host=env.str('WEBAPP_HOST'),
            webapp_port=env.int('WEBAPP_PORT')
        )
    )
