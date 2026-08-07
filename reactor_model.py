import math
from time import time

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

def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")

temperature_A = get_float_input("Enter temperature value (Kelvin): ")
concentration_A = get_float_input("Enter concentration value: ")
residence_time_A = get_float_input("Enter residence time value: ")

a, b, c, d = calculations(temperature_A, concentration_A, residence_time_A)

print("Reaction rate:", a, "mol/L/min")
print("Conversion rate:", b * 100, "%")
print("Remaining concentration of A:", c, "mol/L")
print("Concentration of product B:", d, "mol/L")