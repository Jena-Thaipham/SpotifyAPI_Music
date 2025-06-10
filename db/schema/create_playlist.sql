CREATE TABLE IF NOT EXISTS `playlists` (
    `playlist_id` TEXT PRIMARY KEY,
    `playlist_name` TEXT,
    `owner_id` TEXT,
    `total_tracks` INTEGER,
    `public` BOOLEAN,
    `playlist_uri` TEXT,
    FOREIGN KEY (`owner_id`) REFERENCES `users`(`user_id`)
);
