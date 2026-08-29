import joblib
import sys
import pandas as pd


FEATURE_COLUMNS = ["Temperature (K)","Concentration (M)","Time (s)"]

try:
    model = joblib.load("reactor_model.pkl")
except FileNotFoundError:
    print("Error: trained model 'reactor_model.pkl' not found.")
    sys.exit(1)

try:
    data = pd.read_csv("reaction_data.csv")
except FileNotFoundError:
    print("Error: training data 'reaction_data.csv' not found.")
    sys.exit(1)

min_trained_temperature = data["Temperature (K)"].min()
max_trained_temperature = data["Temperature (K)"].max()
mean_trained_temperature = data["Temperature (K)"].mean()

min_trained_concentration = data["Concentration (M)"].min()
max_trained_concentration = data["Concentration (M)"].max()
mean_trained_concentration = data["Concentration (M)"].mean()

min_trained_time = data["Time (s)"].min()
max_trained_time = data["Time (s)"].max()
mean_trained_time = data["Time (s)"].mean()

print("\nAllowed input ranges (must be within both code and training ranges):")
print(f" Temperature (K): {min_trained_temperature:.2f} - {max_trained_temperature:.2f}")
print(f" Concentration (M): {min_trained_conc:.3f} - {max_trained_conc:.3f}")
print(f" Time (s): {min_trained_time:.2f} - {max_trained_time:.2f}")


# Default search step sizes (used when searching ranges)
temperature_step = 5
concentration_step = 0.5
time_step = 1

def is_interactive():
    return ( sys.stdin is not None and sys.stdin.isatty())

def get_float_input(prompt):
    if not is_interactive():
        print(
            "\nNo input available. "
            "Run this script in a real terminal or provide defaults."
        )

        sys.exit(1)

    while True:
        try:
            raw = input(prompt)
            
        except ValueError:
            print("Please enter a valid number.")
        except EOFError:
            print("\nNo input available. Run this script in a real terminal.")
            sys.exit(1)

def get_value(prompt):
    return prompt;

print("\nEnter CURRENT reactor conditions.")
print("These are the unoptimized conditions.")

current_temperature = get_value(
    "Current temperature (K): ",
    round(mean_trained_temperature, 2)
)


current_concentration = get_value(
    "Current concentration (M): ",
    round(mean_trained_concentration, 3)
)


current_time = get_value(
    "Current residence time (s): ",
    round(mean_trained_time, 2)
)

print("\nEnter the operating range")
print("for the optimizer.")
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

if min_temperature > max_temperature:

    print(
        "\nError: minimum temperature "
        "cannot exceed maximum temperature."
    )

    sys.exit(1)

if min_concentration > max_concentration:

    print(
        "\nError: minimum concentration "
        "cannot exceed maximum concentration."
    )

    sys.exit(1)

if min_time > max_time:

    print(
        "\nError: minimum residence time "
        "cannot exceed maximum residence time."
    )

    sys.exit(1)


if min_temperature < 400:

    print(
        "\nError: minimum temperature "
        "must be greater than 400 K."
    )

    sys.exit(1)

if max_temperature > 600:

    print(
        "\nError: maximum temperature "
        "must be less than 600 K."
    )

    sys.exit(1)

if min_concentration < 2:

    print(
        "\nError: minimum concentration "
        "must be greater than 2 M."
    )

    sys.exit(1)

if max_concentration > 4:

    print(
        "\nError: maximum concentration "
        "must be less than 4 M."
    )

    sys.exit(1)


if min_time < 40:

    print(
        "\nError: minimum time "
        "must be greater than 40 s."
    )

    sys.exit(1)

if max_time > 60:

    print(
        "\nError: maximum time "
        "must be less than 60 s."
    )

    sys.exit(1)

if min_temperature < min_trained_temperature:

    print("\nError: minimum temperature is outside training range.")

    sys.exit(1)


if max_temperature > max_trained_temperature:

    print("\nError: maximum temperature is outside training range.")

    sys.exit(1)


if min_concentration < min_trained_concentration:

    print("\nError: minimum concentration is outside training range.")

    sys.exit(1)


