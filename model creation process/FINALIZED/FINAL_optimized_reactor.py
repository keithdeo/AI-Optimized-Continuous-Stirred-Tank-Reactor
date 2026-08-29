import joblib
import sys
import pandas as pd
import numpy as np
import itertools

FEATURE_COLUMNS = ["Temperature (K)", "Concentration (M)", "Time (s)"]

try:
    model = joblib.load("reactor_model.pkl")
    data = pd.read_csv("reaction_data.csv")
except Exception as e:
    print(f"Error loading files: {e}")
    sys.exit(1)

min_trained_temperature = data["Temperature (K)"].min()
max_trained_temperature = data["Temperature (K)"].max()
min_trained_concentration = data["Concentration (M)"].min()
max_trained_concentration = data["Concentration (M)"].max()
min_trained_time = data["Time (s)"].min()
max_trained_time = data["Time (s)"].max()


print("\nAllowed input ranges (must be within both code and training ranges):")
print(f" Temperature (K): {min_trained_temperature:.2f} to {max_trained_temperature:.2f}")
print(f" Concentration (M): {min_trained_concentration:.3f} to {max_trained_concentration:.3f}")
print(f" Time (s): {min_trained_time:.2f} to {max_trained_time:.2f}")

temperature_step = 1.0  
concentration_step = 0.1 
time_step = 1.0 

def is_interactive():
    return sys.stdin is not None and sys.stdin.isatty()

def get_float_input(prompt, default=None):
    if not is_interactive():
        if default is not None:
            return float(default)
        print("\nNo input available. Run this script in a real terminal.")
        sys.exit(1)
    while True:
        try:
            raw = input(prompt)
            if raw.strip() == "" and default is not None:
                return float(default)
            return float(raw)
        except ValueError:
            print("Please enter a valid number.")
        except EOFError:
            if default is not None:
                return float(default)
            print("\nNo input available. Run this script in a real terminal.")
            sys.exit(1)

def get_value(prompt, default=None):
    if default is None:
        return get_float_input(prompt)
    return get_float_input(f"{prompt} [{default}] ", default)

print("\nEnter CURRENT reactor conditions.")
current_temperature = get_value("Current temperature (K): ", round(min_trained_temperature, 2))
current_concentration = get_value("Current concentration (M): ", round(min_trained_concentration, 3))
current_time = get_value("Current residence time (s): ", round(min_trained_time, 2))

print("\nEnter the operating range for the optimizer.")
min_temperature = get_value("Minimum temperature (K): ", round(min_trained_temperature, 2))
max_temperature = get_value("Maximum temperature (K): ", round(max_trained_temperature, 2))
min_concentration = get_value("Minimum concentration (M): ", round(min_trained_concentration, 3))
max_concentration = get_value("Maximum concentration (M): ", round(max_trained_concentration, 3))
min_time = get_value("Minimum residence time (s): ", round(min_trained_time, 2))
max_time = get_value("Maximum residence time (s): ", round(max_trained_time, 2))

print("\nEnter heating parameters.")
mass = get_value("Mass of material (kg): ", 1.0)
cp = get_value("Specific heat capacity Cp (kJ/(kg*K)): ", 4.18)
feed_temperature = get_value("Feed temperature (K): ", 298.15)

print("\nEnter economic parameters.")
energy_price = get_value("Energy price ($/kWh): ", 0.1)
product_value = get_value("Product value at 100% conversion ($): ", 100.0)

if min_temperature > max_temperature or min_concentration > max_concentration or min_time > max_time:
    print("\nError: minimum values cannot exceed maximum values.")
    sys.exit(1)

if min_temperature < 400 or max_temperature > 600 or min_concentration < 2 or max_concentration > 4 or min_time < 40 or max_time > 60:
    print("\nError: Optimization bounds exceed hardcoded constraints.")
    sys.exit(1)

if min_temperature < min_trained_temperature or max_temperature > max_trained_temperature or min_concentration < min_trained_concentration or max_concentration > max_trained_concentration or min_time < min_trained_time or max_time > max_trained_time:
    print("\nError: Optimization bounds are outside the AI training range.")
    sys.exit(1)

def heating_energy(mass, cp, feed_temperature, reactor_temperature):
    return mass * cp * (reactor_temperature - feed_temperature)

current_prediction = model.predict(pd.DataFrame([[current_temperature, current_concentration, current_time]], columns=FEATURE_COLUMNS))[0]
current_energy = heating_energy(mass, cp, feed_temperature, current_temperature)
current_heating_cost = (current_energy / 3600) * energy_price
current_score = (current_prediction * product_value) - current_heating_cost

print("\nSearching for highest optimization peak...")

temp_vals = np.arange(min_temperature, max_temperature + temperature_step, temperature_step)
conc_vals = np.arange(min_concentration, max_concentration + concentration_step, concentration_step)
time_vals = np.arange(min_time, max_time + time_step, time_step)

search_df = pd.DataFrame(list(itertools.product(temp_vals, conc_vals, time_vals)), columns=FEATURE_COLUMNS)

if search_df.empty:
    print("\nError: no valid reactor conditions found.")
    sys.exit(1)

search_df['Predicted_Conversion'] = model.predict(search_df)
search_df['Energy_Required_kJ'] = mass * cp * (search_df['Temperature (K)'] - feed_temperature)
search_df['Heating_Cost_$'] = (search_df['Energy_Required_kJ'] / 3600) * energy_price
search_df['Economic_Score'] = (search_df['Predicted_Conversion'] * product_value) - search_df['Heating_Cost_$']

best_run = search_df.loc[search_df['Economic_Score'].idxmax()]

conversion_improvement_percent = (best_run['Predicted_Conversion'] - current_prediction) * 100
score_improvement = best_run['Economic_Score'] - current_score

print("\nREACTOR COMPARISON")
print(f"{'Metric':<25} {'CURRENT':<15} {'OPTIMIZED':<15}")
print(f"{'Temperature (K)':<25} {current_temperature:<15.2f} {best_run['Temperature (K)']:<15.2f}")
print(f"{'Concentration (M)':<25} {current_concentration:<15.2f} {best_run['Concentration (M)']:<15.2f}")
print(f"{'Time (s)':<25} {current_time:<15.2f} {best_run['Time (s)']:<15.2f}")
print(f"{'Conversion (%)':<25} {current_prediction * 100:<15.2f} {best_run['Predicted_Conversion'] * 100:<15.2f}")
print(f"{'Energy (kJ)':<25} {current_energy:<15.2f} {best_run['Energy_Required_kJ']:<15.2f}")
print(f"{'Heating Cost ($)':<25} {current_heating_cost:<15.2f} {best_run['Heating_Cost_$']:<15.2f}")
print(f"{'Economic Score ($)':<25} {current_score:<15.2f} {best_run['Economic_Score']:<15.2f}")

print("\nIMPROVEMENT")
print(f"Conversion improvement: {conversion_improvement_percent:.2f} percentage points")
print(f"Economic score improvement: ${score_improvement:.2f}\n")
