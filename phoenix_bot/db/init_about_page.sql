-- Таблица «Про нас»: одна запись для блока на сайте и в боте.
-- Выполни в psql: \i путь/к/init_about_page.sql  или скопируй команды ниже.

CREATE TABLE IF NOT EXISTS about_page (
  id             INTEGER PRIMARY KEY DEFAULT 1 CHECK (id = 1),
  description    TEXT NOT NULL DEFAULT '',
  years_in_competitions INTEGER NOT NULL DEFAULT 0,
  team_size      INTEGER NOT NULL DEFAULT 0
);

-- Одна строка по умолчанию (если ещё нет)
INSERT INTO about_page (id, description, years_in_competitions, team_size)
VALUES (1, 'От идеи — к результату. Мы первая беларуская команда Лиги Инженеров из Лицея БГУ! Создаем роботов сообща и вместе ищем нестандартные решения!', 2, 10)
ON CONFLICT (id) DO NOTHING;
