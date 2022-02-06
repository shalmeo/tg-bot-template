from aiogram_dialog import DialogRegistry

from . import profile_dialog
from . import admin_dailog
from . import panel_dialog


def setup(registry: DialogRegistry):
    for module in (profile_dialog, admin_dailog, panel_dialog):
        module.setup(registry)