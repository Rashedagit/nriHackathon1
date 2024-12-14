# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

# Generate simulated traffic data (in real use case, you'd have actual traffic data)
np.random.seed(42)
num_samples = 1000

# Simulating traffic data: (time of day, day of week, weather condition, traffic volume)
time_of_day = np.random.choice([6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17], num_samples)  # hours
day_of_week = np.random.choice([0, 1, 2, 3, 4, 5, 6], num_samples)  # 0: Monday, 6: Sunday
weather_condition = np.random.choice([0, 1], num_samples)  # 0: Clear, 1: Rainy (binary weather)
traffic_volume = (time_of_day * 10) + (day_of_week * 20) + (weather_condition * 50) + np.random.normal(0, 30, num_samples)

# Create a DataFrame
data = pd.DataFrame({
    'time_of_day': time_of_day,
    'day_of_week': day_of_week,
    'weather_condition': weather_condition,
    'traffic_volume': traffic_volume
})

# Display first few rows of the data
print(data.head())

# Features and target
X = data[['time_of_day', 'day_of_week', 'weather_condition']]  # Features
y = data['traffic_volume']  # Target variable (traffic volume)

# Split the dataset into training and testing sets (80/20 split)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the data (Standardize features)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Initialize the Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Train the model
model.fit(X_train_scaled, y_train)

# Make predictions
y_pred = model.predict(X_test_scaled)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse:.2f}")
print(f"R-squared: {r2:.2f}")

# Plot the actual vs predicted traffic volume
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, alpha=0.7)
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--')
plt.xlabel('Actual Traffic Volume')
plt.ylabel('Predicted Traffic Volume')
plt.title('Actual vs Predicted Traffic Volume')
plt.show()
