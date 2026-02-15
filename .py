#              _     _             _aa
#    _  Branch| |__ | | ___   ___ | |_  _   _
#   | |/ / _ \| '_ \| |/ _ \ / _ \| __|| | | |
#   |   < (_) | | | | | (_) | (_) | |_ | |_| |
#   |_|\_\___/|_| |_|_|\___/ \___/ \__| \__,_|
#
# meta developer: @k1sIotaa
# scope: phantom_ai_winner

import re
import logging
from .. import loader, utils
from telethon.tl.types import Message, MessageEntityMentionName, MessageEntityTextUrl

logger = logging.getLogger(__name__)

@loader.tds
class PhantomAIWinnerMod(loader.Module):
    """AI-Автоответчик: распознает твой номер в списке победителей"""
    
    strings = {"name": "PhantomAI"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "TARGET_PHRASE", 
                "👾𝗣𝗵𝗮𝗻𝘁𝗼𝗺 | М&М | 🐮DAplayers | 🌙𝑳𝒖𝒏𝒂𝒓'𝒔 | k1slotaa🐮🌙", 
                "Твое имя для поиска"
            ),
            loader.ConfigValue("MY_ID", 7931588510, "Твой Telegram ID"),
            loader.ConfigValue("MY_USERNAME", "k1sIotaa", "Твой юзернейм"),
            loader.ConfigValue("ENABLED", True, "Включен ли модуль")
        )

    async def watcher(self, message: Message):
        if not isinstance(message, Message) or not self.config["ENABLED"]:
            return

        is_winner = False
        full_text = message.text or ""
        
        # --- AI АНАЛИЗ ТЕКСТА ---
        # Ищем паттерн: любая цифра/номер, после которой идет твое имя или юзернейм
        # Например: "1. @k1sIotaa" или "Победитель №5: 👾𝗣𝗵𝗮𝗻𝘁𝗼𝗺"
        pattern = rf"(\d+)[\s\.\)\-:]*({re.escape(self.config['TARGET_PHRASE'])}|@{self.config['MY_USERNAME']})"
        match = re.search(pattern, full_text, re.IGNORECASE)

        if match:
            win_number = match.group(1)
            logger.info(f"[Phantom AI] Обнаружена победа под номером {win_number}")
            is_winner = True

        # --- ПРОВЕРКА СКРЫТЫХ ССЫЛОК (из прошлых версий) ---
        if not is_winner and message.entities:
            for entity in message.entities:
                if isinstance(entity, MessageEntityMentionName) and entity.user_id == self.config["MY_ID"]:
                    is_winner = True
                    break
                elif isinstance(entity, MessageEntityTextUrl):
                    if str(self.config["MY_ID"]) in entity.url or self.config["MY_USERNAME"].lower() in entity.url:
                        is_winner = True
                        break

        # Дополнительная проверка на простое наличие фразы
        if not is_winner and self.config["TARGET_PHRASE"] in full_text:
            is_winner = True

        if is_winner:
            try:
                # Пытаемся зайти в комментарии канала через GetDiscussionMessage
                from telethon import functions
                discussion = await self._client(functions.channels.GetDiscussionMessageRequest(
                    peer=message.peer_id,
                    msg_id=message.id
                ))
                
                await self._client.send_message(
                    entity=discussion.chats[0].id,
                    message="Я",
                    reply_to=discussion.messages[0].id
                )
            except Exception:
                # Если это обычный чат или комментарии недоступны — обычный реплай
                try:
                    await message.reply("Я")
                except Exception:
                    pass

    @loader.command()
    async def phstat(self, message: Message):
        """Вкл/Выкл Phantom AI"""
        self.config["ENABLED"] = not self.config["ENABLED"]
        status = "ВКЛЮЧЕН" if self.config["ENABLED"] else "ВЫКЛЮЧЕН"
        await utils.answer(message, f"<b>[Phantom AI]</b> Статус: <code>{status}</code>")
