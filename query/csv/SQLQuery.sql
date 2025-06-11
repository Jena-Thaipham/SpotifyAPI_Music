-- Artist Category
SELECT 
    CASE 
        WHEN popularity >= 74.43 AND followers < 3388441 THEN 'Emerging'
        WHEN popularity >= 80 AND followers >= 5000000 THEN 'Famous'
        ELSE 'Other'
    END AS artist_category,
    
    CASE 
        WHEN popularity >= 74.43 AND followers < 3388441 THEN 'High popularity (≥ 74.43) & Low followers (< 3,388,441)'
        WHEN popularity >= 80 AND followers >= 5000000 THEN 'High popularity (≥ 80) & High followers (≥ 5,000,000)'
        ELSE 'Does not meet criteria for Emerging or Famous'
    END AS category_criteria,
    
    COUNT(*) AS artist_count
FROM artists
GROUP BY artist_category, category_criteria;

-- PopularityFollowerComparison
SELECT 
    CASE 
        WHEN ar.popularity >= 74.43 AND ar.followers < 3388441 THEN 'Emerging'
        WHEN ar.popularity >= 80 AND ar.followers >= 5000000 THEN 'Famous'
        ELSE 'Other'
    END AS artist_category,
    ROUND(AVG(ar.popularity), 2) AS avg_popularity,
    CAST(AVG(ar.followers) AS INTEGER) AS avg_followers
FROM artists ar
GROUP BY artist_category
HAVING artist_category IN ('Emerging', 'Famous');

-- Overall Comparison
SELECT 
    artist_category,
    ROUND(AVG(playlist_count), 2) AS avg_playlist_count,
    ROUND(AVG(album_count), 2) AS avg_album_count,
    ROUND(AVG(track_count), 2) AS avg_track_count,
    ROUND(AVG(genre_count), 2) AS avg_genre_count,
    ROUND(AVG(track_popularity), 2) AS avg_track_popularity,
    ROUND(AVG(album_popularity), 2) AS avg_album_popularity
FROM (
    SELECT 
        ar.artist_id,
        COUNT(DISTINCT pt.playlist_id) AS playlist_count,
        COUNT(DISTINCT al.album_id) AS album_count,
        COUNT(DISTINCT t.track_id) AS track_count,
        COUNT(DISTINCT g.genre) AS genre_count,
        AVG(t.popularity) AS track_popularity,
        AVG(al.popularity) AS album_popularity,
        CASE 
            WHEN ar.popularity >= 74.43 AND ar.followers < 3388441 THEN 'Emerging'
            WHEN ar.popularity >= 80 AND ar.followers >= 5000000 THEN 'Famous'
        END AS artist_category
    FROM artists ar
    LEFT JOIN tracks t ON ar.artist_id = t.artist_id
    LEFT JOIN playlist_tracks pt ON t.track_id = pt.track_id
    LEFT JOIN albums al ON ar.artist_id = al.artist_id
    LEFT JOIN genres g ON ar.artist_id = g.artist_id
    GROUP BY ar.artist_id
) sub
WHERE artist_category IS NOT NULL
GROUP BY artist_category;

-- Followers Gap Comparison (Owner - Artist)
SELECT 
    p.playlist_name,
    u.followers AS playlist_owner_followers,

    -- Average followers of Emerging Artists in the playlist
    CAST(AVG(CASE 
              WHEN ar.popularity >= 74.43 AND ar.followers < 3388441 THEN ar.followers 
             END) AS INTEGER) AS avg_emerging_artist_follower,

    -- Average followers of Famous Artists in the playlist
    CAST(AVG(CASE 
              WHEN ar.popularity >= 80 AND ar.followers >= 5000000 THEN ar.followers 
             END) AS INTEGER) AS avg_famous_artist_follower,

    -- Follower Gap: Owner - Emerging Artist
    CAST((u.followers - AVG(CASE 
                WHEN ar.popularity >= 74.43 AND ar.followers < 3388441 THEN ar.followers 
              END)) AS INTEGER) AS emerging_follower_gap,

    -- Follower Gap: Owner - Famous Artist
    CAST((u.followers - AVG(CASE 
                WHEN ar.popularity >= 80 AND ar.followers >= 5000000 THEN ar.followers 
              END)) AS INTEGER) AS famous_follower_gap

FROM playlists p
JOIN users u ON p.owner_id = u.user_id
JOIN playlist_tracks pt ON p.playlist_id = pt.playlist_id
JOIN tracks t ON pt.track_id = t.track_id
JOIN artists ar ON t.artist_id = ar.artist_id

GROUP BY p.playlist_id
HAVING 
    COUNT(CASE 
             WHEN ar.popularity >= 74.43 AND ar.followers < 3388441 THEN 1 
          END) > 0
