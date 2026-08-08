import os
import joblib

# theoretical cost analysis, assigns 'cost' values for heating & time in order to minimize cost in conversion process
def objective(conversion, temperature, concentration, time_min):
    product_value = conversion * 1000
    heating_cost = temperature * 2
    residence_cost = time_min * 10

    score = product_value - heating_cost - residence_cost

    return score

model_path = "reactor_model.pkl"
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found: {model_path}")

model = joblib.load(model_path)

temperature_range = range(400, 701, 5)
concentration_range = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
time_min_range = range(1, 31)

best_conversion = 0
best_conditions = None

for temperature in temperature_range:

    for concentration in concentration_range:

        for time_min in time_min_range:

            prediction = model.predict([
                [temperature, concentration, time_min]
            ])[0]

            if prediction > best_conversion:
                best_conversion = prediction

                best_conditions = (
                    temperature,
                    concentration,
                    time_min
                )

temperature, concentration, time_min = best_conditions

print("\nOPTIMAL CONDITIONS")
print("-----------------------")
print(f"Temperature: {temperature} K")
print(f"Concentration: {concentration} mol/L")
print(f"Residence time: {time_min} min")
print(f"Predicted conversion: {best_conversion * 100:.2f}%")

score = objective(
    best_conversion,
    temperature,
    concentration,
    time_min
)

best_score = score
print(f"Objective score: {best_score:.2f}")

current_temperature = float(
    input("Current temperature (K): ")
)
current_concentration = float(
    input("Current concentration (mol/L): ")
)
current_time = float(
    input("Current residence time (min): ")
)

current_prediction = model.predict([
    [
        current_temperature,
        current_concentration,
        current_time
    ]
])[0]
print(f"Current predicted conversion: {current_prediction * 100:.2f}%")
