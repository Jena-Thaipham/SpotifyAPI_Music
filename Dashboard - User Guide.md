Overview
This document provides guidance on how to interact with the two dashboards created to analyze and compare music artists based on Spotify data.

🔹 Dashboard 1: Emerging vs. Famous Artists Overview
This dashboard provides a comprehensive overview comparing Emerging and Famous artists based on their popularity, follower count, and key performance metrics. The charts are color-coded consistently across the dashboard to distinguish between the two groups:
Emerging Artists: High popularity but low follower count


Famous Artists: High popularity and high follower count


Thresholds are calculated based on statistical analysis of the full dataset:
Follower thresholds are based on log-scale mean and standard deviation:
 low_log = round(mean_log - std_log, 2)
 high_log = round(mean_log + std_log, 2)


Popularity thresholds are based on:
 low_threshold = round(mean_pop - std_pop, 2)
 high_threshold = round(mean_pop + std_pop, 2)
🔹 Chart Descriptions
Artist Count by Follower Group


Displays how artists are distributed across low, medium, and high follower groups.


Helps to understand the general follower landscape.


Artist Count by Popularity Group


Shows how many artists fall into low, medium, and high popularity categories.


Provides insight into artist visibility and reach.


Key Metrics Comparison Between Emerging and Famous Artists


Compares average values for:
 Album Count, Album Popularity, Genre Count, Playlist Count, Track Count, and Track Popularity.


Bar chart format; provides a snapshot of overall engagement and diversity.


Popularity vs. Followers: Emerging vs. Famous Artists


Visualizes the relationship between artist popularity and follower count.


Highlights distinct positioning of each group based on defined thresholds.


Playlist Owner and Artist Follower Comparison


Compares average follower counts of emerging artists and all artists per playlist.


Also shows playlist owner’s follower count for additional context.


Yearly Trend of Artist Popularity


Line chart showing average popularity over time, separated by artist category.


Tooltip reveals year-specific average popularity.


Yearly Trend of Artist Followers


Line chart illustrating average followers over time for Emerging and Famous artists.


Tooltip shows yearly average follower values.


Yearly Trend of Average Released Albums


Tracks how many albums were released each year by Emerging artists.


Tooltip shows year and album count.


Yearly Trend of Tracks


Displays the number of tracks released per year by Emerging artists.


Tooltip shows year and track count.



🎨 Color Legend (Unified across dashboard)

📌 Usage Notes
Hover tooltips on line charts provide detailed yearly statistics.
🔗 Navigation Tip: Use the navigation button in Dashboard 1 to jump directly to Dashboard 2 (In-Depth Exploration of Emerging Artists)  for a focused exploration of Emerging Artists.
🔹Dashboard 2: In-Depth Exploration of Emerging Artists
This dashboard provides a detailed analysis of Emerging Artists, defined as artists with high popularity but low follower count, based on data thresholds established in Dashboard 1.

🔹 Chart Descriptions
Genre-Based Overview of Emerging Artists’ Activity


Visualizes each Emerging Artist’s track count, album count, and playlist count.
Filter by Artist Name and Genre.
Color: Each genre is color-coded.
Tooltip shows detailed activity per artist.


Top Genres Among Emerging Artists


Bar chart showing:
Artist Count per genre
Average Artist Popularity (bar height)
Average Follower Count as label
Filter by genre to narrow down insights.


Relationship Between Track and Album Popularity of Emerging Artists


Scatter plot comparing:
Avg Track Popularity (x-axis)
Avg Album Popularity (y-axis)
Label each dot with Artist Popularity to identify standout performers.


Emerging Artists: Album Release Trend Over the Years


Line chart showing the total number of albums released each year by all Emerging Artists.
Helps identify active years and growth trends.


Annual Album Output per Emerging Artist


Vertical bar chart showing number of albums per year for each Emerging Artist.
Filter available by Artist Name and Release Year.
Label shows exact album count for that year.


Most Popular Albums of Emerging Artists


Top 10 albums ranked by Album Popularity.
Tooltip includes Artist Name(s) and Track Count on the album.
Useful to explore what types of albums resonate most.


Most Popular Tracks of Emerging Artists


Top 10 tracks ranked by Track Popularity.
Color represents Genre.
Label indicates number of playlists that include the track.
Bar width or height represents Track Duration, giving additional dimension to popularity.



🎨 Color Scheme
🎨 Genres have distinct colors for differentiation

🧭 Tips for Using This Dashboard
Use filters to dive deep into specific artists, genres, or years.
Tooltips provide rich detail — hover over points, bars, or lines for deeper insights.
Combine this dashboard with Dashboard 1 for a complete story: from overview to deep dive.


