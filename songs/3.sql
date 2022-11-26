-- SELECT name FROM songs
-- ORDER BY duration_ms
-- DESC LIMIT 5;

SELECT Top(5) name FROM songs
ORDER BY duration_ms DESC;