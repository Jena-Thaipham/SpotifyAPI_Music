# Tune into Success: Harnessing Spotify Data to Drive Music Business Growth

## Project Overview
This project leverages Spotify's Web API to extract, analyze, and visualize music consumption trends. By storing structured data and applying analytical techniques, we aim to provide actionable insights for record labels, artists, and marketers to optimize their strategies in the music industry.

## Objectives
- **Extract and Store Music Data**: Retrieve track, artist, album, and genre data from Spotify's API and store it in a structured database.
- **Analyze Music Trends**: Identify genre popularity and music consumption trends over time.
- **Business Insights**: Generate insights to assist music industry stakeholders in decision-making.

## Project Components
### 1. Data Extraction
- **API Setup**: Utilize Spotify's Web API to fetch track details (name, artist, album, genre), popularity metrics, release dates, and user playlist data.
- **Data Collection**: Implement Python scripts to automate data extraction based on predefined queries (e.g., top songs per genre, trending artists).

### 2. Database Design
- **Database Creation**: Set up a relational database (SQLite) to store the extracted data.
- **Schema Design**: Define tables for tracks, artists, albums, and genres with proper normalization to eliminate redundancy.

### 3. Data Analysis
- **SQL Queries**: Perform queries to extract insights such as:
  - Which genres are gaining popularity?
  - What characteristics define the most popular tracks?
  - How do demographics (age, location) influence music preferences?
- **Trends and Patterns**: Use visualization tools like Tableau to present music consumption trends.

### 4. Business Insights
- **Market Analysis**: Identify emerging genres and artists for record labels to focus on.
- **Playlist Recommendations**: Suggest curated playlists based on user preferences and trending music.

### 5. Reporting and Presentation
- **Comprehensive Report**: Summarize key findings, trends, and business recommendations in a detailed report.
- **Interactive Dashboard**: Develop a dynamic dashboard to allow stakeholders to explore and interact with the data.

## Usage
- To explore the interactive dashboards, visit the Tableau Public link: [Dashboard](https://public.tableau.com/app/profile/thai.pham7308/viz/DB1Emergingvs_FamousArtistsOverview/Dashboard1).
- Use filters and controls in the dashboard to analyze music trends by genre, artist, and time period.
- For a detailed explanation of how the dashboards work and the insights provided, please refer to the `Dashboard_User_Guide.md` file located in this repository. This guide will help you better understand the data visualizations and how to interpret the results.
- 📄 For a detailed walkthrough of insights and business recommendations, check out the [full case study](./Case_Study.md).

## Technologies Used
- **Programming Languages**: Python
- **Database**: SQLite
- **APIs**: Spotify Web API
- **Data Visualization**: Tableau
- **Tools**: Pandas, NumPy, SQLAlchemy

## 📚 What I Learned

Through this project, I enhanced both my technical and analytical skills. Some key learnings include:

- Gained hands-on experience in working with the Spotify API for real-world data extraction and processing.
- Developed interactive dashboards using Tableau to communicate insights clearly and effectively.
- Improved my ability to translate data-driven insights into actionable business recommendations.
- Strengthened my understanding of how data analytics can directly support decision-making in the music industry.

This project also reinforced the importance of storytelling in data science — making complex analysis accessible and meaningful to business stakeholders.

---

## 🔄 Next Steps

While the project yielded valuable insights, there are still areas worth exploring to increase business impact:

- **Refining audience engagement metrics:** While follower count is available through the Spotify API, it may not accurately reflect true user engagement. **Monthly listeners** could provide a more precise measure, but this metric is not offered through the free API. Some third-party providers do offer this via **paid APIs**, and this is worth noting for future development.
- **User segmentation:** Future work could explore segmenting users by geography, listening behavior, and genre preference to enable more targeted marketing strategies.
- **Cross-platform analysis:** Integrating data from other platforms (e.g., YouTube, Apple Music) could help build a more comprehensive view of artist and track performance.
- **Tracking over time:** A time-series component could be added to monitor how popularity and trends shift over weeks or months.

These next steps would further strengthen the value of the analysis and bring even greater business relevance.

## Installation & Setup

1. Register an app on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications) to obtain your **Client ID** and **Client Secret**.
2. Store the credentials in a `.env` file with the following format: `CLIENT_ID=your_client_id` and `CLIENT_SECRET=your_client_secret`.
3. Clone the repository by running `git clone https://github.com/Jena-Thaipham/SpotifyAPI_Music.git` and navigate into the project directory using `cd SpotifyAPI_Music`.
4. Run the `SpotifyBatchETL.py` file to fetch data from the Spotify API and store it in the database. This will start the data extraction process and store the relevant information in your database for further analysis.
5. If additional IDs are needed, run the `fetch_ids.py` script.




