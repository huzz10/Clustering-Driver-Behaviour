# 🎵 Spotify Data Pipeline

An automated data engineering pipeline that extracts your Spotify listening data, transforms it into meaningful analytics, loads it into PostgreSQL, and visualizes insights through an interactive Streamlit dashboard. Orchestrated with Apache Airflow for scheduled, reliable data processing.

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Data Flow](#data-flow)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)

## ✨ Features

- **Automated Data Extraction**: Fetches recently played tracks and top artists/tracks from Spotify API
- **Incremental Loading**: Only processes new listening history since last run
- **Analytics Aggregation**: Computes daily metrics, genre statistics, and top rankings
- **Data Warehouse**: Star schema design with fact and dimension tables
- **Scheduled Orchestration**: Daily automated runs via Apache Airflow
- **Interactive Dashboard**: Real-time visualization of listening patterns, top artists, genres, and trends
- **Error Handling**: Robust logging and retry mechanisms for API calls

## 🏗️ Architecture

```mermaid
graph TB
    subgraph "Data Source"
        SPOTIFY[Spotify Web API]
    end
    
    subgraph "ETL Layer"
        SPOTIPY[Spotipy Client]
        EXTRACT[Extract Module]
        TRANSFORM[Transform Module]
        PANDAS[Pandas Processing]
    end
    
    subgraph "Orchestration"
        AIRFLOW[Apache Airflow<br/>Scheduler]
        DAG[Spotify ETL DAG<br/>Daily Schedule]
    end
    
    subgraph "Storage Layer"
        POSTGRES[(PostgreSQL<br/>Data Warehouse)]
        ARTISTS[Artists Dimension]
        TRACKS[Tracks Dimension]
        HISTORY[Listening History Fact]
        METRICS[Daily Metrics]
        GENRES[Genre Statistics]
        RANKINGS[Top Rankings]
    end
    
    subgraph "Visualization"
        STREAMLIT[Streamlit Dashboard]
        CHARTS[Interactive Charts<br/>Plotly]
    end
    
    SPOTIFY -->|OAuth 2.0| SPOTIPY
    SPOTIPY --> EXTRACT
    EXTRACT --> TRANSFORM
    TRANSFORM --> PANDAS
    PANDAS --> POSTGRES
    
    AIRFLOW --> DAG
    DAG -->|Triggers| EXTRACT
    
    POSTGRES --> ARTISTS
    POSTGRES --> TRACKS
    POSTGRES --> HISTORY
    POSTGRES --> METRICS
    POSTGRES --> GENRES
    POSTGRES --> RANKINGS
    
    POSTGRES -->|SQL Queries| STREAMLIT
    STREAMLIT --> CHARTS
    
    style SPOTIFY fill:#1DB954,color:#fff
    style AIRFLOW fill:#E43921,color:#fff
    style POSTGRES fill:#336791,color:#fff
    style STREAMLIT fill:#FF4B4B,color:#fff
```

### Architecture Components

1. **Data Source**: Spotify Web API provides listening history and top content
2. **ETL Pipeline**: Python-based extraction, transformation, and loading
3. **Orchestration**: Apache Airflow schedules daily pipeline runs
4. **Storage**: PostgreSQL data warehouse with normalized schema
5. **Visualization**: Streamlit dashboard for interactive analytics

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Data Source** | Spotify Web API, Spotipy | Fetch listening history and top content |
| **ETL** | Python 3.12+, Pandas | Extract, clean, and transform data |
| **Orchestration** | Apache Airflow 2.9.2 | Schedule and monitor pipeline runs |
| **Storage** | PostgreSQL 14+, SQLAlchemy 1.4 | Persist raw and curated data |
| **Visualization** | Streamlit 1.38, Plotly | Interactive dashboard and charts |
| **Utilities** | python-dotenv, tenacity | Configuration and retry logic |

## 📦 Prerequisites

- **Python 3.12+** (recommended) or Python 3.10+
- **PostgreSQL 14+** (or compatible version)
- **Spotify Developer Account** with registered app
- **WSL2 (Ubuntu)** or **Linux/macOS** (recommended for Airflow)
- **Git** (for cloning the repository)

### Spotify API Setup

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Note your **Client ID** and **Client Secret**
4. Add redirect URI: `http://localhost:8888/callback`
5. Request scopes: `user-read-recently-played`, `user-top-read`

## 🚀 Installation

### Option 1: WSL2 (Recommended for Windows)

WSL2 provides the best compatibility with Apache Airflow and PostgreSQL.

#### 1. Install WSL2 and Ubuntu

```powershell
# In PowerShell (as Administrator)
wsl --install -d Ubuntu
```

Restart your computer if prompted, then complete Ubuntu setup.

#### 2. Update System Packages

```bash
sudo apt update && sudo apt upgrade -y
```

#### 3. Install Dependencies

```bash
sudo apt install -y python3 python3-venv python3-pip \
    postgresql postgresql-contrib \
    build-essential libpq-dev openssl libssl-dev
```

#### 4. Clone and Setup Project

```bash
cd ~
git clone <your-repo-url> Spotify-data-pipeline
cd Spotify-data-pipeline

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Option 2: Native Windows

**Note**: Airflow has limited Windows support. Consider using WSL2 or Docker.

```powershell
# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

## ⚙️ Configuration

### 1. Environment Variables

Copy the example environment file and fill in your credentials:

```bash
cp config/env.example .env
```

Edit `.env` with your actual values:

```env
# Spotify API Credentials
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
SPOTIFY_SCOPE=user-read-recently-played user-top-read

# PostgreSQL Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=spotify_analytics
POSTGRES_USER=spotify_user
POSTGRES_PASSWORD=your_secure_password

# Airflow Configuration (WSL/Linux)
AIRFLOW_HOME=/home/your_username/spotify-airflow
```

**Important**: The `.env` file should be in the project root directory.

### 2. First-Time Spotify Authentication

On first run, the pipeline will open a browser for OAuth authentication. You'll need to:
1. Log in to Spotify
2. Authorize the application
3. Copy the callback URL and paste it when prompted

The access token will be cached for subsequent runs.

## 🗄️ Database Setup

### 1. Start PostgreSQL Service

**WSL/Linux:**
```bash
sudo service postgresql start
```

**Windows:**
```powershell
# If installed via installer, service should auto-start
# Or use pgAdmin to start the service
```

### 2. Create Database and User

**WSL/Linux:**
```bash
sudo -u postgres createuser spotify_user --createdb --login --pwprompt
sudo -u postgres createdb spotify_analytics -O spotify_user

# Grant privileges
sudo -u postgres psql <<'SQL'
GRANT ALL PRIVILEGES ON DATABASE spotify_analytics TO spotify_user;
\c spotify_analytics
GRANT USAGE ON SCHEMA public TO spotify_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO spotify_user;
SQL
```

**Windows (using psql):**
```sql
CREATE USER spotify_user WITH PASSWORD 'your_password';
CREATE DATABASE spotify_analytics OWNER spotify_user;
GRANT ALL PRIVILEGES ON DATABASE spotify_analytics TO spotify_user;
```

### 3. Initialize Schema

```bash
psql postgresql://spotify_user:your_password@localhost:5432/spotify_analytics \
     -f sql/schema.sql
```

Or using pgAdmin: Open the SQL editor and execute `sql/schema.sql`.

### Database Schema Overview

- **`artists`**: Artist dimension table with metadata
- **`tracks`**: Track dimension table linked to artists
- **`listening_history`**: Fact table with play events
- **`daily_listening_metrics`**: Aggregated daily statistics
- **`genre_statistics`**: Genre-based analytics
- **`top_artists`**: Top artist rankings (short/medium/long term)
- **`top_tracks`**: Top track rankings (short/medium/long term)

## 🎯 Usage

### Manual Pipeline Execution

Run the ETL pipeline directly without Airflow:

```bash
# Activate virtual environment first
source .venv/bin/activate  # WSL/Linux
# or
.\.venv\Scripts\Activate.ps1  # Windows

# Run pipeline
python -m src.pipeline
```

### Apache Airflow Setup

#### 1. Configure Airflow Home

**WSL/Linux:**
```bash
export AIRFLOW_HOME="$HOME/spotify-airflow"
echo 'export AIRFLOW_HOME="$HOME/spotify-airflow"' >> ~/.bashrc
source ~/.bashrc

# Create Airflow directories
mkdir -p "$AIRFLOW_HOME/dags" "$AIRFLOW_HOME/logs" "$AIRFLOW_HOME/tmp"
```

**Windows (not recommended):**
```powershell
$env:AIRFLOW_HOME = "E:\Python Projects\Spotify-data-pipeline\airflow"
$env:AIRFLOW__DATABASE__SQL_ALCHEMY_CONN = "sqlite:////E:/Python Projects/Spotify-data-pipeline/airflow/airflow.db"
```

#### 2. Initialize Airflow Database

```bash
airflow db init
```

#### 3. Create Airflow Admin User

```bash
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password your_admin_password
```

#### 4. Deploy DAG

```bash
cp dags/spotify_etl_dag.py "$AIRFLOW_HOME/dags/"
```

#### 5. Start Airflow Services

**Terminal 1 - Webserver:**
```bash
airflow webserver --port 8080
```

**Terminal 2 - Scheduler:**
```bash
airflow scheduler
```

Access the Airflow UI at `http://localhost:8080` and log in with your admin credentials.

The `spotify_etl_pipeline` DAG will appear and run daily at midnight (configurable in the DAG definition).

### Streamlit Dashboard

Launch the interactive dashboard:

```bash
# Activate virtual environment
source .venv/bin/activate  # WSL/Linux

# Run Streamlit
streamlit run streamlit_app/app.py --server.port 8501
```

Access the dashboard at `http://localhost:8501`.

**Dashboard Features:**
- Summary metrics (listening time, play counts, active days)
- Daily listening trends (line chart)
- Genre breakdown (bar chart)
- Top artists and tracks rankings (filterable by time range)
- Recent listening history table

## 📁 Project Structure

```
Spotify-data-pipeline/
├── config/
│   ├── __init__.py          # Package marker
│   ├── env.example           # Environment variable template
│   └── settings.py           # Configuration management
├── dags/
│   └── spotify_etl_dag.py    # Airflow DAG definition
├── sql/
│   └── schema.sql            # PostgreSQL schema definitions
├── src/
│   ├── __init__.py           # Package marker
│   ├── database.py           # Database client and operations
│   ├── logger.py             # Logging configuration
│   ├── pipeline.py           # Main ETL pipeline orchestration
│   ├── spotify_client.py     # Spotify API client wrapper
│   └── transformations.py    # Data transformation functions
├── streamlit_app/
│   └── app.py                # Streamlit dashboard application
├── .env                      # Environment variables (create from env.example)
├── .gitignore                # Git ignore rules
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🔄 Data Flow

1. **Extract**: 
   - Fetch recently played tracks (incremental since last run)
   - Fetch top artists and tracks (short/medium/long term)
   - Retrieve artist metadata for enrichment

2. **Transform**:
   - Normalize timestamps and extract date/hour components
   - Derive track and artist dimensions
   - Aggregate daily listening metrics
   - Compute genre statistics
   - Rank top artists and tracks

3. **Load**:
   - Upsert artist and track dimensions
   - Insert new listening history records
   - Replace daily metrics partitions
   - Update genre statistics
   - Refresh top rankings

4. **Visualize**:
   - Streamlit queries PostgreSQL
   - Renders interactive charts and tables
   - Updates in real-time as new data arrives

## 🐛 Troubleshooting

### Common Issues

#### 1. ModuleNotFoundError: No module named 'config'

**Solution**: Ensure you're running from the project root and the `config/__init__.py` file exists.

#### 2. Airflow SQLite Path Error (Windows)

**Error**: `Cannot use relative path: sqlite:///E:/...`

**Solution**: Use WSL2 or set the absolute path with four slashes:
```powershell
$env:AIRFLOW__DATABASE__SQL_ALCHEMY_CONN = "sqlite:////E:/Python Projects/Spotify-data-pipeline/airflow/airflow.db"
```

#### 3. PostgreSQL Connection Failed

**Error**: `password authentication failed`

**Solution**: 
- Verify credentials in `.env` match PostgreSQL user
- Check PostgreSQL service is running: `sudo service postgresql status`
- Ensure user has proper permissions

#### 4. Spotify API Authentication Issues

**Error**: `Invalid client` or `Invalid grant`

**Solution**:
- Verify `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET` in `.env`
- Check redirect URI matches Spotify app settings
- Re-authenticate by deleting cached tokens

#### 5. Streamlit Import Errors

**Solution**: The app automatically adds project root to Python path. If issues persist:
```bash
# Run from project root
cd ~/Spotify-data-pipeline
streamlit run streamlit_app/app.py
```

#### 6. Airflow DAG Not Appearing

**Solution**:
- Verify DAG file is in `$AIRFLOW_HOME/dags/`
- Check for Python syntax errors: `python -m py_compile dags/spotify_etl_dag.py`
- Review Airflow logs: `$AIRFLOW_HOME/logs/`
- Ensure `AIRFLOW_HOME` is set correctly

### Logs Location

- **Airflow Logs**: `$AIRFLOW_HOME/logs/`
- **Application Logs**: Check console output or configure file logging in `src/logger.py`

## 🔮 Future Enhancements

- [ ] Docker Compose setup for easy deployment
- [ ] Support for multiple Spotify accounts
- [ ] Real-time streaming with Kafka
- [ ] Machine learning recommendations based on listening patterns
- [ ] Export functionality (CSV, JSON, Excel)
- [ ] Email/Slack notifications for pipeline failures
- [ ] Data quality checks and validation
- [ ] Integration with other music platforms
- [ ] Advanced analytics (mood detection, tempo analysis)
- [ ] Mobile-responsive dashboard

## 📝 License

This project is provided as-is for educational and personal use.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open an issue on the repository.

---

**Built with ❤️ for music data enthusiasts**
