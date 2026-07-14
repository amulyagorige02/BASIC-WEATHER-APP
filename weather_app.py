import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime

BG_COLOR = "#0F172A"
CARD_COLOR = "#1E293B"
BUTTON_COLOR = "#2563EB"
TEXT_COLOR = "white"

weather_codes = {
    0: "Clear Sky",
    1: "Mainly Clear",
    2: "Partly Cloudy",
    3: "Cloudy",
    45: "Fog",
    48: "Fog",
    51: "Light Drizzle",
    53: "Drizzle",
    55: "Heavy Drizzle",
    61: "Light Rain",
    63: "Rain",
    65: "Heavy Rain",
    71: "Light Snow",
    73: "Snow",
    75: "Heavy Snow",
    80: "Rain Showers",
    81: "Heavy Showers",
    82: "Violent Rain",
    95: "Thunderstorm"
}

root = tk.Tk()
root.title("Professional Weather App")
root.geometry("700x700")
root.configure(bg=BG_COLOR)
root.resizable(False, False)

title = tk.Label(
    root,
    text="🌤 PROFESSIONAL WEATHER APP",
    font=("Arial", 20, "bold"),
    bg=BG_COLOR,
    fg="white"
)
title.pack(pady=15)

frame = tk.Frame(root, bg=CARD_COLOR)
frame.pack(pady=10, padx=20, fill="x")

city_label = tk.Label(
    frame,
    text="Enter City",
    bg=CARD_COLOR,
    fg=TEXT_COLOR,
    font=("Arial", 12, "bold")
)
city_label.pack(pady=5)

city_entry = tk.Entry(
    frame,
    font=("Arial", 14),
    width=30,
    justify="center"
)
city_entry.pack(pady=5)

result = tk.Label(
    root,
    text="",
    bg=BG_COLOR,
    fg="white",
    font=("Arial", 13),
    justify="left"
)
result.pack(pady=20)

hourly_label = tk.Label(
    root,
    text="",
    bg=BG_COLOR,
    fg="cyan",
    font=("Arial", 11),
    justify="left"
)
hourly_label.pack()

daily_label = tk.Label(
    root,
    text="",
    bg=BG_COLOR,
    fg="lightgreen",
    font=("Arial", 11),
    justify="left"
)
daily_label.pack(pady=20)
def get_weather():

    city = city_entry.get().strip()

    if city == "":
        messagebox.showerror("Error", "Please enter a city name.")
        return

    try:

        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"

        geo = requests.get(geo_url).json()

        if "results" not in geo:
            messagebox.showerror("Error", "City not found.")
            return

        lat = geo["results"][0]["latitude"]
        lon = geo["results"][0]["longitude"]
        city_name = geo["results"][0]["name"]
        country = geo["results"][0]["country"]

        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
            f"&hourly=temperature_2m"
            f"&daily=temperature_2m_max,temperature_2m_min"
            f"&timezone=auto"
        )

        weather = requests.get(weather_url).json()

        current = weather["current"]

        temp_c = current["temperature_2m"]
        temp_f = round((temp_c * 9 / 5) + 32, 1)

        humidity = current["relative_humidity_2m"]
        wind = current["wind_speed_10m"]

        code = current["weather_code"]

        condition = weather_codes.get(code, "Unknown")

        result.config(
            text=f"""
City : {city_name}, {country}

Temperature : {temp_c} °C / {temp_f} °F

Humidity : {humidity} %

Wind Speed : {wind} km/h

Condition : {condition}
"""
        )

        hours = weather["hourly"]["time"][:6]
        temps = weather["hourly"]["temperature_2m"][:6]

        hourly_text = "Next 6 Hours Forecast\n\n"

        for t, temp in zip(hours, temps):
            time = t.split("T")[1]
            hourly_text += f"{time}   {temp}°C\n"

        hourly_label.config(text=hourly_text)

        days = weather["daily"]["time"]
        max_temp = weather["daily"]["temperature_2m_max"]
        min_temp = weather["daily"]["temperature_2m_min"]

        daily_text = "5 Day Forecast\n\n"

        for d, mx, mn in zip(days[:5], max_temp[:5], min_temp[:5]):
            daily_text += f"{d}   {mx}°C / {mn}°C\n"

        daily_label.config(text=daily_text)

    except:
        messagebox.showerror(
            "Error",
            "Unable to fetch weather.\nCheck your internet connection."
        )
# -------------------------------
# Get Weather Button
# -------------------------------

get_btn = tk.Button(
    frame,
    text="Get Weather",
    command=get_weather,
    bg=BUTTON_COLOR,
    fg="white",
    font=("Arial", 13, "bold"),
    width=20,
    relief="flat",
    cursor="hand2"
)

get_btn.pack(pady=15)

# -------------------------------
# Footer
# -------------------------------

footer = tk.Label(
    root,
    text="Developed using Python + Tkinter + Open-Meteo API",
    bg=BG_COLOR,
    fg="lightgray",
    font=("Arial", 10)
)
footer.pack(side="bottom", pady=10)

# Press Enter to search
city_entry.bind("<Return>", lambda event: get_weather())

# Focus on input when app starts
city_entry.focus()

# -------------------------------
# Start Application
# -------------------------------

root.mainloop()