AND 
    COUNT(CASE 
             WHEN ar.popularity >= 80 AND ar.followers >= 5000000 THEN 1 
          END) > 0

ORDER BY p.playlist_name;

-- Album By Year Comparison
SELECT 
    CASE 
        WHEN ar.popularity >= 74.43 AND ar.followers < 3388441 THEN 'Emerging'
        WHEN ar.popularity >= 80 AND ar.followers >= 5000000 THEN 'Famous'
    END AS artist_category,
    STRFTIME('%Y', al.release_date) AS year,
    COUNT(DISTINCT al.album_id) AS album_count
FROM albums al
JOIN artists ar ON al.artist_id = ar.artist_id
WHERE STRFTIME('%Y', al.release_date) IS NOT NULL
  AND (
        (ar.popularity >= 74.43 AND ar.followers < 3388441)
     OR (ar.popularity >= 80 AND ar.followers >= 5000000)
  )
GROUP BY artist_category, year
ORDER BY year DESC;

-- Popularity By Year Comparison
SELECT 
    CASE 
        WHEN ar.popularity >= 74.43 AND ar.followers < 3388441 THEN 'Emerging'
        WHEN ar.popularity >= 80 AND ar.followers >= 5000000 THEN 'Famous'
    END AS artist_category,
    STRFTIME('%Y', al.release_date) AS year,
    ROUND(AVG(ar.popularity), 2) AS avg_artist_popularity
FROM artists ar
JOIN albums al ON ar.artist_id = al.artist_id
JOIN (
    SELECT 
        artist_id,
        CASE 
            WHEN popularity >= 74.43 AND followers < 3388441 THEN 'Emerging'
            WHEN popularity >= 80 AND followers >= 5000000 THEN 'Famous'
        END AS artist_category
    FROM artists
) cat ON ar.artist_id = cat.artist_id
WHERE year IS NOT NULL
  AND artist_category IS NOT NULL
GROUP BY artist_category, year
ORDER BY year DESC;

-- Followers By Year Comparison
SELECT 
    CASE 
        WHEN ar.popularity >= 74.43 AND ar.followers < 3388441 THEN 'Emerging'
        WHEN ar.popularity >= 80 AND ar.followers >= 5000000 THEN 'Famous'
    END AS artist_category,
    STRFTIME('%Y', al.release_date) AS year,
    CAST(AVG(ar.followers) AS INTEGER) AS avg_artist_followers
FROM artists ar
JOIN albums al ON ar.artist_id = al.artist_id
WHERE STRFTIME('%Y', al.release_date) IS NOT NULL
  AND (
        (ar.popularity >= 74.43 AND ar.followers < 3388441) OR
        (ar.popularity >= 80 AND ar.followers >= 5000000)
      )
GROUP BY artist_category, year
ORDER BY year DESC;

-- Track By Year Comparison
SELECT 
    CASE 
        WHEN ar.popularity >= 74.43 AND ar.followers < 3388441 THEN 'Emerging'
        WHEN ar.popularity >= 80 AND ar.followers >= 5000000 THEN 'Famous'
    END AS artist_category,
    STRFTIME('%Y', al.release_date) AS year,
    CAST(AVG(track_counts.track_count) AS INTEGER) AS avg_track_count
FROM artists ar
JOIN albums al ON ar.artist_id = al.artist_id
JOIN (
    SELECT 
        t.artist_id,
        COUNT(t.track_id) AS track_count
    FROM tracks t
    GROUP BY t.artist_id
) track_counts ON ar.artist_id = track_counts.artist_id
WHERE STRFTIME('%Y', al.release_date) IS NOT NULL
  AND (
        (ar.popularity >= 74.43 AND ar.followers < 3388441) OR
        (ar.popularity >= 80 AND ar.followers >= 5000000)
      )
GROUP BY artist_category, year
ORDER BY year DESC;

