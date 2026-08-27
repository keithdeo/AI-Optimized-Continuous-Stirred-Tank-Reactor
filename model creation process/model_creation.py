import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

data = pd.read_csv("reaction_data.csv")

print("Dataset loaded successfully!")
print(data.head())

X = data[
    ["Temperature (K)", "Concentration (M)", "Time (s)"]
]

y = data["Conversion A to B"]
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))

model = RandomForestRegressor(n_estimators=100,random_state=42)

print("\nTraining model...")

model.fit(X_train, y_train) # model training starts here

print("Model trained successfully!")

predictions = model.predict(X_test) # model prediction starts here

error = mean_absolute_error(
    y_test,
    predictions
)

print("\nModel Performance")
print("Mean Absolute Error:", error)

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
