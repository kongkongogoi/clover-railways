from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3, os, random, string
from datetime import datetime

app = Flask(__name__)
app.secret_key = "change-this-demo-secret"
DB_PATH = os.path.join(os.path.dirname(__file__), "railway.db")

SAMPLE_TRAINS = [
    ("CR101", "Brahmaputra Valley Express (Demo)", "Guwahati", "Dibrugarh", "06:15", "14:30", 520, 48),
    ("CR102", "Barak Valley Intercity (Demo)", "Guwahati", "Silchar", "07:00", "16:10", 460, 42),
    ("CR103", "Eastern Hills Express (Demo)", "Guwahati", "Naharlagun", "08:20", "13:45", 390, 36),
    ("CR104", "Upper Assam Connector (Demo)", "Dibrugarh", "Tinsukia", "09:10", "10:35", 160, 54),
    ("CR105", "Brahmaputra Link (Demo)", "Guwahati", "Jorhat Town", "15:00", "20:25", 340, 40),
    ("CR106", "Northeast Gateway Express (Demo)", "Naharlagun", "Guwahati", "16:30", "22:00", 410, 38),
    ("CR107", "Hill & Valley Express (Demo)", "Silchar", "Agartala", "06:45", "13:20", 370, 32),
    ("CR108", "Dooars-Northeast Link (Demo)", "Guwahati", "New Jalpaiguri", "21:00", "06:15", 680, 44),
]

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with db() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS trains (
            id INTEGER PRIMARY KEY AUTOINCREMENT, number TEXT UNIQUE, name TEXT,
            source TEXT, destination TEXT, departure TEXT, arrival TEXT,
            fare INTEGER, seats INTEGER)""")
        con.execute("""CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT, pnr TEXT UNIQUE, passenger TEXT,
            age INTEGER, gender TEXT, train_number TEXT, train_name TEXT,
            source TEXT, destination TEXT, journey_date TEXT, travel_class TEXT,
            fare INTEGER, status TEXT DEFAULT 'CONFIRMED', created_at TEXT)""")
        # Refresh the demonstration route catalogue on each start while preserving bookings.
        con.execute("DELETE FROM trains")
        con.executemany("""INSERT INTO trains
            (number,name,source,destination,departure,arrival,fare,seats)
            VALUES (?,?,?,?,?,?,?,?)""", SAMPLE_TRAINS)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/portal")
def portal():
    source = request.args.get("source", "").strip()
    destination = request.args.get("destination", "").strip()
    date = request.args.get("date", "").strip()
    with db() as con:
        trains = con.execute("SELECT * FROM trains WHERE (?='' OR lower(source) LIKE lower(?) OR lower(source)=lower(?)) AND (?='' OR lower(destination) LIKE lower(?) OR lower(destination)=lower(?)) ORDER BY departure",
            (source, f"%{source}%", source, destination, f"%{destination}%", destination)).fetchall()
        recent = con.execute("SELECT * FROM bookings ORDER BY id DESC LIMIT 5").fetchall()
    return render_template("portal.html", trains=trains, recent=recent, source=source, destination=destination, date=date)

@app.route("/book/<int:train_id>", methods=["GET", "POST"])
def book(train_id):
    with db() as con:
        train = con.execute("SELECT * FROM trains WHERE id=?", (train_id,)).fetchone()
    if not train:
        flash("Train not found.", "error")
        return redirect(url_for("portal"))
    if request.method == "POST":
        passenger = request.form.get("passenger", "").strip()
        age = request.form.get("age", type=int)
        gender = request.form.get("gender", "")
        journey_date = request.form.get("journey_date", "")
        travel_class = request.form.get("travel_class", "Sleeper")
        if not passenger or not age or age < 1 or not journey_date:
            flash("Please complete all passenger details correctly.", "error")
            return render_template("book.html", train=train)
        pnr = ''.join(random.choices(string.digits, k=10))
        with db() as con:
            con.execute("""INSERT INTO bookings
                (pnr,passenger,age,gender,train_number,train_name,source,destination,
                 journey_date,travel_class,fare,status,created_at)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (pnr, passenger, age, gender, train["number"], train["name"],
                 train["source"], train["destination"], journey_date, travel_class,
                 train["fare"], "CONFIRMED", datetime.now().strftime("%d %b %Y, %I:%M %p")))
        return render_template("confirmation.html", pnr=pnr, passenger=passenger, train=train,
                               journey_date=journey_date, travel_class=travel_class)
    return render_template("book.html", train=train)

@app.route("/pnr", methods=["GET", "POST"])
def pnr_status():
    booking = None
    searched = False
    if request.method == "POST":
        searched = True
        pnr = request.form.get("pnr", "").strip()
        with db() as con:
            booking = con.execute("SELECT * FROM bookings WHERE pnr=?", (pnr,)).fetchone()
    return render_template("pnr.html", booking=booking, searched=searched)

@app.route("/cancel", methods=["GET", "POST"])
def cancel():
    booking = None
    searched = False
    if request.method == "POST":
        searched = True
        pnr = request.form.get("pnr", "").strip()
        with db() as con:
            booking = con.execute("SELECT * FROM bookings WHERE pnr=?", (pnr,)).fetchone()
            if booking and booking["status"] == "CONFIRMED":
                con.execute("UPDATE bookings SET status='CANCELLED' WHERE pnr=?", (pnr,))
                booking = con.execute("SELECT * FROM bookings WHERE pnr=?", (pnr,)).fetchone()
                flash("Reservation cancelled successfully.", "success")
    return render_template("cancel.html", booking=booking, searched=searched)

@app.route("/admin")
def admin():
    with db() as con:
        bookings = con.execute("SELECT * FROM bookings ORDER BY id DESC").fetchall()
        train_count = con.execute("SELECT COUNT(*) FROM trains").fetchone()[0]
        confirmed = con.execute("SELECT COUNT(*) FROM bookings WHERE status='CONFIRMED'").fetchone()[0]
        cancelled = con.execute("SELECT COUNT(*) FROM bookings WHERE status='CANCELLED'").fetchone()[0]
    return render_template("admin.html", bookings=bookings, train_count=train_count,
                           confirmed=confirmed, cancelled=cancelled)

@app.route("/about")
def about():
    return render_template("about.html")

init_db()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )