import argparse
import joblib
import sys
import pandas as pd


FEATURE_COLUMNS = [
    "Temperature (K)",
    "Concentration (M)",
    "Time (s)"
]


# -----------------------------------
# 1. Load the trained AI model
# -----------------------------------

model = joblib.load("reactor_model.pkl")
data = pd.read_csv("reaction_data.csv")

print("AI model loaded successfully!")


# -----------------------------------
# 2. Command-line arguments
# -----------------------------------

def parse_args():

    parser = argparse.ArgumentParser(
        description="Optimize reactor conditions using a trained AI model."
    )

    # Optimization ranges
    parser.add_argument("--min-temperature", type=float)
    parser.add_argument("--max-temperature", type=float)

    parser.add_argument("--min-concentration", type=float)
    parser.add_argument("--max-concentration", type=float)

    parser.add_argument("--min-time", type=float)
    parser.add_argument("--max-time", type=float)

    # Current / unoptimized conditions
    parser.add_argument("--current-temperature", type=float)
    parser.add_argument("--current-concentration", type=float)
    parser.add_argument("--current-time", type=float)

    # Heating parameters
    parser.add_argument("--mass", type=float)
    parser.add_argument("--cp", type=float)
    parser.add_argument("--feed-temperature", type=float)

    # Economic parameters
    parser.add_argument("--energy-price", type=float)
    parser.add_argument("--product-value", type=float)

    # Search step sizes
    parser.add_argument(
        "--temperature-step",
        type=float,
        default=5
    )

    parser.add_argument(
        "--concentration-step",
        type=float,
        default=0.5
    )

    parser.add_argument(
        "--time-step",
        type=float,
        default=1
    )

    return parser.parse_args()


# -----------------------------------
# 3. Check interactive input
# -----------------------------------

def is_interactive():

    return (
        sys.stdin is not None
        and sys.stdin.isatty()
    )


# -----------------------------------
# 4. Get numerical input
# -----------------------------------

def get_float_input(prompt):

    if not is_interactive():

        print(
            "\nNo input available. "
            "Run this script in a real terminal "
            "or pass values with command-line arguments."
        )

        sys.exit(1)

    while True:

        try:

            return float(input(prompt))

        except ValueError:

            print("Please enter a valid number.")

        except EOFError:

            print(
                "\nNo input available. "
                "Run this script in a real terminal."
            )

            sys.exit(1)


# -----------------------------------
# 5. Use argument if provided,
# otherwise ask user
# -----------------------------------

def get_value(arg_value, prompt):

    if arg_value is not None:

        return arg_value

    return get_float_input(prompt)


# -----------------------------------
# 6. Parse arguments
# -----------------------------------

args = parse_args()


print("\n======================================")
print("       AI REACTOR OPTIMIZATION")
print("======================================")


# -----------------------------------
# 7. Get CURRENT reactor conditions
# -----------------------------------

print("\nEnter CURRENT reactor conditions.")
print("These are the unoptimized conditions.")


current_temperature = get_value(
    args.current_temperature,
    "Current temperature (K): "
)


current_concentration = get_value(
    args.current_concentration,
    "Current concentration (M): "
)


current_time = get_value(
    args.current_time,
    "Current residence time (min): "
)


# -----------------------------------
# 8. Get optimization ranges
# -----------------------------------

print("\nEnter the operating range")
print("for the optimizer.")


min_temperature = get_value(
    args.min_temperature,
    "Minimum temperature (K): "
)


max_temperature = get_value(
    args.max_temperature,
    "Maximum temperature (K): "
)


min_concentration = get_value(
    args.min_concentration,
    "Minimum concentration (M): "
)


max_concentration = get_value(
    args.max_concentration,
    "Maximum concentration (M): "
)


min_time = get_value(
    args.min_time,
    "Minimum residence time (min): "
)


max_time = get_value(
    args.max_time,
    "Maximum residence time (min): "
)


# -----------------------------------
# 9. Heating parameters
# -----------------------------------

print("\nEnter heating parameters.")


