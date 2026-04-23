-- Блок 1: Простые SELECT (5 шт)
SELECT * FROM users WHERE subscription_type = 'Premium';
SELECT title, rating FROM content WHERE rating > 8.5;
SELECT * FROM viewing_history WHERE duration_minutes < 30;
SELECT username FROM users WHERE reg_date > '2025-01-01';
SELECT COUNT(*) FROM content WHERE genre = 'Sci-Fi';

-- Блок 2: Агрегации GROUP BY (5 шт)
SELECT genre, AVG(rating) FROM content GROUP BY genre HAVING AVG(rating) > 7;
SELECT subscription_type, COUNT(*) FROM users GROUP BY subscription_type;
SELECT user_id, SUM(duration_minutes) FROM viewing_history GROUP BY user_id HAVING SUM(duration_minutes) > 500;
SELECT release_year, COUNT(*) FROM content GROUP BY release_year;
SELECT view_date, COUNT(*) FROM viewing_history GROUP BY view_date ORDER BY view_date DESC;

-- Блок 3: JOIN (10 шт)
SELECT u.username, v.view_date FROM users u JOIN viewing_history v ON u.user_id = v.user_id;
SELECT c.title, v.view_date FROM content c JOIN viewing_history v ON c.content_id = v.content_id;
-- ... (добавь аналогичные джойны для набора 10 штук)

-- Блок 4: Оконные функции (5 шт)
SELECT user_id, view_date, duration_minutes, 
SUM(duration_minutes) OVER(PARTITION BY user_id ORDER BY view_date) as running_total
FROM viewing_history;

SELECT content_id, title, rating, 
RANK() OVER(ORDER BY rating DESC) as movie_rank
FROM content;
-- ... (добавь еще 3 по аналогии)

-- Блок 5: CTE и подзапросы (5 шт)
WITH ActiveUsers AS (
    SELECT user_id FROM viewing_history GROUP BY user_id HAVING COUNT(*) > 5
)
SELECT * FROM users WHERE user_id IN (SELECT user_id FROM ActiveUsers);