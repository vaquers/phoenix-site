-- Посты канала сообщества для страницы «Сообщество» (бот сохраняет при channel_post).

CREATE TABLE IF NOT EXISTS community_channel_posts (
  id             SERIAL PRIMARY KEY,
  channel_username TEXT NOT NULL,
  message_id     BIGINT NOT NULL,
  link           TEXT NOT NULL,
  title          TEXT NOT NULL DEFAULT '',
  created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE (channel_username, message_id)
);

CREATE INDEX IF NOT EXISTS idx_community_channel_posts_channel_created
  ON community_channel_posts (channel_username, created_at DESC);
