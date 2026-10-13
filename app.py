from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Data sementara untuk menyimpan histori tidur (disimpan di memori)
sleep_history = []

def calculate_sleep(sleep_time_str, wake_time_str):
    fmt = '%H:%M'
    t1 = datetime.strptime(sleep_time_str, fmt)
    t2 = datetime.strptime(wake_time_str, fmt)
    
    if t2 < t1:
        duration_minutes = ((datetime.strptime("23:59", fmt) - t1).seconds + 
                            (t2 - datetime.strptime("00:00", fmt)).seconds + 60)
    else:
        duration_minutes = (t2 - t1).seconds
        
    duration_hours = round(duration_minutes / 3600, 1)
    
    if 7 <= duration_hours <= 9:
        status = "Cukup & Ideal ✨"
        color = "#4ade80"
    elif duration_hours > 9:
        status = "Kelebihan Tidur 😴"
        color = "#60a5fa"
    else:
        status = "Kurang Tidur ☕"
        color = "#f87171"
        
    return duration_hours, status, color

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        date = request.form.get("date")
        sleep_time = request.form.get("sleep_time")
        wake_time = request.form.get("wake_time")
        mood = request.form.get("mood")
        
        hours, status, color = calculate_sleep(sleep_time, wake_time)
        
        sleep_data = {
            "date": date,
            "sleep_time": sleep_time,
            "wake_time": wake_time,
            "hours": hours,
            "mood": mood,
            "status": status,
            "color": color
        }
        
        sleep_history.insert(0, sleep_data)
        return redirect(url_for("index"))
        
    return render_template("index.html", history=sleep_history)

if __name__ == "__main__":
    app.run(debug=True)
