from typing import Any, Tuple

from aiogram import types
from aiogram.contrib.middlewares.i18n import I18nMiddleware as BaseI18nMiddleware
from babel import Locale

from tbot import schemas
from tbot.utils import get_user


class I18nMiddleware(BaseI18nMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]):
        aiogram_user: types.User = types.User.get_current()
        user: schemas.User = get_user(aiogram_user.id)
        *_, data = args
        if user is None:
            locale: Locale = aiogram_user.locale
            try:
                schemas.Lang(locale.language)
                language = data["locale"] = locale.language
            except ValueError:
                language = data["locale"] = schemas.Lang.RU.value
        else:
            language = data["locale"] = user.lang
        return language
