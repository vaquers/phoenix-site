-- Добавить поле Telegram username в сообщения с сайта.
ALTER TABLE contact_messages ADD COLUMN IF NOT EXISTS telegram_username TEXT NOT NULL DEFAULT '';
