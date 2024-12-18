# -*- coding: utf-8 -*-
"""Heart Disease_Analysis

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1lZs8qJKphZ2HJGAq4ohh9wR6m5kDGMTy
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

df_uci = pd.read_csv('Heart_Disease_UCI.csv')
df_uci.head()

df_uci.shape

df_uci.info()

df_uci.isnull().sum()

# Summary statistics
summary_stats = df_uci.describe() # Changed 'data' to 'df_uci'
print(summary_stats)

# Distribution of features
import matplotlib.pyplot as plt
import seaborn as sns

# Plot histograms for numerical columns
df_uci.hist(bins=15, figsize=(15, 10)) # Changed 'data' to 'df_uci'
plt.show()

"""# **Calculating number of missing values**"""

# Calculate the number of missing values in each column
missing_values = df_uci.isnull().sum()

# Plotting the missing values
plt.figure(figsize=(12, 6))
missing_values.plot(kind='bar', color='blue')
plt.title('Number of Missing Values in Each Column')
plt.xlabel('Columns')
plt.ylabel('Number of Missing Values')
plt.xticks(rotation=45)
plt.show()

"""# **Missing Values Count by Feature:**

    1. trestbps (Resting Blood Pressure): **59** missing values.
    2. chol (Serum Cholesterol): **30** missing values.
    3. fbs (Fasting Blood Sugar): **90** missing values.
    4. restecg (Resting Electrocardiographic Results): **2** missing values.
    5. thalch (Maximum Heart Rate Achieved): **55** missing values.
    6. exang (Exercise Induced Angina): **55** missing values.
    7. oldpeak (ST Depression Induced by Exercise Relative to Rest): **62** missing values.
    8. slope (Slope of the Peak Exercise ST Segment): **309** missing values.
    9. ca (Number of Major Vessels Colored by Fluoroscopy): **611** missing values.
    10. thal (Thalassemia): **486** missing values.

    Impact of Missing Values: Missing values can affect the analysis and modeling process
    by introducing bias and reducing the effectiveness of predictive models. It's important to handle them appropriately
    to avoid misleading results.

# **Handling Missing values with categorical and numerical columns**
"""

# Identify categorical and numerical columns
categorical_cols = df_uci.select_dtypes(include=['object', 'category']).columns
categorical_cols

numerical_cols = df_uci.select_dtypes(include=['number']).columns
numerical_cols

# Fill missing values in numerical columns with the mean
df_uci[numerical_cols] = df_uci[numerical_cols].fillna(df_uci[numerical_cols].mean())

# Fill missing values in categorical columns with the mode
for col in categorical_cols:
    df_uci[col] = df_uci[col].fillna(df_uci[col].mode()[0])

# Verify if there are any remaining missing values
print(df_uci.isnull().sum())

"""# **Calculating number of missing values after handling**"""

# Plotting the missing values (if any remain)
plt.figure(figsize=(10, 5))
df_uci.isnull().sum().plot(kind='bar', color='skyblue')
plt.title('Number of Missing Values in Each Column')
plt.xlabel('Columns')
plt.ylabel('Number of Missing Values')
plt.xticks(rotation=45)
plt.show()

"""# **Handling Outlier with box plot**"""

# Create a box plot for numerical columns
import warnings
warnings.filterwarnings("ignore")
plt.figure(figsize=(8, 7))
sns.boxplot(data=df_uci[numerical_cols])
plt.xticks(rotation=90)  # Rotate x-axis labels for better readability
plt.title('Box Plot for Numerical Columns')
plt.show()

"""# **Removing outlier in chol and trestbps columns with IQR**
The interquartile range (IQR) is a measure of statistical dispersion, which is the spread of the data.  It is defined as the difference between the 75th and 25th percentiles of the data.
"""

# Define a function to remove outliers using IQR
def remove_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

# Remove outliers from 'chol' and 'trestbps'
df_uci_cleaned = remove_outliers(df_uci, 'chol')
df_uci_cleaned = remove_outliers(df_uci_cleaned, 'trestbps')

