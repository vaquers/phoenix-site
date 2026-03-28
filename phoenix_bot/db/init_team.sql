-- Описание страницы «Команда» (одна строка).
CREATE TABLE IF NOT EXISTS team_page (
  id          INTEGER PRIMARY KEY DEFAULT 1 CHECK (id = 1),
  description TEXT NOT NULL DEFAULT ''
);

INSERT INTO team_page (id, description)
VALUES (1, 'Это страстные и увлечённые своей работой участники команды «Phoenix LBSU». Мы соединяем экспертизу в программировании, моделировании, дизайне, проектировании и работе с сообществом, чтобы создавать инновационные решения в области робототехники.')
ON CONFLICT (id) DO NOTHING;


-- Члены команды: фото (file_id или путь), имя, специальность, описание, статус.
CREATE TABLE IF NOT EXISTS team_members (
  id          SERIAL PRIMARY KEY,
  name        TEXT NOT NULL DEFAULT '',
  specialty   TEXT NOT NULL DEFAULT '',
  description TEXT NOT NULL DEFAULT '',
  status      TEXT NOT NULL DEFAULT '',
  photo       TEXT NOT NULL DEFAULT ''
);
