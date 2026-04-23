-- Создание таблиц
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(100),
    reg_date DATE,
    subscription_type VARCHAR(20) -- Free, Basic, Premium
);

CREATE TABLE content (
    content_id SERIAL PRIMARY KEY,
    title VARCHAR(200),
    genre VARCHAR(50),
    release_year INT,
    rating DECIMAL(3,1)
);

CREATE TABLE viewing_history (
    view_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    content_id INT REFERENCES content(content_id),
    view_date DATE,
    duration_minutes INT
);