import math
import joblib
import pandas as pd

model = joblib.load("reactor_model.pkl")
print("AI model loaded successfully!")

def reactor_calculation(temperature,concentration,time):
    # Arrhenius parameters
    A = 1e6
    Ea = 80000
    R = 8.314
    
    # Calculate rate constant
    k = A * math.exp(-Ea / (R * temperature))

    # Calculate reaction rate
    reaction_rate = k * concentration

    # Calculate conversion
    conversion = (1 - math.exp(-k * time))

    # Remaining A
    remaining_A = (concentration * (1 - conversion))

    # Product B
    product_B = (concentration * conversion)

    return (reaction_rate,conversion,remaining_A,product_B)

print("OPTIMIZATION VALIDATION")

temperature = float(input("Optimized temperature (K) (range: 400-600K): "))

concentration = float(input("Optimized concentration (M) (range: 2-4M): "))

time_minutes = float(input("Optimized residence time (min) (range: 40-60min): "))

time_seconds = time_minutes * 60

FEATURE_COLUMNS = ["Temperature (K)","Concentration (M)","Time (s)"]

ai_prediction = model.predict(
    pd.DataFrame(
        [[
            temperature,
          concentration,
            time_seconds
        ]],
        columns=FEATURE_COLUMNS
    )

)[0]

(reaction_rate,actual_conversion,remaining_A,product_B) = reactor_calculation(temperature,concentration,time_seconds)

absolute_error = abs(ai_prediction - actual_conversion)
percentage_error = (absolute_error / actual_conversion) * 100
conversion_difference = (ai_prediction - actual_conversion) * 100

print("VALIDATION RESULTS")

print("\nConditions Tested")

print(f"Temperature: "f"{temperature:.2f} K")

print(f"Concentration: "f"{concentration:.2f} M")

print(f"Residence Time: "f"{time_minutes:.2f} min")

print("\nConversion Comparison")

print(f"AI Predicted Conversion: "f"{ai_prediction * 100:.4f}%")

print(f"Original Model Conversion: "f"{actual_conversion * 100:.4f}%")

print(f"Difference: "f"{conversion_difference:.4f} percentage points")

print(f"Relative Error: "f"{percentage_error:.4f}%")

print("\nReactor Results")

print(f"Reaction Rate: "f"{reaction_rate:.6f}")

print(f"Remaining A: "f"{remaining_A:.4f} M")

print(f"Product B: "f"{product_B:.4f} M")
