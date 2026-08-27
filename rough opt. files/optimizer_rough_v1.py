import joblib
import pandas as pd

FEATURE_COLUMNS = ["Temperature (K)", "Concentration (M)", "Time (s)"]

model = joblib.load("reactor_model.pkl")

temperature_range = range(400, 701, 5)

concentration_range = [1, 1.5, 2, 2.5, 3,3.5, 4, 4.5, 5]

time_range = range(1, 31)

conditions = [
    [temperature, concentration, residence_time]
    for temperature in temperature_range
    for concentration in concentration_range
    for residence_time in time_range
]

feature_df = pd.DataFrame(conditions, columns=FEATURE_COLUMNS)

predictions = model.predict(feature_df)

best_index = int(predictions.argmax())
best_conversion = float(predictions[best_index])
temperature, concentration, residence_time = conditions[best_index]

print("\nOPTIMAL REACTOR CONDITIONS")

print("Temperature:", temperature, "K")
print("Concentration:", concentration, "M")
print("Residence time:", residence_time, "s")
print("Predicted conversion:", best_conversion * 100, "%")
