import fastf1 as ff1
from fastf1 import plotting
import matplotlib.pyplot as plt
import pandas as pd
import os
import time

ff1.Cache.enable_cache("f1cache")
plotting.setup_mpl()

def load_event_schedule(year):
    try:
        ev = ff1.get_event_schedule(year, include_testing=False)
        ev = ev[~ev["EventName"].str.contains("Pre-Season", na=False)]
        return ev
    except Exception as e:
        print("Failed to load event schedule:", e)
        return pd.DataFrame()

def load_session(year, gp_name, session_name, live=False):
    if live:
        try:
            ses = ff1.get_session(year, gp_name, session_name, live=True)
            ses.load(laps=True, telemetry=True, weather=True)
            return ses
        except Exception as e:
            print("No live session found:", e)
            return None
    ev = load_event_schedule(year)
    if ev.empty:
        print("No events found for this year.")
        return None
    try:
        gp = ev[ev["EventName"] == gp_name].iloc[0]
    except IndexError:
        print("Grand Prix not found!")
        return None
    try:
        ses = ff1.get_session(int(year), gp["RoundNumber"], session_name)
        ses.load(laps=True, telemetry=True, weather=True)
        return ses
    except Exception as e:
        print("Failed to load session:", e)
        return None

def select_drivers(drivers):
    print("\nDrivers:", ", ".join(drivers))
    choice = input("Plot all drivers? (y/n): ").strip().lower()
    if choice == 'y':
        return drivers
    sel = input("Enter driver codes separated by commas (e.g., VER,HAM): ")
    sel_drivers = [d.strip().upper() for d in sel.split(",") if d.strip().upper() in drivers]
    return sel_drivers

def select_parameters(laps):
    first_driver = laps['Driver'].iloc[0]
    fastest = laps.pick_driver(first_driver).pick_fastest()
    car_data = fastest.get_car_data().add_distance()
    columns = list(car_data.columns)
    print("\nAvailable telemetry columns:", ", ".join(columns))
    sel = input("Enter telemetry parameters to plot (comma-separated): ")
    sel_params = [p.strip() for p in sel.split(",") if p.strip() in columns]
    return sel_params

def plot_telemetry(ses, drivers, parameters, live=False):
    plt.ion()
    fig, axes = plt.subplots(len(parameters), 1, figsize=(12, 4*len(parameters)), sharex=True)
    if len(parameters) == 1:
        axes = [axes]

    if live:
        try:
            last_lap_numbers = {d: 0 for d in drivers}
            while True:
                for ax in axes:
                    ax.clear()
                lap_info_text = []

                for d in drivers:
                    laps = ses.laps.pick_driver(d).pick_quicklaps()
                    if len(laps) == 0:
                        continue
                    new_laps = laps[laps['LapNumber'] > last_lap_numbers[d]]
                    if new_laps.empty:
                        continue
                    last_lap_numbers[d] = new_laps['LapNumber'].max()
                    for idx, lap in new_laps.iterlaps():
                        try:
                            tel = lap.get_car_data().add_distance()
                        except:
                            continue
                        lap_info_text.append(f"{d}: Lap {lap['LapNumber']} ({lap['LapTime']})")
                        for i, param in enumerate(parameters):
                            if param in tel.columns:
                                axes[i].plot(tel['Distance'], tel[param], label=f"{d} L{lap['LapNumber']}")

                info_str = " | ".join(lap_info_text)
                fig.suptitle(info_str, fontsize=12)
                for i, ax in enumerate(axes):
                    ax.set_ylabel(parameters[i])
                    ax.legend()
                    ax.grid(True)
                axes[-1].set_xlabel("Distance (m)")
                plt.pause(2)
        except KeyboardInterrupt:
            print("\nLive plotting stopped by user.")
            plt.close(fig)
    else:
        for d in drivers:
            laps = ses.laps.pick_driver(d).pick_quicklaps()
            if len(laps) == 0:
                continue
            try:
                lap = laps.pick_fastest()
                tel = lap.get_car_data().add_distance()
            except:
                continue
            for i, param in enumerate(parameters):
                if param in tel.columns:
                    axes[i].plot(tel['Distance'], tel[param], label=f"{d} L{lap['LapNumber']}")
        for i, ax in enumerate(axes):
            ax.set_ylabel(parameters[i])
            ax.legend()
            ax.grid(True)
        axes[-1].set_xlabel("Distance (m)")
        plt.show(block=False)

def main():
    while True:
        print("\n--- F1 Telemetry Viewer ---")
        print("1: Past Session")
        print("2: Live Session")
        mode = input("Select mode (1/2): ").strip()
        if mode == '1':
            year = input("Enter year (e.g., 2025): ").strip()
            try:
                year = int(year)
            except ValueError:
                print("Invalid year input.")
                continue
            gp_name = input("Enter Grand Prix name (exact): ").strip()
            session_name = input("Enter session (FP1, FP2, FP3, Qualifying, Sprint, Race): ").strip()
            ses = load_session(year, gp_name, session_name)
            if ses is None or ses.laps.empty:
                print("Session data not available.")
                continue
        elif mode == '2':
            gp_name = input("Enter Grand Prix name (exact) for live: ").strip()
            session_name = input("Enter session (Race or live session type): ").strip()
            ses = load_session(None, gp_name, session_name, live=True)
            if ses is None:
                print("No live session available.")
                continue
        else:
            print("Invalid option.")
            continue

        drivers = sorted(list(ses.drivers))
        sel_drivers = select_drivers(drivers)
        if not sel_drivers:
            print("No valid drivers selected.")
            continue
        parameters = select_parameters(ses.laps)
        if not parameters:
            print("No valid parameters selected.")
            continue

        plot_telemetry(ses, sel_drivers, parameters, live=(mode=='2'))

        cont = input("\nLoad another session? (y/n): ").strip().lower()
        if cont != 'y':
            print("\nMade by: Samyakraj Bayar")
            break

if __name__ == "__main__":
    os.makedirs("f1cache", exist_ok=True)
    main()
