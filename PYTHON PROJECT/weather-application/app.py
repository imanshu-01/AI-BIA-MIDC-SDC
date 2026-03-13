import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
from datetime import datetime
from PIL import Image, ImageTk
import io
import os
from dataclasses import dataclass
from typing import Optional, Dict, List
import threading
import time

# Data class for weather data
@dataclass
class WeatherData:
    city: str
    temperature: float
    feels_like: float
    humidity: int
    pressure: int
    wind_speed: float
    wind_direction: int
    description: str
    main_condition: str
    icon: str
    sunrise: int
    sunset: int
    visibility: int
    timestamp: float
    forecast: List[Dict] = None

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌤️ Advanced Weather App")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f8ff')
        
        # API Configuration
        self.api_key = "68418ce436132483c0bce07db5b9f435"
        self.base_url = "https://api.openweathermap.org/data/2.5"
        
        # Cache setup
        self.cache_file = "weather_cache.json"
        self.cache = self.load_cache()
        self.cache_duration = 600  # 10 minutes in seconds
        
        # Theme
        self.is_dark_mode = False
        self.colors = {
            'light': {
                'bg': '#f0f8ff',
                'fg': "#000000",
                'primary': '#3498db',
                'secondary': '#ecf0f1',
                'accent': '#e74c3c'
            },
            'dark': {
                'bg': "#000000",
                'fg': '#ecf0f1',
                'primary': "#040A2D",
                'secondary': "#1f2932",
                'accent': '#c0392b'
            }
        }
        
        # Initialize variables
        self.use_celsius = True
        self.current_weather_data = None
        
        # Initialize UI
        self.setup_ui()
        
    def setup_ui(self):
        # Create main container
        self.main_frame = tk.Frame(self.root, bg=self.colors['light']['bg'])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        self.header_frame = tk.Frame(self.main_frame, bg=self.colors['light']['primary'])
        self.header_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.title_label = tk.Label(
            self.header_frame,
            text="🌤️ Advanced Weather App",
            font=('Helvetica', 24, 'bold'),
            bg=self.colors['light']['primary'],
            fg='white'
        )
        self.title_label.pack(pady=10)
        
        # Search frame
        self.search_frame = tk.Frame(self.main_frame, bg=self.colors['light']['bg'])
        self.search_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.city_var = tk.StringVar()
        self.city_combo = ttk.Combobox(
            self.search_frame,
            textvariable=self.city_var,
            font=('Helvetica', 12),
            width=30
        )
        self.city_combo['values'] = self.load_city_list()
        self.city_combo.pack(side=tk.LEFT, padx=(0, 10))
        self.city_combo.bind('<Return>', lambda e: self.fetch_weather())
        
        self.search_btn = tk.Button(
            self.search_frame,
            text="Search",
            font=('Helvetica', 12, 'bold'),
            bg=self.colors['light']['accent'],
            fg='white',
            command=self.fetch_weather,
            relief=tk.FLAT,
            padx=20
        )
        self.search_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.unit_btn = tk.Button(
            self.search_frame,
            text="°C/°F",
            font=('Helvetica', 12),
            bg=self.colors['light']['secondary'],
            command=self.toggle_unit,
            relief=tk.FLAT
        )
        self.unit_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.theme_btn = tk.Button(
            self.search_frame,
            text="🌙/☀️",
            font=('Helvetica', 12),
            bg=self.colors['light']['secondary'],
            command=self.toggle_theme,
            relief=tk.FLAT
        )
        self.theme_btn.pack(side=tk.LEFT)
        
        # Current weather frame
        self.current_frame = tk.Frame(self.main_frame, bg=self.colors['light']['bg'])
        self.current_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Current weather display
        self.current_weather_frame = tk.Frame(
            self.current_frame,
            bg=self.colors['light']['secondary'],
            relief=tk.RAISED,
            bd=2
        )
        self.current_weather_frame.pack(fill=tk.X)
        
        self.icon_label = tk.Label(self.current_weather_frame, bg=self.colors['light']['secondary'])
        self.icon_label.pack(side=tk.LEFT, padx=20, pady=20)
        
        self.temp_label = tk.Label(
            self.current_weather_frame,
            font=('Helvetica', 48, 'bold'),
            bg=self.colors['light']['secondary'],
            fg=self.colors['light']['fg']
        )
        self.temp_label.pack(side=tk.LEFT, padx=(0, 20), pady=20)
        
        self.details_frame = tk.Frame(self.current_weather_frame, bg=self.colors['light']['secondary'])
        self.details_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.city_name_label = tk.Label(
            self.details_frame,
            font=('Helvetica', 20, 'bold'),
            bg=self.colors['light']['secondary'],
            fg=self.colors['light']['fg']
        )
        self.city_name_label.pack(anchor='w')
        
        self.condition_label = tk.Label(
            self.details_frame,
            font=('Helvetica', 14),
            bg=self.colors['light']['secondary'],
            fg=self.colors['light']['fg']
        )
        self.condition_label.pack(anchor='w', pady=(5, 0))
        
        self.feels_like_label = tk.Label(
            self.details_frame,
            font=('Helvetica', 12),
            bg=self.colors['light']['secondary'],
            fg=self.colors['light']['fg']
        )
        self.feels_like_label.pack(anchor='w', pady=(5, 0))
        
        # Metrics frame
        self.metrics_frame = tk.Frame(self.main_frame, bg=self.colors['light']['bg'])
        self.metrics_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.create_metric_widgets()
        
        # Forecast frame
        self.forecast_frame = tk.Frame(self.main_frame, bg=self.colors['light']['bg'])
        self.forecast_frame.pack(fill=tk.BOTH, expand=True)
        
        self.forecast_label = tk.Label(
            self.forecast_frame,
            text="5-Day Forecast",
            font=('Helvetica', 16, 'bold'),
            bg=self.colors['light']['bg'],
            fg=self.colors['light']['fg']
        )
        self.forecast_label.pack(anchor='w', pady=(0, 10))
        
        self.forecast_canvas_frame = tk.Frame(self.forecast_frame, bg=self.colors['light']['bg'])
        self.forecast_canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_bar = tk.Label(
            self.main_frame,
            text="Ready",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg=self.colors['light']['secondary'],
            fg=self.colors['light']['fg']
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def create_metric_widgets(self):
        metrics = [
            ("💧 Humidity", "humidity", "%"),
            ("💨 Wind Speed", "wind", "m/s"),
            ("📊 Pressure", "pressure", "hPa"),
            ("👁️ Visibility", "visibility", "km"),
            ("🌅 Sunrise", "sunrise", ""),
            ("🌇 Sunset", "sunset", "")
        ]
        
        for i, (label, key, unit) in enumerate(metrics):
            frame = tk.Frame(
                self.metrics_frame,
                bg=self.colors['light']['secondary'],
                relief=tk.RAISED,
                bd=1
            )
            frame.grid(row=i//3, column=i%3, padx=5, pady=5, sticky='nsew')
            
            # Configure grid
            self.metrics_frame.grid_columnconfigure(i%3, weight=1)
            self.metrics_frame.grid_rowconfigure(i//3, weight=1)
            
            label_widget = tk.Label(
                frame,
                text=label,
                font=('Helvetica', 10),
                bg=self.colors['light']['secondary'],
                fg=self.colors['light']['fg']
            )
            label_widget.pack(pady=(10, 5))
            
            value_widget = tk.Label(
                frame,
                text="--",
                font=('Helvetica', 14, 'bold'),
                bg=self.colors['light']['secondary'],
                fg=self.colors['light']['fg']
            )
            value_widget.pack(pady=(0, 10))
            
            # Store reference
            setattr(self, f"{key}_label", value_widget)
    
    def load_cache(self):
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_cache(self):
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f)
    
    def load_city_list(self):
        default_cities = [
            "Delhi", "Mumbai", "Kolkata", "Chennai", "Bengaluru",
            "Hyderabad", "Pune", "Ahmedabad", "Jaipur", "Lucknow"
        ]
        
        # Try to load from file
        if os.path.exists('cities.json'):
            try:
                with open('cities.json', 'r') as f:
                    cities = json.load(f)
                    return cities + default_cities
            except:
                pass
        
        return default_cities
    
    def fetch_weather(self):
        city = self.city_var.get().strip()
        if not city:
            messagebox.showwarning("Warning", "Please enter a city name")
            return
        
        # Check cache first
        cache_key = f"{city.lower()}_{'celsius' if self.use_celsius else 'fahrenheit'}"
        if cache_key in self.cache:
            cached_data = self.cache[cache_key]
            if time.time() - cached_data['timestamp'] < self.cache_duration:
                # Convert dict back to WeatherData object
                forecast = cached_data.pop('forecast', None)
                weather_data = WeatherData(**cached_data)
                weather_data.forecast = forecast
                self.update_ui(weather_data)
                self.status_bar.config(text="Data loaded from cache")
                return
        
        # Show loading
        self.status_bar.config(text="Fetching weather data...")
        self.search_btn.config(state=tk.DISABLED)
        
        # Fetch in background thread
        thread = threading.Thread(target=self._fetch_weather_thread, args=(city, cache_key))
        thread.daemon = True
        thread.start()
    
    def _fetch_weather_thread(self, city, cache_key):
        try:
            # Current weather
            current_url = f"{self.base_url}/weather?q={city}&appid={self.api_key}"
            current_response = requests.get(current_url, timeout=10)
            current_data = current_response.json()
            
            if current_data.get("cod") != 200:
                self.root.after(0, self.show_error, current_data.get("message", "City not found"))
                return
            
            # Forecast
            forecast_url = f"{self.base_url}/forecast?q={city}&appid={self.api_key}"
            forecast_response = requests.get(forecast_url, timeout=10)
            forecast_data = forecast_response.json()
            
            # Parse data
            weather_data = WeatherData(
                city=current_data['name'],
                temperature=current_data['main']['temp'] - 273.15,
                feels_like=current_data['main']['feels_like'] - 273.15,
                humidity=current_data['main']['humidity'],
                pressure=current_data['main']['pressure'],
                wind_speed=current_data['wind']['speed'],
                wind_direction=current_data['wind'].get('deg', 0),
                description=current_data['weather'][0]['description'],
                main_condition=current_data['weather'][0]['main'],
                icon=current_data['weather'][0]['icon'],
                sunrise=current_data['sys']['sunrise'],
                sunset=current_data['sys']['sunset'],
                visibility=current_data.get('visibility', 0) / 1000,  # Convert to km
                timestamp=time.time(),
                forecast=forecast_data.get('list', [])[:5]  # Next 5 forecasts
            )
            
            # Cache the data
            self.cache[cache_key] = weather_data.__dict__
            self.save_cache()
            
            # Update UI
            self.root.after(0, self.update_ui, weather_data)
            self.root.after(0, lambda: self.status_bar.config(text="Data fetched successfully"))
            
        except requests.exceptions.RequestException as e:
            self.root.after(0, self.show_error, f"Network error: {str(e)}")
        except Exception as e:
            self.root.after(0, self.show_error, f"Error: {str(e)}")
        finally:
            self.root.after(0, lambda: self.search_btn.config(state=tk.NORMAL))
    
    def update_ui(self, weather_data):
        self.current_weather_data = weather_data
        
        # Temperature
        temp = weather_data.temperature if self.use_celsius else weather_data.temperature * 9/5 + 32
        unit = "°C" if self.use_celsius else "°F"
        self.temp_label.config(text=f"{temp:.1f}{unit}")
        
        # City and condition
        self.city_name_label.config(text=weather_data.city)
        self.condition_label.config(text=weather_data.description.title())
        
        # Feels like
        feels_like = weather_data.feels_like if self.use_celsius else weather_data.feels_like * 9/5 + 32
        self.feels_like_label.config(text=f"Feels like {feels_like:.1f}{unit}")
        
        # Update metrics
        self.humidity_label.config(text=f"{weather_data.humidity}%")
        self.wind_label.config(text=f"{weather_data.wind_speed} m/s")
        self.pressure_label.config(text=f"{weather_data.pressure} hPa")
        self.visibility_label.config(text=f"{weather_data.visibility:.1f} km")
        
        # Convert sunrise/sunset to local time
        sunrise_time = datetime.fromtimestamp(weather_data.sunrise).strftime('%H:%M')
        sunset_time = datetime.fromtimestamp(weather_data.sunset).strftime('%H:%M')
        self.sunrise_label.config(text=sunrise_time)
        self.sunset_label.config(text=sunset_time)
        
        # Try to load weather icon
        self.load_weather_icon(weather_data.icon)
        
        # Update forecast
        if weather_data.forecast:
            self.update_forecast(weather_data.forecast)
    
    def load_weather_icon(self, icon_code):
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        try:
            response = requests.get(icon_url, timeout=5)
            img_data = response.content
            img = Image.open(io.BytesIO(img_data))
            img = img.resize((100, 100), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.icon_label.config(image=photo)
            self.icon_label.image = photo
        except:
            # Fallback to emoji
            emoji_map = {
                '01': '☀️', '02': '⛅', '03': '☁️',
                '04': '☁️', '09': '🌧️', '10': '🌦️',
                '11': '⛈️', '13': '❄️', '50': '🌫️'
            }
            emoji = emoji_map.get(icon_code[:2], '🌤️')
            self.icon_label.config(text=emoji, font=('Helvetica', 48))
    
    def update_forecast(self, forecast_data):
        # Clear previous forecast
        for widget in self.forecast_canvas_frame.winfo_children():
            widget.destroy()
        
        # Create forecast display
        for i, forecast in enumerate(forecast_data[:5]):  # Show next 5 forecasts
            frame = tk.Frame(
                self.forecast_canvas_frame,
                bg=self.colors['light']['secondary'],
                relief=tk.RAISED,
                bd=1
            )
            frame.grid(row=0, column=i, padx=5, pady=5, sticky='nsew')
            self.forecast_canvas_frame.grid_columnconfigure(i, weight=1)
            
            # Date
            date_str = datetime.fromtimestamp(forecast['dt']).strftime('%a %H:%M')
            date_label = tk.Label(
                frame,
                text=date_str,
                font=('Helvetica', 10, 'bold'),
                bg=self.colors['light']['secondary'],
                fg=self.colors['light']['fg']
            )
            date_label.pack(pady=(10, 5))
            
            # Temperature
            temp = forecast['main']['temp'] - 273.15
            if not self.use_celsius:
                temp = temp * 9/5 + 32
            unit = "°C" if self.use_celsius else "°F"
            temp_label = tk.Label(
                frame,
                text=f"{temp:.1f}{unit}",
                font=('Helvetica', 14),
                bg=self.colors['light']['secondary'],
                fg=self.colors['light']['fg']
            )
            temp_label.pack(pady=5)
            
            # Condition
            condition_label = tk.Label(
                frame,
                text=forecast['weather'][0]['main'],
                font=('Helvetica', 10),
                bg=self.colors['light']['secondary'],
                fg=self.colors['light']['fg']
            )
            condition_label.pack(pady=5)
    
    def toggle_unit(self):
        self.use_celsius = not self.use_celsius
        self.unit_btn.config(text="°F" if self.use_celsius else "°C")
        if self.current_weather_data:
            self.update_ui(self.current_weather_data)
    
    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        theme = 'dark' if self.is_dark_mode else 'light'
        colors = self.colors[theme]
        
        # Update theme
        self.theme_btn.config(text="☀️" if self.is_dark_mode else "🌙")
        
        # Update all widgets
        self.update_widget_colors(colors)
    
    def update_widget_colors(self, colors):
        self.main_frame.config(bg=colors['bg'])
        self.header_frame.config(bg=colors['primary'])
        self.title_label.config(bg=colors['primary'])
        self.search_frame.config(bg=colors['bg'])
        self.current_frame.config(bg=colors['bg'])
        self.current_weather_frame.config(bg=colors['secondary'])
        self.icon_label.config(bg=colors['secondary'])
        self.temp_label.config(bg=colors['secondary'], fg=colors['fg'])
        self.details_frame.config(bg=colors['secondary'])
        self.city_name_label.config(bg=colors['secondary'], fg=colors['fg'])
        self.condition_label.config(bg=colors['secondary'], fg=colors['fg'])
        self.feels_like_label.config(bg=colors['secondary'], fg=colors['fg'])
        self.metrics_frame.config(bg=colors['bg'])
        self.forecast_frame.config(bg=colors['bg'])
        self.forecast_label.config(bg=colors['bg'], fg=colors['fg'])
        self.forecast_canvas_frame.config(bg=colors['bg'])
        self.status_bar.config(bg=colors['secondary'], fg=colors['fg'])
        
        # Update metric frames
        for child in self.metrics_frame.winfo_children():
            child.config(bg=colors['secondary'])
            for widget in child.winfo_children():
                widget.config(bg=colors['secondary'], fg=colors['fg'])
        
        # Update forecast frames
        for child in self.forecast_canvas_frame.winfo_children():
            child.config(bg=colors['secondary'])
            for widget in child.winfo_children():
                widget.config(bg=colors['secondary'], fg=colors['fg'])
    
    def show_error(self, message):
        messagebox.showerror("Error", message)
        self.status_bar.config(text="Error occurred")
        self.search_btn.config(state=tk.NORMAL)

def main():
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()