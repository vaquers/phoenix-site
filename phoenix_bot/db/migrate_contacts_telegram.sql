-- Убрать время собраний, добавить поле telegram.
ALTER TABLE contacts_page DROP COLUMN IF EXISTS meeting_time;
ALTER TABLE contacts_page ADD COLUMN IF NOT EXISTS telegram TEXT NOT NULL DEFAULT '';

UPDATE contacts_page SET telegram = '@phoenixfromlbsu' WHERE id = 1 AND (telegram = '' OR telegram IS NULL);
