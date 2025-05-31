import os
from deep_translator import GoogleTranslator

def split_text(text, max_length=5000):
    """Splits text into chunks of max_length characters without breaking sentences."""
    chunks = []
    while len(text) > max_length:
        split_index = text.rfind("\n", 0, max_length)  # Find last newline before max_length
        if split_index == -1:  # If no newline is found, fallback to space-based split
            split_index = text.rfind(" ", 0, max_length)
        if split_index == -1:  # If no space is found, force split
            split_index = max_length
        chunks.append(text[:split_index])
        text = text[split_index:].lstrip()  # Remove leading spaces and newlines for next chunk
    chunks.append(text)  # Add remaining text
    return chunks

def translate_text(text, dest_language='ur'):
    """Translate text to the specified language (default: Urdu)."""
    return GoogleTranslator(source='auto', target=dest_language).translate(text)

def translate_files_in_folder(input_folder, output_folder, with_timestamp=True):
    """Read all English TXT files from a folder, translate to Urdu, and save them."""
    os.makedirs(output_folder, exist_ok=True)  # Create output folder if it doesn't exist
    
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):  # Process only .txt files
            input_filepath = os.path.join(input_folder, filename)
            if with_timestamp:
                output_filepath = os.path.join(output_folder, filename.replace("English_T.txt", "Urdu_T.txt"))
            else:
                output_filepath = os.path.join(output_folder, filename.replace("English.txt", "Urdu.txt"))

            with open(input_filepath, "r", encoding="utf-8") as file:
                english_text = file.read()

            chunks = split_text(english_text)  # Split text into chunks of max 5000 chars
            translated_chunks = [translate_text(chunk) for chunk in chunks]  # Translate each chunk

            with open(output_filepath, "w", encoding="utf-8") as file:
                file.write("\n".join(translated_chunks))

            print(f"Translated: {filename} → {output_filepath}")

if name == "main":
    drama_name = input("Enter the drama name same as (Directory name): ")
    eng_without_time = f"{drama_name}/English/"
    urdu_without_time = f"{drama_name}/Urdu/"
    eng_with_time = f"{drama_name}/English_T/"
    urdu_with_time = f"{drama_name}/Urdu_T/"
    translate_files_in_folder(eng_without_time, urdu_without_time, with_timestamp=False)
    translate_files_in_folder(eng_with_time, urdu_with_time)