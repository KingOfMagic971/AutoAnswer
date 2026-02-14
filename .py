#              _     _             _aa
#    _  Branch| |__ | | ___   ___ | |_  _   _
#   | |/ / _ \| '_ \| |/ _ \ / _ \| __|| | | |
#   |   < (_) | | | | | (_) | (_) | |_ | |_| |
#   |_|\_\___/|_| |_|_|\___/ \___/ \__| \__,_|
#
# meta developer: @k1sIotaa
# scope: phantom_reply

import asyncio
from .. import loader, utils
from telethon.tl.types import Message

@loader.tds
class PhantomAutoReplyMod(loader.Module):
    """Автоответчик в комментарии каналов"""
    
    strings = {
        "name": "PhantomAutoReply",
        "conf_phrase": "Фраза-триггер",
        "conf_answer": "Текст ответа",
        "conf_status": "Включен/Выключен модуль"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "TARGET_PHRASE", 
                "👾𝗣𝗵𝗮𝗻𝘁𝗼𝗺 | М&М | 🐮DAplayers | 🌙𝑳𝒖𝒏𝒂𝒓'𝒔 | k1slotaa🐮🌙", 
                lambda: self.strings["conf_phrase"]
            ),
            loader.ConfigValue(
                "REPLY_TEXT", 
                "Я", 
                lambda: self.strings["conf_answer"]
            ),
            loader.ConfigValue(
                "ENABLED", 
                True, 
                lambda: self.strings["conf_status"],
                validator=loader.validators.Boolean()
            ),
        )

    async def watcher(self, message: Message):
        """Мониторинг сообщений и автоответ в комментарии"""
        if not self.config["ENABLED"] or not getattr(message, "text", None):
            return

        # Проверяем, содержит ли сообщение нужную фразу
        if self.config["TARGET_PHRASE"] in message.text:
            try:
                # Чтобы ответить именно в комментарии (в ветку сообщения):
                # 1. Если это пост в канале, отвечаем на него
                # 2. Если это пересланный пост в чате обсуждения, отвечаем в ветку
                await message.reply(self.config["REPLY_TEXT"])
            except Exception:
                # Если нет прав писать или другая ошибка — пропускаем
                pass

    @loader.command()
    async def phstat(self, message: Message):
        """Переключить работу автоответа (вкл/выкл)"""
        new_state = not self.config["ENABLED"]
        self.config["ENABLED"] = new_state
        state_text = "<b>ВКЛЮЧЕН</b>" if new_state else "<b>ВЫКЛЮЧЕН</b>"
        await utils.answer(message, f"<b>[Phantom]</b> Статус автоответа: {state_text}")
