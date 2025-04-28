import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler

# Load Dataset
data_path = '/Users/salma.abbady/Documents/GitHub/Oil-Price-Predictor/data/processed/brent_with_all_macros.csv'
df = pd.read_csv(data_path)

# 1. Basic EDA

print("Dataset Shape:", df.shape)
print("\nMissing Values:\n", df.isnull().sum())

# Drop rows where Crude_Stocks is NaN (since it's important)
df.dropna(subset=['Crude_Stocks'], inplace=True)
print("\nAfter dropping NaNs in Crude_Stocks:", df.shape)

print("\nSummary Statistics:\n", df.describe())

# 2. Correlation Heatmap
plt.figure(figsize=(15,10))
corr = df.select_dtypes(include=['float64', 'int64']).corr()
sns.heatmap(corr[['Price']].sort_values(by='Price', ascending=False), annot=True, cmap='coolwarm')
plt.title('Correlation of Features with Brent Price')
plt.show()

# 3. Time Series Plots
df['Date'] = pd.to_datetime(df['Date'])

# Plot Brent Price & Crude Stocks
fig, ax1 = plt.subplots(figsize=(14,6))

ax1.set_xlabel('Date')
ax1.set_ylabel('Brent Price', color='tab:blue')
ax1.plot(df['Date'], df['Price'], color='tab:blue', label='Brent Price')
ax1.tick_params(axis='y', labelcolor='tab:blue')

ax2 = ax1.twinx()
ax2.set_ylabel('Crude Stocks', color='tab:red')
ax2.plot(df['Date'], df['Crude_Stocks'], color='tab:red', alpha=0.5, label='Crude Stocks')
ax2.tick_params(axis='y', labelcolor='tab:red')

plt.title('Brent Price vs Crude Oil Stocks Over Time')
fig.tight_layout()
plt.show()

# 4. Feature Selection
df_model = df.drop(columns=['Date'])

target = 'Price'
features = [col for col in df_model.columns if col != target]

print("\nFeatures Selected:", features)

# 5. Feature Scaling
scaler = MinMaxScaler()
df_scaled = pd.DataFrame(scaler.fit_transform(df_model[features]), columns=features)

# Add back the target (unscaled)
df_scaled[target] = df_model[target].values

print("\nFeature scaling complete. Scaled dataset shape:", df_scaled.shape)

# 6. Save Scaled Dataset
output_path = '/Users/salma.abbady/Documents/GitHub/Oil-Price-Predictor/data/processed/brent_scaled_for_modeling.csv'
df_scaled.to_csv(output_path, index=False)
print(f"\nScaled dataset saved to: {output_path}")