-------------------------------------------------------------------------------------------------------------
WITH artist_stats AS (
    SELECT 
        ar.artist_id,
        ar.artist_name,
        ar.popularity,
        ar.followers,
        COUNT(DISTINCT t.track_id) AS track_count,
        COUNT(DISTINCT al.album_id) AS album_count,
        COUNT(DISTINCT pt.playlist_id) AS playlist_count,
        ROUND(AVG(t.popularity), 2) AS track_popularity,
        ROUND(AVG(al.popularity), 2) AS album_popularity
    FROM artists ar
    LEFT JOIN tracks t ON ar.artist_id = t.artist_id
    LEFT JOIN albums al ON ar.artist_id = al.artist_id
    LEFT JOIN playlist_tracks pt ON t.track_id = pt.track_id
    WHERE ar.popularity >= 74.43 AND ar.followers < 3388441
    GROUP BY ar.artist_id, ar.artist_name, ar.popularity, ar.followers
),
avg_stats AS (
    SELECT 
        AVG(followers) AS avg_followers,
        AVG(popularity) AS avg_artist_popularity,
        AVG(track_count) AS avg_track_count,
        AVG(album_count) AS avg_album_count,
        AVG(playlist_count) AS avg_playlist_count,
        AVG(track_popularity) AS avg_track_popularity,
        AVG(album_popularity) AS avg_album_popularity
    FROM artist_stats
),
artist_with_flags AS (
    SELECT 
        a.artist_id,
        a.artist_name,
        a.popularity,
        a.followers,
        a.track_count,
        a.album_count,
        a.playlist_count,
        a.track_popularity,
        a.album_popularity,

        CASE WHEN a.followers > avg.avg_followers THEN 'Yes' ELSE 'No' END AS top_by_follower,
        CASE WHEN a.popularity > avg.avg_artist_popularity THEN 'Yes' ELSE 'No' END AS top_by_popularity,
        CASE WHEN a.track_count > avg.avg_track_count THEN 'Yes' ELSE 'No' END AS top_by_track,
        CASE WHEN a.album_count > avg.avg_album_count THEN 'Yes' ELSE 'No' END AS top_by_album,
        CASE WHEN a.playlist_count > avg.avg_playlist_count THEN 'Yes' ELSE 'No' END AS top_by_playlist,

        CASE 
            WHEN a.track_popularity IS NULL THEN NULL
            WHEN a.track_popularity > avg.avg_track_popularity THEN 'Yes'
            ELSE 'No'
        END AS top_by_track_rate,

        CASE 
            WHEN a.album_popularity IS NULL THEN NULL
            WHEN a.album_popularity > avg.avg_album_popularity THEN 'Yes'
            ELSE 'No'
        END AS top_by_album_rate,

        CASE 
            WHEN a.followers > avg.avg_followers 
             AND a.track_count > avg.avg_track_count 
             AND a.album_count > avg.avg_album_count 
             AND a.playlist_count > avg.avg_playlist_count
            THEN 'Yes' ELSE 'No'
        END AS top_by_all_count,

        CASE 
            WHEN a.track_popularity IS NULL OR a.album_popularity IS NULL THEN NULL
            WHEN a.track_popularity > avg.avg_track_popularity 
             AND a.album_popularity > avg.avg_album_popularity 
             AND a.popularity > avg.avg_artist_popularity
            THEN 'Yes' ELSE 'No'
        END AS top_by_all_rate
    FROM artist_stats a
    CROSS JOIN avg_stats avg
),
final_output AS (
    SELECT 
        awf.*,
        GROUP_CONCAT(DISTINCT g.genre) AS genres
    FROM artist_with_flags awf
    LEFT JOIN genres g ON awf.artist_id = g.artist_id
    GROUP BY awf.artist_id, awf.artist_name, awf.popularity, awf.followers,
             awf.track_count, awf.album_count, awf.playlist_count,
             awf.track_popularity, awf.album_popularity,
             awf.top_by_follower, awf.top_by_popularity, awf.top_by_track,
             awf.top_by_album, awf.top_by_playlist, awf.top_by_track_rate,
             awf.top_by_album_rate,
             awf.top_by_all_count, awf.top_by_all_rate
)
SELECT *
FROM final_output
ORDER BY popularity DESC;

-- ALbum by Year of All Emerging Artists
WITH emerging_artists AS (
    SELECT 
        ar.artist_id,
        ar.artist_name,
        ar.popularity,
        ar.followers
    FROM artists ar
    WHERE ar.popularity >= 74.43 AND ar.followers < 3388441
)

SELECT 
    ea.artist_name,
    SUBSTR(al.release_date, 1, 4) AS release_year,
    COUNT(DISTINCT al.album_id) AS album_count
FROM emerging_artists ea
LEFT JOIN albums al ON ea.artist_id = al.artist_id
GROUP BY ea.artist_name, SUBSTR(al.release_date, 1, 4)
ORDER BY ea.artist_name, release_year;

-- Top Track of EArtist

WITH qualified_emerging_artists AS (
    SELECT 
        artist_id,
        artist_name
    FROM artists
    WHERE popularity >= 74.43 AND followers < 3388441
),

tracks_with_popularity AS (
    SELECT 
        ar.artist_id,
        ar.artist_name,
        t.track_name,
        t.popularity,
        DENSE_RANK() OVER (PARTITION BY ar.artist_id ORDER BY t.popularity DESC) AS rnk
    FROM qualified_emerging_artists qea
    LEFT JOIN artists ar ON qea.artist_id = ar.artist_id
    LEFT JOIN tracks t ON ar.artist_id = t.artist_id
)

