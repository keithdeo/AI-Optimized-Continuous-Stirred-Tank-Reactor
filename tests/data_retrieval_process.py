import random
import pandas as pd
import math

def calculations(temp, conc, time):
    A = 1e6
    Ea = 80000
    R = 8.314
    k = A * math.exp(-Ea / (R * temp))
    reaction_rate = k * conc
    conversion_A_to_B = 1 - math.exp(-k * time)
    remainder_A = conc * (1 - conversion_A_to_B)
    product_B = conc * conversion_A_to_B
    return reaction_rate, conversion_A_to_B, remainder_A, product_B


def get_positive_float(prompt):
    while True:
        try:
            value = float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")
            continue
        if value <= 0:
            print("Please enter a positive number.")
            continue
        return value


def main():
    basis_temp_range = get_positive_float("Enter Temperature range (Kelvin, +-100): ")
    basis_conc_range = get_positive_float("Enter Concentration range (Molar, +-1): ")
    basis_time_range = get_positive_float("Enter Time range (seconds, +-10): ")

    rows = []
    for _ in range(10000):
        temp = random.uniform(basis_temp_range - 100, basis_temp_range + 100)
        conc = random.uniform(basis_conc_range - 1, basis_conc_range + 1)
        duration = random.uniform(basis_time_range - 10, basis_time_range + 10)

        reaction_rate, conversion_A_to_B, remainder_A, product_B = calculations(temp, conc, duration)

        rows.append({
            'Temperature (K)': temp,
            'Concentration (M)': conc,
            'Time (s)': duration,
            'Reaction Rate': reaction_rate,
            'Conversion A to B': conversion_A_to_B,
            'Remainder A': remainder_A,
            'Product B': product_B
        })

    df = pd.DataFrame(rows)
    df.to_csv('reaction_data.csv', index=False)
    print('Saved 10000 rows to reaction_data.csv')


if __name__ == '__main__':
    main()
