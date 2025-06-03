-- Top popular tracks
SELECT t.track_name, ar.artist_name, al.album_name, t.popularity
FROM tracks t
JOIN artists ar ON t.artist_id = ar.artist_id
JOIN albums al ON t.album_id = al.album_id
WHERE t.popularity > (SELECT AVG(popularity) FROM tracks)
ORDER BY t.popularity DESC; 

-- Artists 
SELECT 
    ar.artist_name,
    ar.followers,
    COUNT(DISTINCT t.track_id) AS track_count,
    COUNT(DISTINCT t.album_id) AS album_count,
    COUNT(DISTINCT pt.playlist_id) AS playlist_count,
    ar.popularity AS artist_popularity,
    AVG(t.popularity) AS avg_track_popularity,
    AVG(al.popularity) AS avg_album_popularity
FROM artists ar
LEFT JOIN tracks t ON ar.artist_id = t.artist_id
LEFT JOIN albums al ON t.album_id = al.album_id
LEFT JOIN playlist_tracks pt ON t.track_id = pt.track_id
GROUP BY ar.artist_id
ORDER BY ar.followers DESC;

-- Most Popular Genres by Artists
SELECT genre, COUNT(*) AS genre_count
FROM artist_genres
GROUP BY genre
ORDER BY genre_count DESC;

-- Genres Popularity Based on Track, Artist and Album Popularity
SELECT 
    arg.genre,
    COUNT(DISTINCT t.artist_id) AS total_artists,  
    AVG(t.popularity) OVER (PARTITION BY arg.genre, t.artist_id) AS avg_artist_popularity,  
    COUNT(*) AS total_tracks,  
    AVG(t.popularity) AS avg_track_popularity,  
    COUNT(DISTINCT t.album_id) AS total_albums,  
    AVG(t.popularity) OVER (PARTITION BY arg.genre, t.album_id) AS avg_album_popularity  
FROM tracks t
JOIN artist_genres arg ON CAST(t.artist_id AS INTEGER) = arg.artist_id
GROUP BY arg.genre
ORDER BY total_tracks DESC;

-- Tracks by Release Year
SELECT SUBSTR(al.release_date, 1, 4) AS release_year, COUNT(t.track_id) AS num_tracks
FROM tracks t
JOIN albums al ON t.album_id = al.album_id
GROUP BY release_year
ORDER BY release_year;

-- Albums by Release Year
SELECT SUBSTR(al.release_date, 1, 4) AS release_year, COUNT(DISTINCT al.album_id) AS num_albums
FROM albums al
GROUP BY release_year
ORDER BY release_year;

-- Tracks with Explicit Content
SELECT t.track_name, ar.artist_name, t.popularity
FROM tracks t
JOIN artists ar ON t.artist_id = ar.artist_id
WHERE t.explicit = 1
ORDER BY t.popularity DESC


-- Tracks Duration by Genre
SELECT arg.genre, AVG(t.duration_ms)/60000 AS avg_duration_min
FROM tracks t
JOIN artist_genres arg ON CAST(t.artist_id AS INTEGER) = arg.artist_id
GROUP BY arg.genre
ORDER BY avg_duration_min DESC;

-- Tracks with Most Playlist Additions
SELECT t.track_name, COUNT(pt.playlist_id) AS num_playlists, popularity
FROM playlist_tracks pt
JOIN tracks t ON pt.track_id = t.track_id
GROUP BY t.track_id
ORDER BY num_playlists DESC

-- Top Albums by Total Tracks
SELECT album_name, artist_ids, total_tracks, popularity
FROM albums
WHERE total_tracks > (
    SELECT AVG(total_tracks) FROM albums
)
ORDER BY total_tracks DESC;

-- Most Collaborative Albums
SELECT 
    album_name, 
    LENGTH(artist_ids) - LENGTH(REPLACE(artist_ids, ',', '')) + 1 AS num_artists, 
    popularity,
    total_tracks
FROM albums
ORDER BY num_artists DESC;

-- Average Track and Artist Popularity per Album
SELECT 
    al.album_name, 
    al.popularity AS album_popularity,
    AVG(t.popularity) AS avg_track_popularity,
    AVG(ar.popularity) AS avg_artist_popularity
FROM albums al
JOIN tracks t ON al.album_id = t.album_id
JOIN artists ar ON al.artist_ids = ar.artist_id
GROUP BY al.album_id
ORDER BY avg_track_popularity DESC;

-- Playlists with Most Tracks by Track and Artist Popularity along with User's followers
SELECT 
    p.playlist_name,
    p.total_tracks,
    AVG(t.popularity) AS avg_track_popularity,
    AVG(ar.popularity) AS avg_artist_popularity,
    COUNT(DISTINCT ar.artist_id) AS unique_artist_count,
    u.followers AS user_followers
FROM playlists p
JOIN playlist_tracks pt ON p.playlist_id = pt.playlist_id
JOIN tracks t ON pt.track_id = t.track_id
JOIN artists ar ON t.artist_id = ar.artist_id
JOIN users u ON p.owner_id = u.user_id
GROUP BY p.playlist_id
ORDER BY p.total_tracks DESC;

-- Public playlist
SELECT 
    p.playlist_id,
    p.playlist_name,
    p.total_tracks,
    AVG(t.popularity) AS avg_track_popularity
FROM playlists p
JOIN users u ON p.owner_id = u.user_id
LEFT JOIN playlist_tracks pt ON p.playlist_id = pt.playlist_id
LEFT JOIN tracks t ON pt.track_id = t.track_id
WHERE p.public = 1
GROUP BY p.playlist_id
ORDER BY avg_track_popularity DESC;

-- Active Users with Many Playlists
SELECT 
    u.user_id AS owner_id,
    COUNT(DISTINCT p.playlist_id) AS playlist_count,
    u.followers,
    AVG(t.popularity) AS avg_track_popularity,
    AVG(p.total_tracks) AS avg_total_tracks
FROM users u
JOIN playlists p ON p.owner_id = u.user_id
JOIN playlist_tracks pt ON p.playlist_id = pt.playlist_id
JOIN tracks t ON pt.track_id = t.track_id
GROUP BY u.user_id
ORDER BY playlist_count DESC;

-- Artists by Popularity Range
SELECT 
  CASE 
    WHEN ar.popularity BETWEEN 0 AND 20 THEN '0-20'
    WHEN ar.popularity BETWEEN 21 AND 40 THEN '21-40'
    WHEN ar.popularity BETWEEN 41 AND 60 THEN '41-60'
    WHEN ar.popularity BETWEEN 61 AND 80 THEN '61-80'
    ELSE '81-100'
  END AS popularity_range,
  COUNT(DISTINCT ar.artist_id) AS artist_count,
  COUNT(DISTINCT t.track_id) AS track_count,
  COUNT(DISTINCT t.album_id) AS album_count
FROM artists ar
LEFT JOIN tracks t ON ar.artist_id = t.artist_id
GROUP BY popularity_range
ORDER BY popularity_range;
