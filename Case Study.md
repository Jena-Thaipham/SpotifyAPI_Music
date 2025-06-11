# Case Study: Spotify Artist Analysis — Emerging vs Famous Artists

## Introduction

This case study analyzes Spotify artist data to distinguish and compare Emerging artists (high popularity, low follower count) and Famous artists (high popularity, high follower count). The goal is to uncover insights about artist growth, audience engagement, and content productivity, supporting strategic decisions in the music business.

Two interactive Tableau dashboards, developed using Spotify API data, provide comprehensive views and in-depth explorations of artist metrics and trends.

## Data & Tools

- **Data Source:** Spotify Web API – track, artist, album, playlist, and user data  
- **Database:** SQLite for structured data storage  
- **Programming:** Python for data extraction and processing  
- **Visualization:** Tableau for creating interactive dashboards  
- **Supporting Libraries:** Pandas, NumPy, SQLAlchemy

## Dashboards Overview

- **Dashboard 1: Emerging vs. Famous Artists Overview**  
  Provides a high-level comparison between artist groups, analyzing popularity, follower count, playlists, tracks, albums, and yearly trends.  
  📊 [View Dashboard 1](https://public.tableau.com/app/profile/thai.pham7308/viz/DB1Emergingvs_FamousArtistsOverview/Dashboard1)

- **Dashboard 2: In-Depth Exploration of Emerging Artists**  
  Focuses on detailed metrics of Emerging artists, including top performers by multiple success measures, annual output, and top tracks.  
  📊 [View Dashboard 2](https://public.tableau.com/app/profile/thai.pham7308/viz/DB2In-DepthExplorationofEmergingArtists/Dashboard2)

👉 Use the dashboard navigation buttons or refer to the included `Dashboard_User_Guide.md` in this repository for detailed usage instructions and insight interpretation.

## Key Insights

1. **Emerging vs. Famous Artist Profiles:**  
   While Famous artists have higher follower counts and larger catalogs, Emerging artists can achieve comparable popularity, indicating rising influence despite lower audience reach.

2. **Playlist Exposure Challenges:**  
   The follower gap metric shows that playlist owners typically have fewer followers than the Emerging artists featured. This indicates that the current playlists may provide limited exposure benefits to the artists, suggesting a need to target playlists managed by users with larger audiences to boost artist visibility effectively.

3. **Productivity & Trend Dynamics:**  
   Yearly trends show Emerging artists steadily increasing album and track releases, with rapid growth in followers and popularity over time.

## Business Recommendations

- **Leverage Playlist Placements:**  
  Prioritize featuring Emerging artists on high-follower playlists to boost exposure and follower growth.

- **Early Identification of Rising Talent:**  
  Monitor popularity and productivity metrics to invest in artists with high growth potential.

- **Optimize Release Timing:**  
  Align album and track releases with identified productivity trends to maximize audience engagement.

-  **Expand Cross-Platform Presence:**
Encourage artists to promote music on multiple streaming services and social media channels to broaden reach beyond Spotify.

  **Engage with Fan Communities:**
Facilitate direct interaction between artists and fans through social media, live events, and fan-driven playlists to deepen loyalty and increase organic growth.

## Action Plan

1. **Enhance Data Collection:**  
   Integrate additional engagement metrics like monthly listeners from paid APIs.

2. **Segment Audience:**  
   Develop user profiles by geography and listening behavior to customize marketing efforts.

3. **Cross-Platform Analysis:**  
   Incorporate data from YouTube, Apple Music, and other platforms for holistic artist performance insights.

4. **Data-Driven Marketing Campaigns:**
Collect additional data on listener demographics, regions, and genres to enable tailored marketing efforts in future campaigns

5. **Build Predictive Models:**  
   Implement time-series forecasting to anticipate trends and guide proactive marketing.

## Conclusion

This case study demonstrates how Spotify data, when analyzed and visualized effectively, can reveal valuable insights into artist development and music consumption trends. By distinguishing Emerging and Famous artists, stakeholders can better allocate resources, tailor marketing, and support artist growth, ultimately driving business success in the competitive music industry.



