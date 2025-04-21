CREATE TABLE IF NOT EXISTS `users` (
            `user_id` TEXT PRIMARY KEY,
            `followers` INTEGER,
            `user_uri` TEXT
);
