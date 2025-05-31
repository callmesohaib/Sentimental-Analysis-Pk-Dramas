import os
from pytube import Playlist
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

def get_video_ids(playlist_url):
    """Extract video titles and IDs from the YouTube playlist URL."""
    playlist = Playlist(playlist_url)
    return [video.video_id for video in playlist.videos]

def format_time(seconds):
    """Convert seconds to [mm:ss] format."""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02}:{seconds:02}"

def get_transcript(video_id, with_timestamp=True):
    """Fetch manual transcript with or without timestamps."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        if with_timestamp:
            return "\n".join([f"[{format_time(t['start'])}] {t['text']}" for t in transcript])
        else:
            return "\n".join([t['text'] for t in transcript])
        
    except (TranscriptsDisabled, NoTranscriptFound):
        return None  # Manual transcript not available
    except Exception as e:
        return f"Error fetching transcript: {str(e)}"

def save_transcripts(playlist_url, drama_name, no_of_eps):
    """Download and save transcripts for all videos in the playlist."""
    video_data = get_video_ids(playlist_url)

    # Create folders
    timestamp_folder = f"{drama_name}/English_T/"
    no_timestamp_folder = f"{drama_name}/English/"
    os.makedirs(timestamp_folder, exist_ok=True)
    os.makedirs(no_timestamp_folder, exist_ok=True)

    episode_number = no_of_eps + 1
    for video_id in video_data:
        episode_number -= 1

        timestamp_filename = os.path.join(timestamp_folder, f"{drama_name}Ep{episode_number}_English_T.txt")
        no_timestamp_filename = os.path.join(no_timestamp_folder, f"{drama_name}Ep{episode_number}_English.txt")

        # Try fetching manual transcript
        transcript_with_time = get_transcript(video_id, with_timestamp=True)
        transcript_without_time = get_transcript(video_id, with_timestamp=False)

        if transcript_with_time and transcript_without_time:
            # Save manual transcript (with timestamps)
            with open(timestamp_filename, "w", encoding="utf-8") as f:
                f.write(transcript_with_time)
            print(f"Manual transcript (with timestamps) saved: {timestamp_filename}")

            # Save manual transcript (without timestamps)
            with open(no_timestamp_filename, "w", encoding="utf-8") as f:
                f.write(transcript_without_time)
            print(f"Manual transcript (without timestamps) saved: {no_timestamp_filename}")
        
        else:
            print(f"Manual transcript not available...")
            continue

if name == "main":
    drama_name = input("Enter the drama name: ")
    no_of_eps = int(input("Enter the number of episodes: "))
    playlist_url = input("Enter YouTube Playlist URL: ")
    save_transcripts(playlist_url, drama_name, no_of_eps)