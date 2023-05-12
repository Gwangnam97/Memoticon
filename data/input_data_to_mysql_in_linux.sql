-- CREATE TABLE sys.memo (
--   id INT AUTO_INCREMENT PRIMARY KEY,
--   url TEXT,
--   hashtag TEXT
-- );

-- 1. MySQL의 설정 파일 "C:\ProgramData\MySQL\MySQL Server {버전}\my.ini" (my.cnf 또는 my.ini)을 열고
-- 2. [mysqld] 섹션에 local_infile=1라는 설정을 추가
-- 3. MySQL 서버를 재시작 : win+r -> "services.msc" -> MySQL80 중지 후 재시작

-- add "OPT_LOCAL_INFILE=1" Manage Server Connections -> Advancd -> Others

truncate main.memo;
set global local_infile=1;
LOAD DATA LOCAL INFILE 'data.tsv' 
INTO TABLE main.memo
CHARACTER SET utf8mb4
FIELDS TERMINATED BY '\t'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(url,hashtag);