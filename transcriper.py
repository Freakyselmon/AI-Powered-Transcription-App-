import os
import whisper
from pathlib import Path

def find_media_files(input_folder):
    """Finds all audio and video files in the input folder."""
    media_extensions = {'.mp3', '.wav', '.mp4', '.mkv', '.avi', '.mov'}
    return [os.path.join(root, file) 
            for root, _, files in os.walk(input_folder) 
            for file in files if Path(file).suffix.lower() in media_extensions]

def transcribe_file(model, file_path, output_folder):
    """Transcribes the given media file and saves the text."""
    print(f"Transcribing: {file_path}")
    
    try:
        result = model.transcribe(file_path)
        text_output = result["text"]

        # Save as text file
        file_name = Path(file_path).stem
        text_file_path = os.path.join(output_folder, f"{file_name}.txt")
        
        with open(text_file_path, "w", encoding="utf-8") as text_file:
            text_file.write(text_output)

        print(f"✅ Transcription saved: {text_file_path}")

    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    input_folder = "input_media"
    output_folder = "output_transcriptions"

    os.makedirs(output_folder, exist_ok=True)
    model = whisper.load_model("tiny")  # Change to "base" for better accuracy

    media_files = find_media_files(input_folder)
    if not media_files:
        print("⚠️ No media files found in input_media/")
        return

    for file in media_files:
        transcribe_file(model, file, output_folder)

    print("\n🎉 Transcription completed!")

if __name__ == "__main__":
    main()

#transcriber.py
