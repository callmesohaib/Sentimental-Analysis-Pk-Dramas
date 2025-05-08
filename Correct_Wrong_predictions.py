import pandas as pd

# Load the Excel file
df = pd.read_excel("urdu_predictions_with_actual_predicated.xlsx")

# Optional: Strip whitespace from columns just in case
df.columns = df.columns.str.strip()

# Ensure consistency in values (strip and upper/lower if needed)
df['Actual Sentiment'] = df['Actual Sentiment'].astype(str).str.strip()
df['Predicted Sentiment'] = df['Predicted Sentiment'].astype(str).str.strip()

# Correct predictions
correct_preds = df[df['Actual Sentiment'] == df['Predicted Sentiment']].sample(10, random_state=1)

# Incorrect predictions
incorrect_preds = df[df['Actual Sentiment'] != df['Predicted Sentiment']].sample(10, random_state=1)

# Save or display them
print("✅ Correct Predictions:\n", correct_preds)
print("\n❌ Incorrect Predictions:\n", incorrect_preds)

# # Optionally save to new Excel sheets
# with pd.ExcelWriter("urdu_predictions_samples.xlsx") as writer:
#     correct_preds.to_excel(writer, sheet_name="Correct", index=False)
#     incorrect_preds.to_excel(writer, sheet_name="Incorrect", index=False)