mass = get_value(
    args.mass,
    "Mass of material (kg): "
)


cp = get_value(
    args.cp,
    "Specific heat capacity Cp (kJ/(kg*K)): "
)


feed_temperature = get_value(
    args.feed_temperature,
    "Feed temperature (K): "
)


# -----------------------------------
# 10. Economic parameters
# -----------------------------------

print("\nEnter economic parameters.")


energy_price = get_value(
    args.energy_price,
    "Energy price ($/kWh): "
)


product_value = get_value(
    args.product_value,
    "Product value at 100% conversion ($): "
)


# -----------------------------------
# 11. Training-data ranges
# -----------------------------------

min_trained_temperature = (
    data["Temperature (K)"].min()
)

max_trained_temperature = (
    data["Temperature (K)"].max()
)

min_trained_concentration = (
    data["Concentration (M)"].min()
)

max_trained_concentration = (
    data["Concentration (M)"].max()
)

min_trained_time_seconds = (
    data["Time (s)"].min()
)

max_trained_time_seconds = (
    data["Time (s)"].max()
)

# Convert seconds to minutes

min_trained_time = (
    min_trained_time_seconds / 60
)

max_trained_time = (
    max_trained_time_seconds / 60
)


# -----------------------------------
# 12. Validate optimization ranges
# -----------------------------------

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


if args.temperature_step <= 0:

    print(
        "\nError: temperature step "
        "must be positive."
    )

    sys.exit(1)


if args.concentration_step <= 0:

    print(
        "\nError: concentration step "
        "must be positive."
    )

    sys.exit(1)


if args.time_step <= 0:

    print(
        "\nError: time step "
        "must be positive."
    )

    sys.exit(1)


# -----------------------------------
# 13. Validate against AI training range
# -----------------------------------

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


# -----------------------------------
# 14. Heating energy function
# -----------------------------------

def heating_energy(
    mass,
    cp,
    feed_temperature,
    reactor_temperature
):

    return (
        mass
        * cp
        * (
            reactor_temperature
            - feed_temperature
        )
    )


# -----------------------------------
# 15. Calculate CURRENT reactor
# performance
# -----------------------------------

current_time_seconds = current_time * 60


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


# -----------------------------------
# 16. Create optimization ranges
# -----------------------------------

temperature_range = []

temperature = min_temperature

while temperature <= max_temperature:

    temperature_range.append(temperature)

    temperature += args.temperature_step


concentration_range = []

concentration = min_concentration

while concentration <= max_concentration:

    concentration_range.append(concentration)

    concentration += args.concentration_step


time_range = []

time = min_time

while time <= max_time:

    time_range.append(time)

    time += args.time_step


# -----------------------------------
# 17. Initialize optimization
# -----------------------------------

best_score = float("-inf")

best_conversion = 0

best_conditions = None

best_energy = 0

best_energy_cost = 0

best_conversion_value = 0


# -----------------------------------
# 18. Search for optimal conditions
# -----------------------------------

print("\nSearching reactor conditions...")


for temperature in temperature_range:

    for concentration in concentration_range:

        for time in time_range:

            time_seconds = time * 60


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


# -----------------------------------
# 19. Make sure optimization worked
# -----------------------------------

if best_conditions is None:

    print(
        "\nError: no valid reactor conditions found."
    )

    sys.exit(1)


temperature, concentration, time = (
    best_conditions
)


# -----------------------------------
# 20. Calculate improvement
# -----------------------------------

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


# -----------------------------------
# 21. Display comparison
# -----------------------------------

print("\n======================================")
print("       REACTOR COMPARISON")
print("======================================")


print("\n                    CURRENT       OPTIMIZED")
print("------------------------------------------------")


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
    f"Time (min)           "
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


# -----------------------------------
# 22. Display improvements
# -----------------------------------

print("\n======================================")
print("             IMPROVEMENT")
print("======================================")


print(
    f"Conversion improvement: "
    f"{conversion_improvement_percent:.2f} percentage points"
)


print(
    f"Economic score improvement: "
    f"${score_improvement:.2f}"
)


print("\n======================================")