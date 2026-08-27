import argparse
import joblib
import sys
import pandas as pd

FEATURE_COLUMNS = ["Temperature (K)", "Concentration (M)", "Time (s)"]

model = joblib.load("reactor_model.pkl")

print("AI model loaded successfully!")

def parse_args():
    parser = argparse.ArgumentParser(
        description="Optimize reactor conditions using a trained AI model."
    )

    parser.add_argument("--min-temperature", type=float)
    parser.add_argument("--max-temperature", type=float)
    parser.add_argument("--min-concentration", type=float)
    parser.add_argument("--max-concentration", type=float)
    parser.add_argument("--min-time", type=float)
    parser.add_argument("--max-time", type=float)
    parser.add_argument("--mass", type=float)
    parser.add_argument("--cp", type=float)
    parser.add_argument("--feed-temperature", type=float)
    parser.add_argument("--temperature-step", type=float, default=5)
    parser.add_argument("--concentration-step", type=float, default=0.5)
    parser.add_argument("--time-step", type=float, default=1)

    return parser.parse_args()


def is_interactive():
    return sys.stdin is not None and sys.stdin.isatty()


def get_float_input(prompt):
    if not is_interactive():
        print("\nNo input available. Run this script in a real terminal or pass values with command-line arguments.")
        sys.exit(1)

    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")
        except EOFError:
            print("\nNo input available. Run this script in a real terminal where you can type values.")
            sys.exit(1)


def get_value(arg_value, prompt):
    if arg_value is not None:
        return arg_value
    return get_float_input(prompt)

args = parse_args()

print("AI REACTOR OPTIMIZATION")
print("\nEnter the operating range for the optimizer.")

# Temperature range
min_temperature = get_value(
    args.min_temperature,
    "Minimum temperature (K): "
)

max_temperature = get_value(
    args.max_temperature,
    "Maximum temperature (K): "
)


# Concentration range
min_concentration = get_value(
    args.min_concentration,
    "Minimum concentration (mol/L): "
)

max_concentration = get_value(
    args.max_concentration,
    "Maximum concentration (mol/L): "
)


# Residence time range
min_time = get_value(
    args.min_time,
    "Minimum residence time (min): "
)

max_time = get_value(
    args.max_time,
    "Maximum residence time (min): "
)

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

# Validate range inputs
if min_temperature > max_temperature:
    print("\nError: minimum temperature cannot exceed maximum temperature.")
    sys.exit(1)

if min_concentration > max_concentration:
    print("\nError: minimum concentration cannot exceed maximum concentration.")
    sys.exit(1)

if min_time > max_time:
    print("\nError: minimum residence time cannot exceed maximum residence time.")
    sys.exit(1)

if args.temperature_step <= 0 or args.concentration_step <= 0 or args.time_step <= 0:
    print("\nError: step sizes must be positive numbers.")
    sys.exit(1)

def heating_energy(
    mass,
    cp,
    feed_temperature,
    reactor_temperature
):

    energy = mass * cp * (
        reactor_temperature - feed_temperature
    )

    return energy

best_conversion = 0

best_conditions = None


temperature_step = int(args.temperature_step)

concentration_step = float(args.concentration_step)

time_step = int(args.time_step)


temperature_range = range(
    int(min_temperature),
    int(max_temperature) + 1,
    temperature_step
)


# Generate concentration values
concentration_range = []

concentration = min_concentration

while concentration <= max_concentration:

    concentration_range.append(concentration)

    concentration += concentration_step


time_range = range(
    int(min_time),
    int(max_time) + 1,
    time_step
)

if len(temperature_range) == 0 or len(concentration_range) == 0 or len(time_range) == 0:
    print("\nError: one or more search ranges are empty. Check your min/max values and step sizes.")
    sys.exit(1)

print("\nSearching reactor conditions...")

for temperature in temperature_range:

    for concentration in concentration_range:

        for time in time_range:

            # Ask AI for predicted conversion
            prediction = model.predict(
                pd.DataFrame(
                    [[temperature, concentration, time]],
                    columns=FEATURE_COLUMNS
                )
            )[0]

            # Check if this is the best result

            if prediction > best_conversion:

                best_conversion = prediction

                best_conditions = (
                    temperature,
                    concentration,
                    time
                )

if best_conditions is None:
    print("\nError: no valid reactor conditions were found. Check your input values and search steps.")
    sys.exit(1)

temperature, concentration, time = best_conditions

energy = heating_energy(
    mass,
    cp,
    feed_temperature,
    temperature
)
print("OPTIMIZATION RESULTS")
print("\nOptimal Conditions")

print(
    f"Temperature: {temperature} K"
)

print(
    f"Concentration: {concentration:.2f} mol/L"
)

print(
    f"Residence Time: {time} min"
)

print(
    f"Predicted Conversion: "
    f"{best_conversion * 100:.2f}%"
)

print("\nHeating Requirements")
print(
    f"Feed Temperature: "
    f"{feed_temperature} K"
)

print(
    f"Heating Energy: "
    f"{energy:.2f} kJ"
)

print("\n======================================")
