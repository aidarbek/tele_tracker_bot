CREATE DATABASE tracker CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
use tracker;

CREATE TABLE tracker (
  owner INT,
  bot VARCHAR(100) UNIQUE
);

CREATE TABLE subs (
  bot VARCHAR(100),
  name VARCHAR(100)
);
#SET NAMES utf8;
#ALTER DATABASE tracker CHARACTER SET = utf8 COLLATE = utf8_general_ci;
#ALTER TABLE subs CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
#ALTER TABLE tracker.subs MODIFY COLUMN name VARCHAR(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;