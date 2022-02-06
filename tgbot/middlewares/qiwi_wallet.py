from typing import Dict, Any

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware



class QiwiWalletMiddleware(BaseMiddleware):
    def __init__(self, wallet):
        super().__init__()
        self.wallet = wallet
        
    
    async def on_pre_process_message(self, message: types.Message, data: Dict[str, Any]):
        data["wallet"] = self.wallet
        
        
    async def on_pre_process_callback_query(self, call: types.CallbackQuery, data: Dict[str, Any]):
        data["wallet"] = self.wallet