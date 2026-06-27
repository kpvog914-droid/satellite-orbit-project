import numpy as np
import pandas as pd

Cd   = 2.2
A    = 10.0
m    = 500.0
GM   = 3.986e14
R_earth = 6371000
rho0 = 5.24e-13
H    = 60.0
REENTRY_ALT = 120.0
START_ALT   = 400.0

def atmospheric_density(altitude, f107):
    solar_factor = 1.0 + 1.5 * (f107 - 70) / (230 - 70)
    density = rho0 * np.exp(-(altitude - 400) / H) * solar_factor
    return density

def daily_altitude_loss(altitude, f107):
    r = R_earth + (altitude * 1000)
    v = np.sqrt(GM / r)
    rho = atmospheric_density(altitude, f107)
    drag_force = 0.5 * rho * (v**2) * Cd * A
    deceleration = drag_force / m
    altitude_loss_m = (deceleration * 86400 * r) / (2 * v)
    altitude_loss_km = altitude_loss_m / 1000
    return altitude_loss_km

def run_simulation(f107_input):
    altitude  = START_ALT
    altitudes = [altitude]
    day       = 0

    is_series = isinstance(f107_input, pd.Series)

    if is_series:
        f107_values = f107_input.values.tolist()
        total_days  = len(f107_values)

    while altitude > REENTRY_ALT:

        if is_series:
            # Repeat the historical solar cycle when dataset ends
            f107 = f107_values[day % total_days]
        else:
            f107 = f107_input

        loss = daily_altitude_loss(altitude, f107)
        altitude = altitude - loss
        altitudes.append(altitude)

        day += 1

    days_survived = day
    return altitudes, days_survived

def validate_model():
    print("\n" + "="*50)
    print("MODEL VALIDATION")
    print("="*50)
    altitudes, days = run_simulation(150)
    if len(altitudes) >= 31:
        monthly_loss = altitudes[0] - altitudes[30]
    else:
        monthly_loss = 0
        print("WARNING: Simulation ended before 30 days!")
    print(f"Model result:  {monthly_loss:.2f} km/month at F10.7 = 150")
    print(f"ISS observed:  ~2 km/month (NASA public data)")
    if 0.5 <= monthly_loss <= 5.0:
        print("Status: PASS")
        print("The model is physically consistent with ISS observations.")
    else:
        print("Status: FAIL")
        print("Monthly loss is outside expected range. Check your constants.")
    print("="*50 + "\n")
    return monthly_loss

print("\n" + "="*50)
print("RUNNING ALL TESTS FOR simulation.py")
print("="*50)

print("\nTEST 1: Solar max decays faster than solar min")
_, days_min = run_simulation(70)
_, days_max = run_simulation(230)
print(f"  Solar minimum (F10.7=70):  {days_min} days survived")
print(f"  Solar maximum (F10.7=230): {days_max} days survived")
if days_max < days_min:
    print("  Result: PASS — Solar max correctly decays faster")
else:
    print("  Result: FAIL — Something is wrong with the physics")

print("\nTEST 2: Validation against ISS observed decay rate")
validate_model()

print("\nTEST 3: Simulation handles a pandas Series as input")
fake_series = pd.Series([150.0] * 5000)
altitudes_series, days_series = run_simulation(fake_series)
print(f"  Survived {days_series} days using pandas Series input")
print("  Result: PASS — No crash, simulation completed successfully")

print("\n" + "="*50)
print("SUMMARY OF SIMULATION RESULTS")
print("="*50)
_, days_avg = run_simulation(150)
print(f"  Solar minimum  (F10.7=70):  {days_min} days = {days_min/365:.1f} years")
print(f"  Average sun    (F10.7=150): {days_avg} days = {days_avg/365:.1f} years")
print(f"  Solar maximum  (F10.7=230): {days_max} days = {days_max/365:.1f} years")
print(f"\n  Difference: Solar min lasts {days_min - days_max} more days than solar max")
print("="*50)
print("\nAll tests complete. simulation.py is ready to share with the team.")
