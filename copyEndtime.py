import pandas as pd
import os

def add_endtimes_from_reference_mixed_formats(original_excel, reference_csv, output_excel):
    """
    Copy end times from reference CSV file to original Excel file by matching on dramaname_Ep_# and Sentence_No,
    while preserving all original columns including start times.
    
    Args:
        original_excel: Path to Excel file without end times (.xlsx)
        reference_csv: Path to CSV file with end times (.csv)
        output_excel: Path to save the merged Excel file (.xlsx)
    """
    # Read both files
    df_original = pd.read_excel(original_excel)
    df_reference = pd.read_csv(reference_csv)
    
    # Strip whitespace from column names
    df_original.columns = df_original.columns.str.strip()
    df_reference.columns = df_reference.columns.str.strip()
    
    # Print columns for debugging
    print("Original Excel columns:", df_original.columns.tolist())
    print("Reference CSV columns:", df_reference.columns.tolist())
    
    # Make sure we have the required columns
    required_cols = ['Drama_Name', 'dramaname_Ep_#', 'Sentence_No']
    for col in required_cols:
        if col not in df_original.columns:
            raise ValueError(f"Original Excel file missing required column: {col}")
        if col not in df_reference.columns:
            raise ValueError(f"Reference CSV file missing required column: {col}")
    
    if 'timestamp(end-time)' not in df_reference.columns:
        raise ValueError("Reference CSV file missing 'timestamp(end-time)' column")
    
    # Create a mapping dictionary from the reference file
    endtime_map = {}
    for _, row in df_reference.iterrows():
        key = (row['dramaname_Ep_#'], row['Sentence_No'])
        endtime_map[key] = row['timestamp(end-time)']
    
    # Create a copy of the original dataframe to preserve all existing columns
    df_output = df_original.copy()
    
    # Add end times to the output dataframe without affecting other columns
    df_output['timestamp(end-time)'] = df_output.apply(
        lambda row: endtime_map.get((row['dramaname_Ep_#'], row['Sentence_No']), None),
        axis=1
    )
    
    # Save the merged file as Excel
    df_output.to_excel(output_excel, index=False)
    print(f"✅ Successfully saved merged Excel file with end times to {output_excel}")

# Example usage:
base_path = r"A:\University\BSCS 6th sem\NLP\NLP"
original_excel = os.path.join(base_path, "Labeled_Dataset.xlsx")
reference_csv = os.path.join(base_path, "Dataset_with_Endtime.csv")
output_excel = os.path.join(base_path, "Dataset_Final.xlsx")

add_endtimes_from_reference_mixed_formats(original_excel, reference_csv, output_excel)