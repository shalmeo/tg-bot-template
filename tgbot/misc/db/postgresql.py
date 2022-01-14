import asyncpg

from typing import Union



class Database:
    
    def __init__(self, config):
        self.pool: Union[asyncpg.Pool, None] = None
        self.config = config

    
    async def create(self):

        self.pool = await asyncpg.create_pool(user=self.config.db.user, 
                                              password=self.config.db.password, 
                                              host=self.config.db.host, 
                                              database=self.config.db.db_name)
    

    async def create_table_users(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS Users (
        ID SERIAL PRIMARY KEY,
        FULLNAME VARCHAR(255) NOT NULL,
        USERNAME VARCHAR(255) NULL,
        TELEGRAM_ID BIGINT NOT NULL UNIQUE
        );
        '''
        await self.pool.execute(sql)


    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters, start=1)
        ])
        return sql, tuple(parameters.values())


    async def add_user(self, full_name, username, telegram_id):
        sql = '''INSERT INTO Users (FULLNAME, USERNAME, TELEGRAM_ID) VALUES($1, $2, $3)'''
        await self.pool.execute(sql, full_name, username, telegram_id)


    async def select_all_users(self):
        sql = '''SELECT * FROM Users'''
        return await self.pool.fetch(sql)

    
    async def select_user(self, **kwargs):
        sql = '''SELECT * FROM Users WHERE '''
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.pool.fetchrow(sql, parameters)

    
    async def count_users(self):
        sql = '''SELECT COUNT(*) FROM Users'''
        return await self.pool.fetchval(sql)
    

    async def update_username(self, username, telegram_id):
        sql = '''UPDATE Users SET USERNAME=$1 WHERE TELEGRAM_ID=$2'''
        await self.pool.execute(sql, username, telegram_id)
    

    async def delete_users(self):
        sql = '''DELETE FROM Users WHERE True'''
        await self.pool.execute(sql)