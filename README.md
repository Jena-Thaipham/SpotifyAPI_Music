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

## Technologies Used
- **Programming Languages**: Python
- **Database**: SQLite
- **APIs**: Spotify Web API
- **Data Visualization**: Tableau
- **Tools**: Pandas, NumPy, SQLAlchemy

## Installation & Setup

1. Register an app on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications) to obtain your **Client ID** and **Client Secret**.
2. Store the credentials in a `.env` file with the following format: `CLIENT_ID=your_client_id` and `CLIENT_SECRET=your_client_secret`.
3. Clone the repository by running `git clone https://github.com/Jena-Thaipham/SpotifyAPI_Music.git` and navigate into the project directory using `cd SpotifyAPI_Music`.
4. Run the `SpotifyETL.py` file to fetch data from the Spotify API and store it in the database. This will start the data extraction process and store the relevant information in your database for further analysis.
5. If additional IDs are needed, run the `fetch_ids.py` script.


