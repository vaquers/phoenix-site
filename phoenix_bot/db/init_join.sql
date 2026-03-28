-- Описание страницы «Стать участником» (одна строка).
CREATE TABLE IF NOT EXISTS join_page (
  id          INTEGER PRIMARY KEY DEFAULT 1 CHECK (id = 1),
  description TEXT NOT NULL DEFAULT ''
);

INSERT INTO join_page (id, description)
VALUES (
  1,
  'Присоединяйтесь к сообществу, чтобы учиться новому, делиться опытом и создавать полезные проекты вместе.'
)
ON CONFLICT (id) DO NOTHING;


-- Анкеты (заявки) со страницы «Стать участником».
CREATE TABLE IF NOT EXISTS join_applications (
  id          SERIAL PRIMARY KEY,
  full_name   TEXT NOT NULL DEFAULT '',
  grade       TEXT NOT NULL DEFAULT '',
  profile     TEXT NOT NULL DEFAULT '',
  email       TEXT NOT NULL DEFAULT '',
  telegram    TEXT NOT NULL DEFAULT '',
  role        TEXT NOT NULL DEFAULT '',
  experience  TEXT NOT NULL DEFAULT '',
  motivation  TEXT NOT NULL DEFAULT '',
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
