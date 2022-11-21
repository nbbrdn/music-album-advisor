CREATE TABLE IF NOT EXISTS users (
    telegram_id BIGINT NOT NULL,
    user_name VARCHAR(250) NOT NULL,
    first_name VARCHAR(250) NOT NULL,
    last_name VARCHAR(250) NOT NULL,
    language_code VARCHAR(10),
    register_date TIMESTAMP,
    last_activity_date TIMESTAMP,
    stop_date TIMESTAMP,
    restart_date TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT 'f',
    PRIMARY KEY (telegram_id)
);

CREATE TABLE IF NOT EXISTS albums (
    id SERIAL PRIMARY KEY,
    artist VARCHAR(250) NOT NULL,
    title VARCHAR(250) NOT NULL,
    year SMALLINT NOT NULL,
    cover_id VARCHAR(250),
    description TEXT,
    wiki_url VARCHAR(250),
    spotify_url VARCHAR(250),
    apple_url VARCHAR(250),
    youtube_url VARCHAR(250),
    other_url VARCHAR(250)
);
