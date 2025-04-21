CREATE TABLE IF NOT EXISTS `tracks` (
	`track_id` TEXT PRIMARY KEY,
	`track_name` TEXT,
	`artist_id` TEXT NOT NULL,
	`album_id` TEXT NOT NULL ,
	`track_uri` TEXT,
	`track_number` INTEGER,
	`markets` TEXT,
	`local` BOOLEAN,
	`disc_number` INTEGER,
	`explicit` BOOLEAN,
	`duration_ms` INTEGER,
	`popularity` INTEGER CHECK(popularity BETWEEN 0 AND 100)
);