# Plotting the cleaned data to visualize the absence of outliers
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
sns.boxplot(data=df_uci_cleaned, x='chol')
plt.title('Box Plot of Chol (Cleaned)')

plt.subplot(1, 2, 2)
sns.boxplot(data=df_uci_cleaned, x='trestbps')
plt.title('Box Plot of Trestbps (Cleaned)')

plt.tight_layout()
plt.show()

"""# **Histogram plot for numeric columns with sex column**"""

# Plot histograms for numeric columns with sex column
num_numeric_cols = df_uci.select_dtypes(include=['number']).shape[1]
num_cols_per_row = 2
num_rows = (num_numeric_cols + num_cols_per_row - 1) // num_cols_per_row

plt.figure(figsize=(12, 8))

for i, col in enumerate(df_uci.select_dtypes(include=['number'])):
    plt.subplot(num_rows, num_cols_per_row, i+1)
    sns.histplot(data=df_uci, x=col, hue='sex', kde=True, bins=20)
    plt.title(f'Histogram of {col} by Sex')
    plt.xlabel(col)
    plt.ylabel('Frequency')

plt.tight_layout()
plt.show()

"""# **Sex Distribution**"""

plt.figure(figsize=(8,6))
ax = sns.countplot(x='sex',data=df_uci)
plt.title('Sex Distribution')

for p in ax.patches:
    ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points')

plt.show()

df_uci['sex'].value_counts()

"""# **Age and Heart Disease Diagnosis Distribution by Sex and Dataset**"""

import plotly.express as px

fig = px.sunburst(df_uci,
                  path=['sex','dataset'],
                  values='age',
                  color='num',
                  title='Age and Heart Disease Diagnosis Distribution by Sex and Dataset')
fig.show()

"""# **Correlation Matrix**"""

# Correlation matrix
correlation_matrix = df_uci.select_dtypes(include=['number']).corr() # Select only numerical columns for correlation

# Heatmap of correlations
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.show()

"""**Insights:**
*   Features like oldpeak, ca, and thalch seem to be strong indicators for predicting heart disease.
*   Age and maximum heart rate are important to consider, as older patients with lower heart rates appear more likely to develop heart disease.
*   Surprisingly, cholesterol (chol) has a weak correlation, suggesting it may not be as strong a predictor in this specific dataset.

# **Heart Disease Class Distribution**
"""

# Count the number of occurrences for each class in 'num'
target_dist = df_uci['num'].value_counts() # Changed data to df_uci

# Bar plot to visualize class imbalance
sns.countplot(x='num', data=df_uci) # Changed data to df_uci
plt.title('Heart Disease Class Distribution')
plt.show()

"""# **Feature Importance Analysis**"""

# Bar plot for categorical features like 'sex', 'cp', and 'fbs'
categorical_columns = ['sex', 'cp', 'fbs', 'restecg', 'exang', 'thal']

for col in categorical_columns:
    plt.figure(figsize=(6, 4))
    sns.countplot(x=col, hue='num', data=df_uci) # Changed data to df_uci
    plt.title(f'{col} vs Heart Disease')
    plt.show()

# Box plots for numerical columns like 'age', 'chol', 'thalch', 'trestbps', and 'oldpeak'
numerical_columns = ['age', 'chol', 'trestbps', 'thalch', 'oldpeak']

for col in numerical_columns:
    plt.figure(figsize=(6, 4))
    sns.boxplot(x='num', y=col, data=df_uci) # Changed data to df_uci
    plt.title(f'{col} vs Heart Disease')
    plt.show()

"""# **Outliner detection**"""

# Box plots to detect outliers for numerical columns
for col in numerical_columns:
    plt.figure(figsize=(6, 4))
    sns.boxplot(df_uci[col]) # Changed data to df_uci
    plt.title(f'Outlier Detection for {col}')
    plt.show()

# Z-score method to remove outliers
from scipy import stats

