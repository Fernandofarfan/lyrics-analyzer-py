# Lyrics Analyzer Python

A RESTful API built with Flask and MongoDB to manage and analyze song lyrics.

## Features
- Full CRUD operations for songs.
- Health check and song count endpoints.
- MongoDB integration for data persistence.
- Pre-populated with sample data from `songs.json`.

## Prerequisites
- Python 3.8+
- MongoDB instance (Atlas or local)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd lyrics-analyzer-py
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Set the following environment variables:
- `MONGODB_SERVICE`: MongoDB host address.
- `MONGODB_USERNAME`: MongoDB username (optional).
- `MONGODB_PASSWORD`: MongoDB password (optional).
- `MONGODB_PORT`: MongoDB port (optional).

## Running the Application

```bash
python app.py
```
The application will start on `http://localhost:8080`.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Application health check |
| GET | `/count` | Get total number of songs |
| GET | `/song` | List all songs |
| GET | `/song/<id>` | Get song by ID |
| POST | `/song` | Add a new song |
| PUT | `/song/<id>` | Update an existing song |
| DELETE | `/song/<id>` | Delete a song |

## Project Structure
- `app.py`: Application entry point.
- `backend/`: Core backend logic.
- `backend/routes.py`: API route definitions.
- `backend/data/songs.json`: Initial data seeding.
- `tests/`: Automated tests.

## License
This project is licensed under the Apache License 2.0. See `LICENSE` for details.
Authorship: Fernando Farfán