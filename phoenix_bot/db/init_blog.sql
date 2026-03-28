-- Описание страницы «Блог» (одна строка) и записи блога.

CREATE TABLE IF NOT EXISTS blog_page (
  id          INTEGER PRIMARY KEY DEFAULT 1 CHECK (id = 1),
  description TEXT NOT NULL DEFAULT ''
);

INSERT INTO blog_page (id, description)
VALUES (
  1,
  'Блог команды Phoenix — здесь мы делимся закулисьем подготовки, выступлений и жизни команды.'
)
ON CONFLICT (id) DO NOTHING;


-- Записи блога: номер (для сортировки и отображения), описание и фото (Telegram file_id).
CREATE TABLE IF NOT EXISTS blog_posts (
  id          SERIAL PRIMARY KEY,
  number      INTEGER NOT NULL DEFAULT 1,
  description TEXT NOT NULL DEFAULT '',
  photo       TEXT NOT NULL DEFAULT ''
);