if max_concentration > max_trained_concentration:

    print("\nError: maximum concentration is outside training range.")

    sys.exit(1)


if min_time < min_trained_time:

    print("\nError: minimum time is outside training range.")

    sys.exit(1)


if max_time > max_trained_time:

    print("\nError: maximum time is outside training range.")

    sys.exit(1)

def heating_energy(mass,cp,feed_temperature,reactor_temperature):
    return (mass * cp * (reactor_temperature - feed_temperature))


current_time_seconds = current_time

current_prediction = model.predict(
    pd.DataFrame(
        [[
            current_temperature,
            current_concentration,
            current_time_seconds
        ]],
        columns=FEATURE_COLUMNS
    )
)[0]


current_energy = heating_energy(
    mass,
    cp,
    feed_temperature,
    current_temperature
)


current_energy_kwh = (
    current_energy / 3600
)


current_heating_cost = (
    current_energy_kwh
    * energy_price
)


current_conversion_value = (
    current_prediction
    * product_value
)


current_score = (
    current_conversion_value
    - current_heating_cost
)

temperature_range = []

temperature = min_temperature

while temperature <= max_temperature:

    temperature_range.append(temperature)

    temperature += temperature_step


concentration_range = []

concentration = min_concentration

while concentration <= max_concentration:

    concentration_range.append(concentration)

    concentration += concentration_step


time_range = []

time = min_time

while time <= max_time:

    time_range.append(time)

    time += time_step

best_score = float("-inf")

best_conversion = 0

best_conditions = None

best_energy = 0

best_energy_cost = 0

best_conversion_value = 0

for temperature in temperature_range:

    for concentration in concentration_range:

        for time in time_range:

            time_seconds = time


            prediction = model.predict(
                pd.DataFrame(
                    [[
                        temperature,
                        concentration,
                        time_seconds
                    ]],
                    columns=FEATURE_COLUMNS
                )
            )[0]


            energy = heating_energy(
                mass,
                cp,
                feed_temperature,
                temperature
            )


            energy_kwh = (
                energy / 3600
            )


            heating_cost = (
                energy_kwh
                * energy_price
            )


            conversion_value = (
                prediction
                * product_value
            )


            score = (
                conversion_value
                - heating_cost
            )


            if score > best_score:

                best_score = score

                best_conversion = prediction

                best_conditions = (
                    temperature,
                    concentration,
                    time
                )

                best_energy = energy

                best_energy_cost = heating_cost

                best_conversion_value = (
                    conversion_value
                )

if best_conditions is None:

    print(
        "\nError: no valid reactor conditions found."
    )

    sys.exit(1)


temperature, concentration, time = (
    best_conditions
)

conversion_improvement = (
    best_conversion
    - current_prediction
)


conversion_improvement_percent = (
    conversion_improvement
    * 100
)


score_improvement = (
    best_score
    - current_score
)

print("REACTOR COMPARISON")

print(
    f"Temperature (K)     "
    f"{current_temperature:10.2f}     "
    f"{temperature:10.2f}"
)


print(
    f"Concentration (M)   "
    f"{current_concentration:10.2f}     "
    f"{concentration:10.2f}"
)


print(
    f"Time (s)           "
    f"{current_time:10.2f}     "
    f"{time:10.2f}"
)


print(
    f"Conversion (%)       "
    f"{current_prediction * 100:10.2f}     "
    f"{best_conversion * 100:10.2f}"
)


print(
    f"Energy (kJ)          "
    f"{current_energy:10.2f}     "
    f"{best_energy:10.2f}"
)


print(
    f"Heating Cost ($)     "
    f"{current_heating_cost:10.2f}     "
    f"{best_energy_cost:10.2f}"
)


print(
    f"Economic Score ($)   "
    f"{current_score:10.2f}     "
    f"{best_score:10.2f}"
)

print("IMPROVEMENT")

print(
    f"Conversion improvement: "
    f"{conversion_improvement_percent:.2f} percentage points"
)


print(
    f"Economic score improvement: "
    f"${score_improvement:.2f}"
)
