import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
import joblib

# Load the data
data = pd.read_csv('Maternal Health Risk Data Set.csv')

# Check for missing values
print(data.isnull().sum())

# Encode the target variable
le = LabelEncoder()
data['RiskLevel'] = le.fit_transform(data['RiskLevel'])

# Split features and target
X = data.drop('RiskLevel', axis=1)
y = data['RiskLevel']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Random Forest Classifier
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Make predictions
y_pred = rf_model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")
print(classification_report(y_test, y_pred, target_names=le.classes_))

# Save the model and label encoder
joblib.dump(rf_model, 'maternal_health_rf_model.pkl')
joblib.dump(le, 'label_encoder.pkl')