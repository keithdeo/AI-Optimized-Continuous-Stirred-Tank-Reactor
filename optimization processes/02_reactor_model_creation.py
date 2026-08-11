import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error


# -----------------------------------
# 1. Load the reactor dataset
# -----------------------------------

data = pd.read_csv("reaction_data.csv")

print("Dataset loaded successfully!")
print(data.head())


# -----------------------------------
# 2. Define inputs and target
# -----------------------------------

X = data[
    ["Temperature (K)", "Concentration (M)", "Time (s)"]
]

y = data["Conversion A to B"]


# -----------------------------------
# 3. Split data into training/testing
# -----------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# -----------------------------------
# 4. Create the Random Forest model
# -----------------------------------

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)


# -----------------------------------
# 5. Train the model
# -----------------------------------

print("\nTraining model...")

model.fit(X_train, y_train) # model training starts here

print("Model trained successfully!")


# -----------------------------------
# 6. Test the model
# -----------------------------------

predictions = model.predict(X_test) # model prediction starts here


# -----------------------------------
# 7. Calculate model error
# -----------------------------------

error = mean_absolute_error(
    y_test,
    predictions
)

print("\nModel Performance")
print("-------------------------")
print("Mean Absolute Error:", error)


# -----------------------------------
# 8. Test a new reactor condition
# -----------------------------------

new_conditions = pd.DataFrame(
    [[
        500,    # Temperature (K)
        2,      # Concentration (M)
        10      # Time (s)
    ]],
    columns=["Temperature (K)", "Concentration (M)", "Time (s)"]
)

prediction = model.predict(new_conditions)

print("\nNew Reactor Prediction")
print("-------------------------")
print("Temperature: 500 K")
print("Concentration: 2 M")
print("Time: 10 s")
print("Predicted conversion:", prediction[0] * 100, "%")


# -----------------------------------
# 9. Save the trained model
# -----------------------------------

joblib.dump(
    model,
    "reactor_model.pkl"
)

print("\nModel saved successfully!")
print("Created file: reactor_model.pkl")

print(data[[
    "Temperature (K)",
    "Concentration (M)",
    "Time (s)"
]].describe())