z_scores = stats.zscore(df_uci[numerical_columns]) # Changed data to df_uci
abs_z_scores = np.abs(z_scores)
filtered_entries = (abs_z_scores < 3).all(axis=1)
cleaned_data = df_uci[filtered_entries] # Changed data to df_uci

"""# **Chest Pain Analysis (cp)**"""

# Cross-tabulation between chest pain type and heart disease
cp_num_crosstab = pd.crosstab(df_uci['cp'], df_uci['num']) # Changed data to df_uci
print(cp_num_crosstab)

# Visualize chest pain distribution for heart disease classes
sns.countplot(x='cp', hue='num', data=df_uci) # Changed data to df_uci
plt.title('Chest Pain Type vs Heart Disease')
plt.show()

"""# **Exercise-Induced Angina (exang)**"""

# Bar plot to visualize relationship between 'exang' and 'num'
sns.countplot(x='exang', hue='num', data=df_uci) # Changed data to df_uci
plt.title('Exercise-Induced Angina vs Heart Disease')
plt.show()

"""# **Maximum Heart Rate (thalch)**"""

# Box plot to visualize 'thalch' across different heart disease classes
sns.boxplot(x='num', y='thalch', data=df_uci) # Changed data to df_uci
plt.title('Maximum Heart Rate Achieved (thalch) vs Heart Disease')
plt.show()

"""# **ST Depression (oldpeak)**"""

# Box plot to visualize 'oldpeak' across different heart disease classes
sns.boxplot(x='num', y='oldpeak', data=df_uci) # Changed data to df_uci
plt.title('ST Depression (oldpeak) vs Heart Disease')
plt.show()

"""# **Surgical or Clinical Indicators (ca and thal)**"""

# Bar plots for 'ca' and 'thal' against 'num'
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
sns.countplot(x='ca', hue='num', data=df_uci) # Changed data to df_uci
plt.title('Number of Major Vessels (ca) vs Heart Disease')

plt.subplot(1, 2, 2)
sns.countplot(x='thal', hue='num', data=df_uci) # Changed data to df_uci
plt.title('Thalassemia (thal) vs Heart Disease')

plt.tight_layout()
plt.show()

"""# **Risk Factor Analysis**"""

# Comparing risk factors like 'chol', 'trestbps', 'fbs' with heart disease
risk_factors = ['chol', 'trestbps', 'fbs']

for factor in risk_factors:
    plt.figure(figsize=(6, 4))
    sns.boxplot(x='num', y=factor, data=df_uci) # Changed data to df_uci
    plt.title(f'{factor} vs Heart Disease')
    plt.show()

"""# **Multivariate Analysis**"""

# Pair plots for multivariate analysis
sns.pairplot(df_uci, hue='num', vars=['age', 'chol', 'trestbps', 'thalch', 'oldpeak']) # Changed data to df_uci
plt.show()

"""# **Distribution of Predicted Attribute (num) by Region(Dataset)**"""

plt.figure(figsize=(8,6))
sns.barplot(x='dataset',y='num',data=df_uci)
plt.title('Distribution of Predicted Attribute (num) by Region(Dataset)')
plt.show()

"""# **Scatter Plot: Age vs Cholesterol (colored by sex, sized by trestbps)**"""

# Create a scatter plot
fig1 = px.scatter(df_uci, x='age', y='chol', color='sex', size='trestbps', hover_data=['cp', 'dataset'])

# Update layout with title
fig1.update_layout(title='Scatter Plot: Age vs Cholesterol (colored by sex, sized by trestbps)')

# Show the plot
fig1.show()

"""# **Distribution of Predicted Attribute (num) by Region(Dataset)**"""

plt.figure(figsize=(8,6))
sns.countplot(x='dataset',hue='num',data=df_uci)
plt.title('Distribution of Predicted Attribute (num) by Region(Dataset)')
plt.show()

"""# **Distribution of Thalassemia Present (thal) by Region(Dataset)**"""

