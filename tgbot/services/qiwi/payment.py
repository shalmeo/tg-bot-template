from typing import Union

from aiogram.dispatcher.handler import ctx_data

from glQiwiApi import types as qiwi_types


async def create_payment(amount: Union[float, int] = 1, wallet=None) -> qiwi_types.Bill:
    async with wallet:
        return await wallet.create_p2p_bill(amount=amount)