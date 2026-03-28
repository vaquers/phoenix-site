-- Описание страницы «Спонсоры» и список спонсоров.

CREATE TABLE IF NOT EXISTS sponsors_page (
  id          INTEGER PRIMARY KEY DEFAULT 1 CHECK (id = 1),
  description TEXT NOT NULL DEFAULT ''
);

INSERT INTO sponsors_page (id, description)
VALUES (
  1,
  'Наши партнёры помогают развивать инфраструктуру, поддерживают участие в соревнованиях и образовательные инициативы команды Phoenix.'
)
ON CONFLICT (id) DO NOTHING;


-- Спонсоры: фото (Telegram file_id), subtitle, title, description, status (медаль).
-- status: -1 -> нет медали, 1 -> gold, 2 -> silver, 3 -> bronze.
CREATE TABLE IF NOT EXISTS sponsors (
  id          SERIAL PRIMARY KEY,
  photo       TEXT NOT NULL DEFAULT '',
  subtitle    TEXT NOT NULL DEFAULT '',
  title       TEXT NOT NULL DEFAULT '',
  description TEXT NOT NULL DEFAULT '',
  status      INTEGER NOT NULL DEFAULT -1
);

