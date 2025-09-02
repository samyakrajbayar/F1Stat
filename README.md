# F1Stat
F1Stat is a Python-based application that leverages the FastF1  library to fetch, analyze, and visualize live and historical or live Formula 1 race data.



1. Requirements

Make sure you have the following installed:

1) Python 3.12 or higher
2) Required Python libraries:

(use this code in the terminal):
  pip install fastf1 matplotlib pandas
  Optional (for caching and speed): os is part of standard Python.



2. File Setup

1) Save the Python code as, for example:
   f1_telemetry_app.py

2) Create a folder called f1cache in the same directory (the code will also create it automatically). This is used by FastF1 to store cached session data for faster loading.



3. Running the App

Run the app in plain Python (terminal or command prompt):
  python f1_telemetry_app.py
  (You will see a terminal-based interactive menu.)



4. Menu Options

Main Menu
--- F1 Telemetry Viewer ---
1: Past Session
2: Live Session
Select mode (1/2):

  1 → Load a past F1 session.
  2 → Load live session telemetry (if a live session is ongoing).

  Past Session Mode
  You’ll be prompted to enter:
    Year (e.g., 2025)
    Grand Prix Name (exactly as in FastF1, e.g., “Dutch Grand Prix”)
    Session (FP1, FP2, FP3, Qualifying, Sprint, Race)

  If the session exists, the code will:
    Load laps, telemetry, and weather.
    List available drivers and parameters.

  Live Session Mode
  You’ll be prompted to enter:
    Grand Prix Name (current live session)
    Session Type (usually “Race” or live session type)
    (The code will try to fetch live telemetry (may fail if no live session is available or network access is blocked).)



5. Selecting Drivers and Parameters

After loading a session:
  The app will list all drivers.
  You can choose to plot all drivers by typing y, or select a subset by entering driver codes separated by commas (e.g., VER,HAM).
  Next, you will be prompted to choose telemetry parameters to plot (e.g., Speed,Throttle,Brake). Only valid telemetry columns will be plotted.



6. Plotting

The app will generate interactive Matplotlib plots.
Each line is labeled with Driver + Lap Number.
The legend ensures you can identify drivers and laps.
For live sessions, the plot updates dynamically with new lap data every ~2 seconds.
(For past sessions, the plot shows the data once.)



7. Navigation

Stop live plotting: Press Ctrl+C in the terminal.

After a session finishes, you’ll be asked:
    Load another session? (y/n):
    (Type y to load a new session or n to exit.)


8. Things to Note

Ensure correct spelling for Grand Prix and session names, otherwise the session may not load.
Use fast internet for live telemetry; it may fail if network or session is unavailable.
Only telemetry parameters available in the session can be plotted.
You can resize the Matplotlib window for better visualization.






