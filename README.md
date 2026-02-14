# AutoAnswer
Модуль автоматический отвечает сообщением Я при виде какого либо 
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
from telethon import functions
import logging

logger = logging.getLogger(__name__)

@loader.tds
class PhantomWinnerMod(loader.Module):
    """Авто-комментатор для @k1sIotaa. Работает во всех каналах."""
    
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
        # Проверка текста сообщения
        full_text = message.text or ""
        
        # 1. Проверка по фразе или юзернейму в тексте
        if self.config["TARGET_PHRASE"] in full_text or f"@{self.config['MY_USERNAME']}" in full_text:
            is_winner = True

        # 2. Проверка сущностей (скрытые ссылки/упоминания)
        if not is_winner and message.entities:
            for entity in message.entities:
                if isinstance(entity, MessageEntityMentionName):
                    if entity.user_id == self.config["MY_ID"]:
                        is_winner = True
                        break
                elif isinstance(entity, MessageEntityTextUrl):
                    if str(self.config["MY_ID"]) in entity.url or self.config["MY_USERNAME"].lower() in entity.url:
                        is_winner = True
                        break

        if is_winner:
            try:
                # Пытаемся получить сообщение из обсуждения для комментирования
                discussion = await self._client(functions.channels.GetDiscussionMessageRequest(
                    peer=message.peer_id,
                    msg_id=message.id
                ))
                
                # Отправляем "Я" в группу обсуждения (комментарии)
                await self._client.send_message(
                    entity=discussion.chats[0].id,
                    message="Я",
                    reply_to=discussion.messages[0].id
                )
                logger.info(f"[Phantom] Оставлен комментарий в канале {message.chat_id}")
            except Exception as e:
                # Если обсуждение не найдено или закрыто, пробуем обычный ответ
                try:
                    await message.reply("Я")
                except Exception:
                    pass

    @loader.command()
    async def phstat(self, message: Message):
        """Переключить модуль (Вкл/Выкл)"""
        self.config["ENABLED"] = not self.config["ENABLED"]
        status = "ВКЛЮЧЕН" if self.config["ENABLED"] else "ВЫКЛЮЧЕН"
        await utils.answer(message, f"<b>[Phantom]</b> Модуль: <code>{status}</code>")
