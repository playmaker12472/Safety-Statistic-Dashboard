from flask import Flask, render_template, jsonify, request
import datetime

app = Flask(__name__)
app.secret_key = "safety-dashboard"  # Required for session management

# Safety Statistics (Stored in memory, can be upgraded to a database)
safety_stats = {
    "zero_lta_target": 365,
    "past_best_record": 0,  # Initial past best record
    "current_record": 0,  # Start current record at 0
    "last_accident": "21.09.18",
    "last_update": datetime.datetime.now().strftime("%d.%m.%Y")  # Tracks last update
}

def update_current_record():
    """Automatically increments the current record daily."""
    today = datetime.datetime.now().strftime("%d.%m.%Y")
    if safety_stats["last_update"] != today:
        safety_stats["current_record"] += 1
        safety_stats["last_update"] = today

        # Update past best record if current surpasses it
        if safety_stats["current_record"] > safety_stats["past_best_record"]:
            safety_stats["past_best_record"] = safety_stats["current_record"]

@app.route('/')
def index():
    """Render the main dashboard"""
    update_current_record()
    return render_template("index.html")

@app.route('/time')
def get_time():
    """Returns the current time and date"""
    now = datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S")
    return jsonify({"time": now})

@app.route('/stats')
def get_stats():
    """Returns the safety statistics"""
    update_current_record()
    return jsonify(safety_stats)

@app.route('/reset', methods=['POST'])
def reset_stats():
    """Resets the current record and updates last accident date"""
    current_date = datetime.datetime.now().strftime("%d.%m.%y")
    safety_stats["last_accident"] = current_date

    # Before resetting, check if the current record is the highest
    if safety_stats["current_record"] > safety_stats["past_best_record"]:
        safety_stats["past_best_record"] = safety_stats["current_record"]

    safety_stats["current_record"] = 0  # Reset current record
    return jsonify(safety_stats)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
    # app.run()
