"""
This script transcribes audio files from LICRC sermons
using OpenAI's Whisper model.
"""

import os
import sys
import re
import whisper

# Check for PyTorch
import torch
print("Is CUDA enabled? " + str(torch.cuda.is_available()))
print("Current CUDA GPU: " + str(torch.cuda.get_device_name(0)))

def transcribe_audio(file_path):
    """Transcribes only .mp3 files in the specified directory using Whisper."""
    # Loop through all .mp3 files in file_path directory
    for file in os.listdir(file_path):
        if file.endswith(".mp3"):
            full_path = os.path.join(file_path, file)
            transcribe(full_path)

def transcribe(file_path):
    """Transcribes a single audio file using Whisper
    and saves the output with timestamps."""
    print("Loading model...")
    model = whisper.load_model("turbo")

    print(f"Transcribing: {file_path}")
    result = model.transcribe(file_path, language="en", verbose=True)

    # Create output file name
    base_name = re.sub(r"\s*\[.*?\]", "", os.path.splitext(file_path)[0])
    output_path = f"{base_name}_transcript"

    # Save timestamped + punctuated transcription as .txt
    with open(output_path + ".txt", "w", encoding="utf-8") as f:
        for segment in result["segments"]:
            start = segment["start"]
            end = segment["end"]
            text = segment["text"]
            f.write(f"[{start:.2f} --> {end:.2f}] {text}\n")
    # Save timestamped + punctuated transcription as .md
    with open(output_path + ".md", "w", encoding="utf-8") as f:
        for segment in result["segments"]:
            start = segment["start"]
            end = segment["end"]
            text = segment["text"]
            f.write(f"[{start:.2f} --> {end:.2f}] {text}\n")

    print(f"Transcription saved to: {output_path}.txt and {output_path}.md")

# When script is run, transcribe all audio files in the current directory
if __name__ == "__main__":
    transcribe_audio(sys.argv[1] if len(sys.argv) > 1 else os.getcwd())
