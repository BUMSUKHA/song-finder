-- DROP TABLE IF EXISTS user;

-- CREATE TABLE user(
--     userid integer PRIMARY KEY AUTOINCREMENT,
--     username text UNIQUE NOT NULL,
--     password text NOT NULL,
--     email text NOT NULL,
--     gender text CHECK(gender in ('Male', 'Female', 'Other')),
--     create_at timestamp DEFAULT (DATETIME('now', 'localtime'))
-- );

-- INSERT INTO user(username, password, email, gender)
-- VALUES ('test', '123', 'test@gmail.com', 'Male');

-- DELETE FROM user;

CREATE TABLE favorite (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    userid INTEGER,
    songid TEXT NOT NULL,
    create_at TIMESTAMP DEFAULT (DATETIME('now', 'localtime')),
    FOREIGN KEY (userid) REFERENCES user(userid),
    UNIQUE(userid, songid)  -- 유저가 같은 노래를 중복으로 즐겨찾기하지 않도록 유니크 제약
);