plt.figure(figsize=(8, 6))
sns.countplot(x='thal', hue='dataset', data=df_uci)
plt.title('Distribution of Thalassemia Present (thal) by Dataset')
plt.show()

# Group by 'thal' and 'dataset' columns and count occurrences
grouped_counts = df_uci.groupby(['thal', 'dataset']).size()

print("Grouped counts by 'thal' and 'dataset':")
print(grouped_counts)

"""# **Distribution of age Present (age) by sex**"""

plt.figure(figsize=(8, 6))
sns.countplot(x='age', hue='sex', data=df_uci)
plt.title('Distribution of age Present (age) by sex')
plt.show()

"""# **Distribution of chest pain type Present (cp) by num**"""

plt.figure(figsize=(8, 6))
sns.countplot(x='cp', hue='num', data=df_uci)
plt.title('Distribution of chest pain type Present (cp) by num')
plt.show()

# Group by 'thal' and 'dataset' columns and count occurrences
grouped_counts = df_uci.groupby(['cp', 'num']).size()

print("Grouped counts by 'cp' and 'num':")
print(grouped_counts)

"""# **Distribution of resting blood pressure Present (trestbps) by age**"""

plt.figure(figsize=(8, 6))
sns.countplot(x='trestbps', hue='age', data=df_uci)
plt.title('Distribution of resting blood pressure Present (trestbps) by age')
plt.show()

# Group by 'thal' and 'dataset' columns and count occurrences
grouped_counts = df_uci.groupby(['trestbps', 'age']).size()

print("Grouped counts by 'trestbps' and 'age':")
print(grouped_counts)

df_uci.head()

# Convert 'sex': Male -> 1, Female -> 0
df_uci['sex'] = df_uci['sex'].replace({'Male': 1, 'Female': 0})

# Convert 'cp' (chest pain types): typical angina -> 3, atypical angina -> 2, non-anginal -> 1, asymptomatic -> 0
df_uci['cp'] = df_uci['cp'].replace({
    'typical angina': 3,
    'atypical angina': 2,
    'non-anginal': 1,
    'asymptomatic': 0
})

# Convert 'fbs' (fasting blood sugar): True -> 1, False -> 0
df_uci['fbs'] = df_uci['fbs'].astype(int)

# Convert 'restecg': lv hypertrophy -> 2, normal -> 0, st-t abnormality -> 1
df_uci['restecg'] = df_uci['restecg'].replace({
    'normal': 0,
    'st-t abnormality': 1,
    'lv hypertrophy': 2
})

# Convert 'exang' (exercise-induced angina): True -> 1, False -> 0
df_uci['exang'] = df_uci['exang'].astype(int)

# Convert 'slope' (slope of the peak exercise ST segment): downsloping -> 0, flat -> 1, upsloping -> 2
df_uci['slope'] = df_uci['slope'].replace({
    'downsloping': 0,
    'flat': 1,
    'upsloping': 2
})

# Convert 'thal': fixed defect -> 2, normal -> 0, reversable defect -> 1
df_uci['thal'] = df_uci['thal'].replace({
    'normal': 0,
    'reversable defect': 1,
    'fixed defect': 2
})

df_uci.head()

X=df_uci.drop(['dataset'],axis=1)
y=df_uci['num']

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.preprocessing import StandardScaler

# Initialize a dictionary to store evaluation metrics for each algorithm
evaluation_metrics = {}

# Initialize a StandardScaler object and fit to training data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

from sklearn.linear_model import LogisticRegression

# Create a logistic regression model
log_model = LogisticRegression(max_iter=1000)
log_model.fit(X_train, y_train)

# Make predictions
y_pred_log = log_model.predict(X_test)

# Calculate metrics
accuracy_log = accuracy_score(y_test, y_pred_log)
precision_log = precision_score(y_test, y_pred_log, average='weighted')
recall_log = recall_score(y_test, y_pred_log, average='weighted')
f1_log = f1_score(y_test, y_pred_log, average='weighted')

