# Overview

This document provides guidance on how to interact with the two dashboards created to analyze and compare music artists based on Spotify data.

---

## 🔹 Dashboard 1: Emerging vs. Famous Artists Overview

**Link:**  
[https://public.tableau.com/app/profile/thai.pham7308/viz/DB1Emergingvs_FamousArtistsOverview/Dashboard1](https://public.tableau.com/app/profile/thai.pham7308/viz/DB1Emergingvs_FamousArtistsOverview/Dashboard1)

This dashboard provides a comprehensive overview comparing Emerging and Famous artists based on their popularity, follower count, and key performance metrics. The charts are color-coded consistently across the dashboard to distinguish between the two groups:

- **Emerging Artists:** High popularity but low follower count  
- **Famous Artists:** High popularity and high follower count

### Thresholds are calculated based on statistical analysis of the full dataset:

- **Follower thresholds** are based on log-scale mean and standard deviation:  
low_threshold = round(mean_log - std_log, 2)
high_threshold = round(mean_log + std_log, 2)
- **Popularity thresholds** are based on:  
low_threshold = round(mean_pop - std_pop, 2)
high_threshold = round(mean_pop + std_pop, 2)

---

## Chart Descriptions

All tables and charts in the dashboard are numbered as shown in the illustration to facilitate easy reference and tracking.


### Table: Artist Group Summary by Popularity & Followers (#1)

This table displays the number of artists categorized as Emerging or Famous, based on predefined thresholds of popularity and follower count.

**Insight Provided:**  
The table simply reports the count of artists in each group, offering a quick overview of how many meet the criteria for Emerging or Famous status.

---

### Popularity vs. Followers: Emerging vs. Famous Artists (#2)

- This dual bar chart compares the average popularity and average follower count between Emerging and Famous artists.  
- Hover over bars to see the details.

**Insights Provided:**  
- Shows that Famous artists not only have higher followers, but may also slightly outperform in popularity.  
- Highlights that Emerging artists can have comparable popularity, despite having significantly fewer followers.  
- Helps identify the gap between audience reach and perceived popularity.

---

### Comparison of Track and Album Popularity (#3)

This bar chart compares the average popularity of albums and tracks across two artist categories: Emerging and Famous. Each group is represented by two bars—one for average album popularity and one for average track popularity.

**Insights Provided:**  
This chart compares the average popularity of tracks and albums between Emerging and Famous artists. Interestingly, Emerging artists show slightly higher average popularity scores, suggesting they may be gaining more traction despite having fewer followers.

---

### Impact of Playlist Owner on Artist Followers (#4)

**Definition – Follower Gap:**  
Follower Gap = Playlist Owner’s Follower Count - Average Follower Count of the Artist Group in a specific playlist.

**Insights Provided:**  
This metric illustrates the potential opportunity for an artist to gain visibility by being featured in a playlist. It calculates the gap as the playlist owner's follower count minus the artist's followers. A more positive gap indicates a greater opportunity for the artist to leverage the playlist owner's audience for increased exposure. Conversely, a gap close to zero or negative suggests little to no opportunity for visibility boost through that playlist.

---

### Key Metrics Comparison Between Emerging and Famous Artist (#5)

This section provides a side-by-side comparison of average values across several important metrics for emerging and famous artists. These metrics include the average number of playlists, albums, tracks, and genres associated with each artist group.

- Hover over bars to see the details.

**Insights Provided:**  
- Helps identify which artist group is more extensively represented across Spotify content types.  
- A higher average playlist count for one group may indicate stronger promotional exposure.  
- Differences in album and track counts can reflect varying levels of productivity or catalog size.  
- Genre diversity (via average genre count) may reveal how versatile or niche the artists are in each group.

---

### Yearly Trend of Artist Followers (#6)

Line chart illustrating average followers over time for Emerging and Famous artists. Tooltip shows yearly average follower values.

**Insights Provided:**  
This chart reveals how the follower counts for Emerging and Famous artists have evolved over time, highlighting growth trends and periods of accelerated popularity for each group.

---

### Yearly Trend of Artist Popularity (#7)

Line chart showing average popularity over time, separated by artist category. Tooltip reveals year-specific average popularity.

**Insights provided:**  
This chart highlights how the average popularity of Emerging and Famous artists changes over time, revealing shifts in audience interest and artist impact within each category.

---

### Yearly Trend of Average Released Albums (#8)

Tracks how many albums were released each year by Emerging artists. Tooltip shows year and album count.

**Insights provided:**  
This chart shows the annual volume of album releases by Emerging artists, indicating their productivity and engagement with the market over the years.

---

### Yearly Trend of Tracks (#9)

Displays the number of tracks released per year by Emerging artists. Tooltip shows year and track count.

**Insights provided:**  
This chart tracks the yearly count of tracks released by Emerging artists, providing insight into their content output and potential growth in presence over time.

---

## 🔗 Navigation Tip

Use the navigation button in Dashboard 1 to jump directly to Dashboard 2 (In-Depth Exploration of Emerging Artists) for a focused exploration of Emerging Artists.

## 🔹 Dashboard 2: In-Depth Exploration of Emerging Artists

**Link:**  
[https://public.tableau.com/app/profile/thai.pham7308/viz/DB2In-DepthExplorationofEmergingArtists/Dashboard2](https://public.tableau.com/app/profile/thai.pham7308/viz/DB2In-DepthExplorationofEmergingArtists/Dashboard2)

This dashboard provides a detailed analysis of Emerging Artists, defined as artists with high popularity but low follower count, based on data thresholds established in Dashboard 1.

---

### Top Emerging Artists By Various Metrics (#1)

This table displays the names and key metrics of Emerging Artists, including:

- **Follower Count:** Total number of followers an artist has.  
- **Popularity:** Overall popularity score of the artist.  
- **Track Count:** Total number of tracks by the artist.  
- **Album Count:** Total number of albums by the artist.  
- **Playlist Count:** Total number of playlists that include tracks by the artist.  
- **Track Popularity:** Average popularity score of all tracks by the artist.  
- **Album Popularity:** Average popularity score of all albums by the artist.

**Use the Metric Filter to select artists based on different criteria:**

- **Top By Follower:** Artists with follower counts above the average of all emerging artists.  
- **Top By Popularity:** Artists with overall popularity above average.  
- **Top By Track, Top By Album, Top By Playlist:** Artists whose counts of tracks, albums, or playlists they appear in exceed the average.  
- **Top By Track Rate, Top By Album Rate:** Artists whose average track or album popularity is above the average of all emerging artists.  
- **Top By All Count:** Artists exceeding the average in all count-based metrics (followers, tracks, albums, playlists).  
- **Top By All Rate:** Artists exceeding the average in all popularity-based metrics (artist popularity, track popularity, album popularity).

---

### Chart: Annual Album Output per Emerging Artist (#2)

Shows the number of albums released each year by emerging artists (only artists with release date information appear). The chart updates dynamically based on the Metric Filter selections.

---

### Chart: Top Most Popular Track (#3)

Displays the most popular track(s) for each artist according to the current Metric Filter. If an artist has multiple tracks tied for highest popularity, all are shown. Hover over each track for detailed information.

> **Note:** Since this shows only the top track per artist, the total number of tracks here is usually less than the track count shown in Table 1.

---

### Interaction Tip

Click on any artist’s name in Table 1 to filter the two charts, so they display information only for the selected artist.

---

### Insights Provided

- Highlights emerging artists’ performance across multiple key metrics, such as follower counts and popularity scores.  
- The annual album output chart reveals productivity trends of emerging artists over time.  
- The top track chart identifies standout tracks contributing to an artist’s popularity.  
- The metric filter allows flexible exploration of artist groups based on various success dimensions, enabling comparisons within the emerging artist category.

---

## 🔗 Navigation Tip

The **"Compare Emerging vs. Famous Artist"** button offers a quick way to navigate back to the overall artist group comparison dashboard.