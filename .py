
#              _     _             _aa
#    _  Branch| |__ | | ___   ___ | |_  _   _
#   | |/ / _ \| '_ \| |/ _ \ / _ \| __|| | | |
#   |   < (_) | | | | | (_) | (_) | |_ | |_| |
#   |_|\_\___/|_| |_|_|\___/ \___/ \__| \__,_|
#
# meta developer: @k1sIotaa
# scope: phantom_reply

from .. import loader, utils
from telethon.tl.types import Message

@loader.tds
class PhantomAutoReplyMod(loader.Module):
    """Автоответчик на специфическую фразу (для розыгрышей/активностей)"""
    
    strings = {
        "name": "PhantomAutoReply",
        "conf_phrase": "Фраза-триггер (строгое совпадение)",
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
                "Я/Я выиграл", 
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
        """Проверка всех входящих сообщений"""
        if not self.config["ENABLED"] or not message.text:
            return

        # Сравниваем текст сообщения с тем, что в конфиге
        if message.text.strip() == self.config["TARGET_PHRASE"]:
            try:
                # Отправляем ответ в тот же чат/ветку комментариев
                await message.respond(self.config["REPLY_TEXT"])
                # Опционально: логируем в консоль юзербота (не обязательно)
                # logger.info(f"Сработал автоответ в чате {message.chat_id}")
            except Exception:
                # Игнорируем ошибки (например, если запрещено писать в чате)
                pass

    @loader.command()
    async def phstat(self, message: Message):
        """Переключить работу автоответа (вкл/выкл)"""
        new_state = not self.config["ENABLED"]
        self.config["ENABLED"] = new_state
        state_text = "ВКЛЮЧЕН" if new_state else "ВЫКЛЮЧЕН"
        await utils.answer(message, f"<b>[Phantom]</b> Автоответ теперь: <code>{state_text}</code>")
