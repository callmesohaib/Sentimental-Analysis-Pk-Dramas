import os
import re
import csv
import yt_dlp
import codecs
from collections import OrderedDict

def fetch_playlist_videos(playlist_url, order="ascending"):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            result = ydl.extract_info(playlist_url, download=False)
            if 'entries' in result:
                videos = [
                    f"https://www.youtube.com/watch?v={entry['id']}" for entry in result['entries']]
                if order.lower() == "descending":
                    videos = videos[::-1]
                return videos
        except Exception as e:
            print(f"❌ Error fetching playlist: {e}")
            return []

def extract_episode_number(dramaname_ep):
    match = re.search(r'Ep(\d+)', dramaname_ep.split('_')[0])
    if match:
        return int(match.group(1))
    return None

def get_matching_english_filename(urdu_filename):
    """Convert Urdu filename to matching English filename"""
    if '_Urdu_T' in urdu_filename:
        return urdu_filename.replace('_Urdu_T', '_English_T')
    return urdu_filename.replace('.txt', '_English_T.txt')

def parse_subtitle_file_with_order(filepath):
    """Parse subtitle file and return ordered list of (timestamp, text)"""
    subtitles = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    if line.startswith('['):
                        timestamp, text = re.match(r'^\[(.*?)\]\s*(.*)', line).groups()
                        subtitles.append((timestamp, text))
                    else:
                        subtitles.append(("-", line))
    except Exception as e:
        print(f"❌ Error reading {filepath}: {e}")
    return subtitles