print(f'Logistic Regression: Accuracy: {accuracy_log}, Precision: {precision_log}, Recall: {recall_log}, F1-Score: {f1_log}')

gbc_model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, min_samples_split=2, min_samples_leaf=1, subsample=1.0)
gbc_model.fit(X_train_scaled, y_train)
gbc_predictions = gbc_model.predict(X_test_scaled)
gbc_proba = gbc_model.predict_proba(X_test_scaled)

# Initialize a dictionary to store the Gini coefficients for each class
gini_coefficients = {}

# Calculate the Gini coefficient for each class
for class_label in range(gbc_proba.shape[1]):
    class_proba = gbc_proba[:, class_label]
    gini_coefficients[f'Class {class_label}'] = roc_auc_score((y_test == class_label).astype(int), class_proba) * 2 - 1

# Average the Gini coefficients across all classes
average_gini_coefficient = np.mean(list(gini_coefficients.values()))

# Compute other evaluation metrics
conf_matrix = confusion_matrix(y_test, rfc_predictions)
accuracy = accuracy_score(y_test, rfc_predictions)
precision = precision_score(y_test, gbc_predictions, average='weighted')
recall = recall_score(y_test, gbc_predictions, average='weighted')
f1 = f1_score(y_test, gbc_predictions, average='weighted')

# Store evaluation metrics in a dictionary
gbc_metrics = {
    'Confusion Matrix': conf_matrix,
    'Accuracy': accuracy,
    'Precision': precision,
    'Recall': recall,
    'F1 Score': f1,
    'Gini Coefficients': gini_coefficients,
    'Average Gini Coefficient': average_gini_coefficient
}

# Store metrics in the evaluation dictionary
evaluation_metrics['GradientBoostingClassifier'] = gbc_metrics

# Print evaluation metrics
print("Evaluation Metrics for Gradient Boosting Classifier:")
for metric_name, metric_value in gbc_metrics.items():
    print(f"{metric_name}: {metric_value}")

from sklearn.ensemble import RandomForestClassifier

rfc_model = RandomForestClassifier(n_estimators=100)
rfc_model.fit(X_train_scaled, y_train)
rfc_predictions = rfc_model.predict(X_test_scaled)
rfc_proba = rfc_model.predict_proba(X_test_scaled)

gini_coefficients = {}
for class_label in range(rfc_proba.shape[1]):
    class_proba = rfc_proba[:, class_label]
    gini_coefficients[f'Class {class_label}'] = roc_auc_score((y_test == class_label).astype(int), class_proba) * 2 - 1
average_gini_coefficient = np.mean(list(gini_coefficients.values()))

conf_matrix = confusion_matrix(y_test, rfc_predictions)
accuracy = accuracy_score(y_test, rfc_predictions)
precision = precision_score(y_test, rfc_predictions, average='weighted')
recall = recall_score(y_test, rfc_predictions, average='weighted')
f1 = f1_score(y_test, rfc_predictions, average='weighted')

rfc_metrics = {
    'Confusion Matrix': conf_matrix,
    'Accuracy': accuracy,
    'Precision': precision,
    'Recall': recall,
    'F1 Score': f1,
    'Gini Coefficients': gini_coefficients,
    'Average Gini Coefficient': average_gini_coefficient
}

evaluation_metrics['RandomForestClassifier'] = rfc_metrics

print("Evaluation Metrics for Random Forest Classifier:")
for metric_name, metric_value in rfc_metrics.items():
    print(f"{metric_name}: {metric_value}")

from sklearn.svm import SVC

svc_model = SVC(probability=True)
svc_model.fit(X_train_scaled, y_train)
svc_predictions = svc_model.predict(X_test_scaled)
svc_proba = svc_model.predict_proba(X_test_scaled)

gini_coefficients = {}
for class_label in range(svc_proba.shape[1]):
    class_proba = svc_proba[:, class_label]
    gini_coefficients[f'Class {class_label}'] = roc_auc_score((y_test == class_label).astype(int), class_proba) * 2 - 1

average_gini_coefficient = np.mean(list(gini_coefficients.values()))

