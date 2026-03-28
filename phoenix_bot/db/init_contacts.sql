-- Страница «Контакты»: описание, почта, телефон, адрес, телеграм.
CREATE TABLE IF NOT EXISTS contacts_page (
  id          INTEGER PRIMARY KEY DEFAULT 1 CHECK (id = 1),
  description TEXT NOT NULL DEFAULT '',
  email       TEXT NOT NULL DEFAULT '',
  phone       TEXT NOT NULL DEFAULT '',
  address     TEXT NOT NULL DEFAULT '',
  telegram    TEXT NOT NULL DEFAULT ''
);

INSERT INTO contacts_page (id, description, email, phone, address, telegram)
VALUES (
  1,
  'Свяжитесь с нами по почте, телефону или в Telegram.',
  'contact@phoenixlbsu.com',
  '+375 (29) 811-10-10',
  'Лицей БГУ, Ульяновская 8, Минск, Беларусь',
  '@phoenixfromlbsu'
)
ON CONFLICT (id) DO NOTHING;


-- Сообщения от пользователей с сайта.
CREATE TABLE IF NOT EXISTS contact_messages (
  id               SERIAL PRIMARY KEY,
  name             TEXT NOT NULL DEFAULT '',
  email            TEXT NOT NULL DEFAULT '',
  message_text     TEXT NOT NULL DEFAULT '',
  telegram_username TEXT NOT NULL DEFAULT '',
  created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
