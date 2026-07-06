import os
import subprocess
from pydub import AudioSegment

# --- Configuration ---
INPUT_TEXT_FILE = '../input/novel_prepared_for_audio.txt'  # <-- RENAME THIS TO YOUR FILE
OUTPUT_MP3_FILE = '../output/The-Collected-Short-Stories-Jeffrey-Archer-Audiobook_Final.mp3'
MODEL_PATH = '../model/en_US-amy-medium.onnx'
CONFIG_PATH = '../model/en_US-amy-medium.onnx.json'
MAX_CHARS_PER_CHUNK = 1000  # Split the text for stability and progress
TEMP_WAV_DIR = 'temp_wav_files'

def split_text_into_chunks(text, max_chars):
    """Splits text into chunks of maximum size, respecting paragraphs/sentences."""
    chunks = []
    current_chunk = ""
    for paragraph in text.split('\n'):
        if len(current_chunk) + len(paragraph) + 1 < max_chars:
            current_chunk += paragraph + " "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = paragraph + " "
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def convert_chunk_to_wav(chunk_text, output_wav_path):
    """Calls the piper CLI tool to convert text to a WAV file."""
    try:
        # The 'piper' command-line utility installed by piper-tts package is called here
        command = [
            "piper",
            "--model", MODEL_PATH,
            "--config", CONFIG_PATH,
            "--output_file", output_wav_path,
            "--length_scale", "1.25"  # This makes it 25% slower and more "narrative"
        ]
        
        # Pass the text to piper via standard input
        result = subprocess.run(command, input=chunk_text.encode('utf-8'), check=True, capture_output=True)
        # print(f"Piper Output: {result.stdout.decode().strip()}")
        # print(f"Piper Errors: {result.stderr.decode().strip()}")
        
    except subprocess.CalledProcessError as e:
        print(f"Error during Piper conversion of {output_wav_path}: {e}")
        # Optionally, print the text that failed for debugging: print(chunk_text)
        raise

# --- Main Logic ---
if __name__ == "__main__":
    if not os.path.exists(TEMP_WAV_DIR):
        os.makedirs(TEMP_WAV_DIR)
    
    # 1. Read the cleaned novel text
    print(f"Reading novel from {INPUT_TEXT_FILE}...")
    with open(INPUT_TEXT_FILE, 'r', encoding='utf-8') as f:
        novel_text = f.read()

    # 2. Split into chunks
    text_chunks = split_text_into_chunks(novel_text, MAX_CHARS_PER_CHUNK)
    print(f"Novel split into {len(text_chunks)} segments for processing.")

    # 3. Convert each chunk to a temporary WAV file
    wav_files = []
    for i, chunk in enumerate(text_chunks):
        temp_wav_file = os.path.join(TEMP_WAV_DIR, f"segment_{i:04d}.wav")
        print(f"Converting segment {i+1}/{len(text_chunks)}...")
        try:
            convert_chunk_to_wav(chunk, temp_wav_file)
            wav_files.append(temp_wav_file)
        except Exception as e:
            print(f"FATAL: Skipping segment {i+1} due to error: {e}")
            
    # 4. Concatenate and convert to MP3 using pydub
    print("\n--- Combining segments and converting to MP3 ---")
    combined_audio = AudioSegment.empty()
    
    for wav_file in wav_files:
        try:
            segment = AudioSegment.from_wav(wav_file)
            combined_audio += segment
        except Exception as e:
            print(f"Warning: Could not process {wav_file} for combination. Error: {e}")

    # Export to the final MP3 file
    print(f"Exporting final audiobook to {OUTPUT_MP3_FILE}...")
    combined_audio.export(OUTPUT_MP3_FILE, format="mp3")
    
    # 5. Clean up temporary files
    print("Cleaning up temporary files...")
    for wav_file in wav_files:
        os.remove(wav_file)
    os.rmdir(TEMP_WAV_DIR)

    print(f"\n✅ Audiobook created successfully as {OUTPUT_MP3_FILE}!")