conf_matrix = confusion_matrix(y_test, svc_predictions)
accuracy = accuracy_score(y_test, svc_predictions)
precision = precision_score(y_test, svc_predictions, average='weighted')
recall = recall_score(y_test, svc_predictions, average='weighted')
f1 = f1_score(y_test, svc_predictions, average='weighted')

svc_metrics = {
    'Confusion Matrix': conf_matrix,
    'Accuracy': accuracy,
    'Precision': precision,
    'Recall': recall,
    'F1 Score': f1,
    'Gini Coefficients': gini_coefficients,
    'Average Gini Coefficient': average_gini_coefficient
}

evaluation_metrics['SVC'] = svc_metrics
print("Evaluation Metrics for SVM:")
for metric_name, metric_value in svc_metrics.items():
    print(f"{metric_name}: {metric_value}")

import matplotlib.pyplot as plt

# Accuracy scores for each model
accuracy_scores = [accuracy_log, evaluation_metrics['GradientBoostingClassifier']['Accuracy'], evaluation_metrics['RandomForestClassifier']['Accuracy'], evaluation_metrics['SVC']['Accuracy']]

# Model names
model_names = ['Logistic Regression', 'Gradient Boosting', 'Random Forest', 'SVM']

# Create the bar chart
plt.figure(figsize=(10, 6))
bars = plt.bar(model_names, accuracy_scores, color=['blue', 'green', 'orange', 'red'])
plt.xlabel('Model')
plt.ylabel('Accuracy Score')
plt.title('Accuracy Comparison of Different Models')
plt.ylim(0.9, 1.0)  # Adjust y-axis limits for better visualization if accuracy is between 0.9 and 1.0

# Add percentages above the bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.005, f'{round(yval * 100, 2)}%', ha='center', va='bottom')

# Show the plot
plt.tight_layout()
plt.show()

# Model names
model_names = ['Logistic Regression', 'Gradient Boosting', 'Random Forest', 'SVM']

# Metrics for each model
accuracy = [accuracy_log, evaluation_metrics['GradientBoostingClassifier']['Accuracy'], evaluation_metrics['RandomForestClassifier']['Accuracy'], evaluation_metrics['SVC']['Accuracy']]
precision = [precision_log, evaluation_metrics['GradientBoostingClassifier']['Precision'], evaluation_metrics['RandomForestClassifier']['Precision'], evaluation_metrics['SVC']['Precision']]
recall = [recall_log, evaluation_metrics['GradientBoostingClassifier']['Recall'], evaluation_metrics['RandomForestClassifier']['Recall'], evaluation_metrics['SVC']['Recall']]
f1 = [f1_log, evaluation_metrics['GradientBoostingClassifier']['F1 Score'], evaluation_metrics['RandomForestClassifier']['F1 Score'], evaluation_metrics['SVC']['F1 Score']]

# Set the width of the bars
bar_width = 0.2

# Set position of bar on X axis
r1 = np.arange(len(accuracy))
r2 = [x + bar_width for x in r1]
r3 = [x + bar_width for x in r2]
r4 = [x + bar_width for x in r3]

# Make the plot
plt.figure(figsize=(12, 8))
plt.bar(r1, accuracy, color='#7f6d5f', width=bar_width, edgecolor='white', label='Accuracy')
plt.bar(r2, precision, color='#557f2d', width=bar_width, edgecolor='white', label='Precision')
plt.bar(r3, recall, color='#2d7f5e', width=bar_width, edgecolor='white', label='Recall')
plt.bar(r4, f1, color='#5a3c80', width=bar_width, edgecolor='white', label='F1-Score')

# Add xticks on the middle of the group bars
plt.xlabel('Model', fontweight='bold')
plt.xticks([r + bar_width for r in range(len(accuracy))], model_names)

# Set y-axis limits
plt.ylim(0.9, 1.0)

# Create legend & Show graphic
plt.legend()
plt.title('Model Performance Comparison')
plt.show()