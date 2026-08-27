import argparse
import joblib
import sys
import pandas as pd


FEATURE_COLUMNS = [
    "Temperature (K)",
    "Concentration (M)",
    "Time (s)"
]

model = joblib.load("reactor_model.pkl")

data = pd.read_csv("reaction_data.csv")

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

    # Economic inputs
    parser.add_argument("--energy-price", type=float)
    parser.add_argument("--product-value", type=float)

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

def is_interactive():

    return (
        sys.stdin is not None
        and sys.stdin.isatty()
    )

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
                "Run this script in a real terminal "
                "where you can type values."
            )

            sys.exit(1)

def get_value(arg_value, prompt):

    if arg_value is not None:

        return arg_value

    return get_float_input(prompt)

args = parse_args()

print("AI REACTOR OPTIMIZATION")

print("\nEnter the operating range "for the optimizer.")


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

print("\nEnter economic parameters.")

energy_price = get_value(
    args.energy_price,
    "Energy price ($/kWh): "
)

product_value = get_value(
    args.product_value,
    "Product value at 100% conversion ($): "
)

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

min_trained_time = (
    min_trained_time_seconds / 60
)

max_trained_time = (
    max_trained_time_seconds / 60
)

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


if min_temperature < min_trained_temperature:

    print(
        "\nError: minimum temperature "
        "is outside the AI training range."
    )

    print(
        f"Training minimum: "
        f"{min_trained_temperature:.2f} K"
    )

    sys.exit(1)


if max_temperature > max_trained_temperature:

    print(
        "\nError: maximum temperature "
        "is outside the AI training range."
    )

    print(
        f"Training maximum: "
        f"{max_trained_temperature:.2f} K"
    )

    sys.exit(1)


if min_concentration < min_trained_concentration:

    print(
        "\nError: minimum concentration "
        "is outside the AI training range."
    )

    print(
        f"Training minimum: "
        f"{min_trained_concentration:.2f} M"
    )

    sys.exit(1)


if max_concentration > max_trained_concentration:

    print(
        "\nError: maximum concentration "
        "is outside the AI training range."
    )

    print(
        f"Training maximum: "
        f"{max_trained_concentration:.2f} M"
    )

    sys.exit(1)


if min_time < min_trained_time:

    print(
        "\nError: minimum residence time "
        "is outside the AI training range."
    )

    print(
        f"Training minimum: "
        f"{min_trained_time:.2f} min"
    )

    sys.exit(1)


if max_time > max_trained_time:

    print(
        "\nError: maximum residence time "
        "is outside the AI training range."
    )

    print(
        f"Training maximum: "
        f"{max_trained_time:.2f} min"
    )

    sys.exit(1)


def heating_energy(
    mass,
    cp,
    feed_temperature,
    reactor_temperature
):

    energy = (
        mass
        * cp
        * (
            reactor_temperature
            - feed_temperature
        )
    )

    return energy

temperature_step = (
    args.temperature_step
)


concentration_step = (
    args.concentration_step
)


time_step = (
    args.time_step
)


# Temperature range

temperature_range = []

temperature = min_temperature

while temperature <= max_temperature:

    temperature_range.append(
        temperature
    )

    temperature += temperature_step


# Concentration range

concentration_range = []

concentration = min_concentration

while concentration <= max_concentration:

    concentration_range.append(
        concentration
    )

    concentration += concentration_step


# Residence-time range

time_range = []

time = min_time

while time <= max_time:

    time_range.append(time)

    time += time_step

if (
    len(temperature_range) == 0
    or len(concentration_range) == 0
    or len(time_range) == 0
):

    print(
        "\nError: one or more search ranges "
        "are empty."
    )

    sys.exit(1)

best_score = float("-inf")

best_conversion = 0

best_conditions = None

best_energy = 0

best_energy_cost = 0

best_conversion_value = 0


print(
    "\nSearching reactor conditions..."
)


for temperature in temperature_range:

    for concentration in concentration_range:

        for time in time_range:

            time_seconds = time * 60

            prediction = model.predict(

                pd.DataFrame(
                    [
                        [
                            temperature,
                            concentration,
                            time_seconds
                        ]
                    ],

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

                best_energy_cost = (
                    heating_cost
                )

                best_conversion_value = (
                    conversion_value
                )



if best_conditions is None:

    print(
        "\nError: no valid reactor "
        "conditions were found."
    )

    sys.exit(1)


temperature, concentration, time = (
    best_conditions
)

print("OPTIMIZATION RESULTS")

print(
    f"Temperature: "
    f"{temperature:.2f} K"
)


print(
    f"Concentration: "
    f"{concentration:.2f} M"
)


print(
    f"Residence Time: "
    f"{time:.2f} min"
)


print(
    f"Predicted Conversion: "
    f"{best_conversion * 100:.2f}%"
)

print(
    f"Feed Temperature: "
    f"{feed_temperature:.2f} K"
)


print(
    f"Heating Energy: "
    f"{best_energy:.2f} kJ"
)


print(
    f"Heating Energy: "
    f"{best_energy / 3600:.4f} kWh"
)

print("\nEconomic Results")


print(
    f"Conversion Value: "
    f"${best_conversion_value:.2f}"
)


print(
    f"Heating Cost: "
    f"${best_energy_cost:.2f}"
)


print(
    f"Economic Score: "
    f"${best_score:.2f}"
)