def generate_final_csv_with_endtime(base_path, drama_playlist_mapping):
    output_csv = os.path.join(base_path, "Dataset_with_Endtime.csv")

    with codecs.open(output_csv, mode='w', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow([
            "Drama_Name",
            "dramaname_Ep_#",
            "Url",
            "timestamp(start-time)",
            "timestamp(end-time)",
            "Sentence_No",
            "Sentence_text",
            "English_Sentence_text",
            "Sentiment(P/N)",
        ])

        for drama_name, info in drama_playlist_mapping.items():
            playlist_url = info["playlist_url"]
            order = info.get("order", "ascending")

            print(f"\n📥 Processing drama: {drama_name}...")
            playlist_videos = fetch_playlist_videos(playlist_url, order)
            if not playlist_videos:
                print(f"⚠️ No videos found for {drama_name}, skipping...")
                continue

            drama_path = os.path.join(base_path, drama_name)
            urdu_folder = os.path.join(drama_path, "Urdu_T")
            english_folder = os.path.join(drama_path, "English_T")

            if not os.path.exists(urdu_folder):
                print(f"⚠️ Urdu folder not found: {urdu_folder}")
                continue
            if not os.path.exists(english_folder):
                print(f"⚠️ English folder not found: {english_folder}")
                continue

            # Process each Urdu file
            for urdu_filename in os.listdir(urdu_folder):
                if not urdu_filename.endswith('.txt'):
                    continue

                print(f"\n📄 Processing file: {urdu_filename}")
                urdu_filepath = os.path.join(urdu_folder, urdu_filename)
                english_filename = get_matching_english_filename(urdu_filename)
                english_filepath = os.path.join(english_folder, english_filename)

                if not os.path.exists(english_filepath):
                    print(f"⚠️ Matching English file not found: {english_filename}")
                    continue

                # Parse both subtitle files with order preserved
                urdu_subtitles = parse_subtitle_file_with_order(urdu_filepath)
                english_subtitles = parse_subtitle_file_with_order(english_filepath)

                if not urdu_subtitles:
                    print(f"⚠️ No subtitles found in Urdu file: {urdu_filename}")
                    continue
                if not english_subtitles:
                    print(f"⚠️ No subtitles found in English file: {english_filename}")
                    continue

                # Get episode info
                episode_name = urdu_filename.split('_')[0].replace('.txt', '')
                episode_number = extract_episode_number(episode_name)
                episode_url = playlist_videos[episode_number-1] if episode_number and episode_number <= len(playlist_videos) else "N/A"

                # Create ordered dictionaries for both subtitle files
                urdu_dict = OrderedDict()
                for timestamp, text in urdu_subtitles:
                    urdu_dict[timestamp] = text
                
                english_dict = OrderedDict()
                for timestamp, text in english_subtitles:
                    english_dict[timestamp] = text

                # Find common timestamps between Urdu and English
                common_timestamps = set(urdu_dict.keys()) & set(english_dict.keys())
                if not common_timestamps:
                    print(f"⚠️ No matching timestamps between {urdu_filename} and {english_filename}")
                    continue

                # Create a list of all timestamps in order (from Urdu file)
                all_timestamps = []
                for timestamp, _ in urdu_subtitles:
                    if timestamp in common_timestamps and timestamp not in all_timestamps:
                        all_timestamps.append(timestamp)

                # Write matched subtitles to CSV with end times
                sentence_no = 1
                for i, timestamp in enumerate(all_timestamps):
                    # Get end time (next timestamp or empty if last one)
                    end_time = all_timestamps[i+1] if i+1 < len(all_timestamps) else ""
                    
                    writer.writerow([
                        drama_name,
                        episode_name,
                        episode_url,
                        timestamp,
                        end_time,
                        sentence_no,
                        urdu_dict[timestamp],
                        english_dict[timestamp],
                        "",  # Sentiment column
                    ])
                    sentence_no += 1

                print(f"✅ Processed {sentence_no-1} subtitle pairs from {urdu_filename}")

    print("\n🎯 Dataset_with_Endtime.csv generated successfully!")

# Your existing configuration
base_path = r"A:\University\BSCS 6th sem\NLP\NLP"
drama_playlist_mapping = {
    "Bandhay Ek Dour Se": {
        "playlist_url": "https://www.youtube.com/playlist?list=PLdZNFVCDo_1cbdDt_gKKokphFdbdpkwJW",
        "order": "descending"
    },
    "Ehsaan Faramosh": {
        "playlist_url": "https://www.youtube.com/playlist?list=PLb2aaNHUy_gFHGL6l6g-yssJmyh93CFe_",
        "order": "descending"
    },
    "Hasrat": {
        "playlist_url": "https://www.youtube.com/playlist?list=PLb2aaNHUy_gHh-l7X_6Ewv_uphydZI6Ro",
        "order": "descending"
    },
    "Mann Aangan": {
        "playlist_url": "https://www.youtube.com/playlist?list=PLb2aaNHUy_gH2x-QifStEqeEIPPK1-sRg",
        "order": "descending"
    },
    "Mann Jogi": {
        "playlist_url": "https://www.youtube.com/playlist?list=PLbVdwtmx18suEeQtGU39w3zjw7eZpbOiZ",
        "order": "descending"
    },
    "Muqaddar Ka Sitara": {
        "playlist_url": "https://www.youtube.com/playlist?list=PLb2aaNHUy_gF38YorYXdoAbdSh_25YDwp",
        "order": "descending"
    },
    "Romeo Juliet": {
        "playlist_url": "https://www.youtube.com/playlist?list=PLb2aaNHUy_gFJ6D8UGRJPLmshruKzGUyX",
        "order": "ascending"
    },
    "Tere Aany Se": {
        "playlist_url": "https://www.youtube.com/playlist?list=PLdZNFVCDo_1dTPH-rYiRFlGIE7A24n_mQ",
        "order": "ascending"
    },
    "Tere Ishq Ke Naam": {
        "playlist_url": "https://www.youtube.com/playlist?list=PLb2aaNHUy_gEsfFu1bR8x60-nrXRX-65Y",
        "order": "descending"
    },
    "Tum Bin Kesay Jiyen": {
        "playlist_url": "https://www.youtube.com/playlist?list=PLb2aaNHUy_gFAWdsB89jKYJ-CCL31Is6X",
        "order": "descending"
    },
    "Tum ho Waja": {
        "playlist_url": "https://www.youtube.com/playlist?list=PLbVdwtmx18stk0BcnMK_OLle3YdFzU5gl",
        "order": "ascending"
    }
}

generate_final_csv_with_endtime(base_path, drama_playlist_mapping)