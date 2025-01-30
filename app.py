from flask import Flask, render_template, jsonify, request
import datetime
import os

app = Flask(__name__)
app.secret_key = "safety-dashboard"  # Required for session management

# Safety Statistics (Stored in memory, can be upgraded to a database)
safety_stats = {
    "zero_lta_target": 13384650,
    "past_best_record": 0,  # Initial past best record
    "last_accident": "21.09.18",  # Last accident date in DD.MM.YY format
}

def calculate_current_record():
    """Calculates current record as days since the last accident."""
    today = datetime.datetime.now()
    last_accident_date = datetime.datetime.strptime(safety_stats["last_accident"], "%d.%m.%y")
    current_record = (today - last_accident_date).days
    return current_record

@app.route('/')
def index():
    """Render the main dashboard"""
    return render_template("index.html")

@app.route('/time')
def get_time():
    """Returns the current time and date"""
    now = datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S")
    return jsonify({"time": now})

@app.route('/stats')
def get_stats():
    """Returns the safety statistics"""
    current_record = calculate_current_record()

    # Update past best record if current surpasses it
    if current_record > safety_stats["past_best_record"]:
        safety_stats["past_best_record"] = current_record

    return jsonify({
        "zero_lta_target": safety_stats["zero_lta_target"],
        "past_best_record": safety_stats["past_best_record"],
        "current_record": current_record,
        "last_accident": safety_stats["last_accident"]
    })

@app.route('/reset', methods=['POST'])
def reset_stats():
    """Resets the current record and updates last accident date"""
    current_date = datetime.datetime.now().strftime("%d.%m.%y")
    safety_stats["last_accident"] = current_date  # Update last accident date

    return jsonify(safety_stats)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Use Render's assigned PORT
    app.run(host="0.0.0.0", port=port)
