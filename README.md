# Clover Railways — Python Railway Reservation System

A Black Clover-inspired dark fantasy visual theme for a classroom railway reservation project.
The clover emblem is original CSS/SVG artwork and is not an official anime logo.

## Features
- Intro/landing page about Assam and Northeast India demo rail routes; click the clover emblem to open the portal.
- Search sample trains by source and destination.
- Passenger booking form and generated 10-digit PNR.
- PNR status lookup.
- Ticket cancellation.
- Admin dashboard with booking summary.
- SQLite database created automatically.

## Run on Windows
1. Install Python 3.10 or newer.
2. Open this folder in VS Code.
3. Open Terminal and run:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python app.py
   ```
4. Open http://127.0.0.1:5000 in your browser.

## Run on macOS/Linux
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python app.py
   ```

## Demo notes
- The train list and fares are sample data, not live Assam and Northeast India demo rail routes inventory.
- No payment gateway or official IRCTC connection is included.
- Admin dashboard is intentionally simple for classroom demonstration and has no authentication.
- Delete `railway.db` to reset all bookings and recreate the sample train database on next launch.


## Visual upgrade
- Crimson red and black theme.
- Animated train transition when navigating between pages.
- Floating clover and magical symbols on the landing page.
- Sample routes focused on Assam and Northeast India.

All route names, times and fares are illustrative academic demo data, not live railway schedules.
