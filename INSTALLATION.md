# Shapro Installation Guide

## System Requirements
- Python 3.8 or higher
- pip (Python package manager)
- Git
- Modern web browser

## Installation Steps

### 1. Clone the Repository
```bash
git clone https://github.com/gitahmayimbi-ux/Shapro.git
cd Shapro
```

### 2. Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
# Copy example file
cp .env.example .env

# Edit .env with your settings
# Add your API keys:
# - OpenWeatherMap API key (get from https://openweathermap.org/api)
# - NASA POWER API key (optional, get from https://power.larc.nasa.gov/)
```

### 5. Initialize Database
```bash
python backend/app.py
# The database will be created automatically on first run
```

### 6. Run the Application
```bash
python backend/app.py
```

The application will start on `http://localhost:5000`

### 7. Open in Browser
Navigate to `http://localhost:5000` in your web browser

## Getting API Keys

### OpenWeatherMap
1. Go to https://openweathermap.org/api
2. Sign up for a free account
3. Copy your API key from the dashboard
4. Add to `.env` file

### NASA POWER (Optional)
1. Visit https://power.larc.nasa.gov/
2. No key required for basic usage
3. Useful for historical climate data

## Troubleshooting

### Port Already in Use
If port 5000 is already in use:
```bash
# Change port in backend/app.py
app.run(port=5001)  # Use different port
```

### Database Errors
If you encounter database errors:
```bash
# Delete existing database
rm shapro.db

# Restart application
python backend/app.py
```

### Import Errors
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

## Development Mode

For development with auto-reload:
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
python backend/app.py
```

## Next Steps

1. Add your farm data
2. Connect weather API
3. Create crop entries
4. Monitor recommendations
5. Track analytics

For more information, see [API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md)
