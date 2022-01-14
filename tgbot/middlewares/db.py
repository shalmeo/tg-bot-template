from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware


class DbMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, db):
        super(DbMiddleware, self).__init__()
        self.db = db


    async def pre_process(self, obj, data, *args):
        data['db'] = self.db