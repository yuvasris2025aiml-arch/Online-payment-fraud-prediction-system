import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pickle

np.random.seed(42)

data = []

# Generate better dataset
for i in range(500):
    amount = np.random.randint(100, 100000)
    oldOrg = np.random.randint(1000, 200000)
    newOrg = oldOrg - amount if oldOrg > amount else 0
    oldDest = np.random.randint(0, 100000)
    newDest = oldDest + amount

    # Fraud logic
    if amount > 50000 or newOrg == 0:
        fraud = 1
    else:
        fraud = 0

    data.append([amount, oldOrg, newOrg, oldDest, newDest, fraud])

df = pd.DataFrame(data, columns=[
    "amount","oldbalanceOrg","newbalanceOrig",
    "oldbalanceDest","newbalanceDest","isFraud"
])

X = df.drop("isFraud", axis=1)
y = df["isFraud"]

scaler = StandardScaler()
X = scaler.fit_transform(X)

model = RandomForestClassifier()
model.fit(X, y)

pickle.dump(model, open("model.pkl","wb"))
pickle.dump(scaler, open("scaler.pkl","wb"))

print("✅ Model trained successfully")