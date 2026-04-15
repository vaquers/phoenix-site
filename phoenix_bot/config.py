import os
from aiogram import Router

router = Router()

# Единственный супер-админ: только он управляет доступом к боту
SUPER_ADMIN_ID = 5584466914

# Токен бота (используется и ботом, и backend'ом для получения фото)
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8357947641:AAFuWLR_F3tJgGp41ZboX8Dy9BFy0B5DL_Y")
COMMUNITY_RSS_URL = os.environ.get("COMMUNITY_RSS_URL", "https://rsshub.app/telegram/channel/phoenixlbsu")
# Канал сообщества: если бот добавлен в канал как админ, посты сохраняются в БД и отдаются в API.
COMMUNITY_CHANNEL_USERNAME = os.environ.get("COMMUNITY_CHANNEL_USERNAME", "phoenixlbsu")