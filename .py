#              _     _             _aa
#    _  Branch| |__ | | ___   ___ | |_  _   _
#   | |/ / _ \| '_ \| |/ _ \ / _ \| __|| | | |
#   |   < (_) | | | | | (_) | (_) | |_ | |_| |
#   |_|\_\___/|_| |_|_|\___/ \___/ \__| \__,_|
#
# meta developer: @k1sIotaa
# scope: phantom_reply

from .. import loader, utils
from telethon.tl.types import Message, MessageEntityMentionName, MessageEntityTextUrl
import logging

logger = logging.getLogger(__name__)

@loader.tds
class PhantomWinnerMod(loader.Module):
    """Авто-выигрыш для @k1sIotaa. Моментальный ответ 'Я' в комментарии."""
    
    strings = {"name": "PhantomWinner"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "TARGET_PHRASE", 
                "👾𝗣𝗵𝗮𝗻𝘁𝗼𝗺 | М&М | 🐮DAplayers | 🌙𝑳𝒖𝒏𝒂𝒓'𝒔 | k1slotaa🐮🌙", 
                "Фраза для поиска"
            ),
            loader.ConfigValue("MY_ID", 7931588510, "Твой Telegram ID"),
            loader.ConfigValue("MY_USERNAME", "k1sIotaa", "Твой юзернейм"),
            loader.ConfigValue("ENABLED", True, "Статус работы модуля")
        )

    async def watcher(self, message: Message):
        if not isinstance(message, Message) or not self.config["ENABLED"]:
            return

        is_winner = False
        full_text = message.text or ""

        # 1. Простая проверка текста
        if self.config["TARGET_PHRASE"] in full_text:
            is_winner = True

        # 2. Проверка скрытых ссылок (синий текст на скриншоте)
        if not is_winner and message.entities:
            for entity in message.entities:
                if isinstance(entity, MessageEntityMentionName):
                    if entity.user_id == self.config["MY_ID"]:
                        is_winner = True
                        break
                elif isinstance(entity, MessageEntityTextUrl):
                    url = entity.url.lower()
                    if str(self.config["MY_ID"]) in url or self.config["MY_USERNAME"].lower() in url:
                        is_winner = True
                        break

        if is_winner:
            try:
                # Пытаемся отправить коммент
                await self._client.send_message(
                    entity=message.peer_id,
                    message="Я",
                    comment_to=message.id
                )
            except Exception:
                try:
                    # Если не вышло (например, нет группы обсуждения), просто отвечаем
                    await message.reply("Я")
                except Exception:
                    pass

    @loader.command()
    async def phstat(self, message: Message):
        """Переключить модуль (Вкл/Выкл)"""
        self.config["ENABLED"] = not self.config["ENABLED"]
        status = "ВКЛЮЧЕН" if self.config["ENABLED"] else "ВЫКЛЮЧЕН"
        await utils.answer(message, f"<b>[Phantom]</b> Модуль: <code>{status}</code>")