SELECT 
    artist_name,
    track_name,
    popularity AS track_popularity
FROM tracks_with_popularity
WHERE rnk = 1
ORDER BY track_popularity DESC;




































































-- Emerging Artists Overview
SELECT 
    ar.artist_name,
    ar.popularity AS artist_popularity,
    ar.followers AS artist_followers,
    GROUP_CONCAT(DISTINCT g.genre) AS genres,  
    COUNT(DISTINCT al.album_id) AS album_count,
    COUNT(DISTINCT tr.track_id) AS track_count,
    COUNT(DISTINCT pt.playlist_id) AS playlist_count

FROM artists ar

INNER JOIN genres g ON ar.artist_id = g.artist_id
INNER JOIN albums al ON ar.artist_id = al.artist_id
INNER JOIN tracks tr ON ar.artist_id = tr.artist_id
INNER JOIN playlist_tracks pt ON tr.track_id = pt.track_id

WHERE ar.popularity >= 74.43 
  AND ar.followers < 3388441

GROUP BY ar.artist_id
ORDER BY ar.popularity DESC;

--  Genres By Emerging Artists
SELECT 
    g.genre,
    COUNT(DISTINCT ar.artist_id) AS artist_count,
    ROUND(AVG(ar.popularity), 2) AS avg_popularity,
    CAST(AVG(ar.followers) AS INTEGER) AS avg_followers
FROM artists ar
JOIN genres g ON ar.artist_id = g.artist_id
WHERE ar.popularity >= 74.43
  AND ar.followers < 3388441
GROUP BY g.genre
ORDER BY artist_count DESC;

-- Album By Year of Emerging Artists
SELECT 
    SUBSTR(a.release_date, 1, 4) AS release_year,
    COUNT(DISTINCT a.album_id) AS album_count
FROM albums a
JOIN artists ar ON a.artist_id = ar.artist_id
WHERE ar.popularity >= 74.43 AND ar.followers < 3388441
GROUP BY release_year
ORDER BY release_year;

-- Released Albums By Emerging Artists
SELECT 
    ar.artist_name,
    SUBSTR(a.release_date, 1, 4) AS release_year,
    COUNT(DISTINCT a.album_id) AS album_count
FROM albums a
JOIN artists ar ON a.artist_id = ar.artist_id
WHERE ar.popularity >= 74.43 AND ar.followers < 3388441
GROUP BY ar.artist_id, release_year
ORDER BY ar.artist_name, release_year;

-- Track Album Popularity of Emerging Artists
SELECT 
    ar.artist_name,
    ar.popularity AS artist_popularity,
    ROUND(AVG(DISTINCT t.popularity), 2) AS avg_track_popularity,
    ROUND(AVG(DISTINCT al.popularity), 2) AS avg_album_popularity
FROM artists ar
LEFT JOIN tracks t ON ar.artist_id = t.artist_id
INNER JOIN albums al ON ar.artist_id = al.artist_id
WHERE ar.popularity >= 74.43 AND ar.followers < 3388441
GROUP BY ar.artist_id
ORDER BY avg_track_popularity DESC;

-- Top 10 Tracks of Emerging Artists
SELECT 
    t.track_name,
    ar.artist_name,
    g.genre,
    t.popularity AS track_popularity,
    ar.popularity AS artist_popularity,
    t.duration_ms,
    COUNT(DISTINCT pt.playlist_id) AS playlist_count,
    COUNT(DISTINCT t.album_id) AS album_count
FROM tracks t
JOIN artists ar ON t.artist_id = ar.artist_id
JOIN genres g ON ar.artist_id = g.artist_id
LEFT JOIN playlist_tracks pt ON t.track_id = pt.track_id
WHERE ar.popularity >= 74.43
  AND ar.followers < 3388441
GROUP BY t.track_id
ORDER BY t.popularity DESC
LIMIT 10;

-- Top 10 Albums of Emerging Artists
SELECT 
    al.album_name,
    GROUP_CONCAT(DISTINCT ar.artist_name) AS artist_names,
    al.popularity AS album_popularity,
    ROUND(AVG(ar.popularity), 2) AS avg_artist_popularity,
    COUNT(DISTINCT t.track_id) AS track_count
FROM albums al
JOIN tracks t ON al.album_id = t.album_id
JOIN artists ar ON t.artist_id = ar.artist_id
WHERE ar.popularity >= 74.43
  AND ar.followers < 3388441
GROUP BY al.album_id
ORDER BY al.popularity DESC
LIMIT 10;












