import os
import json
import subprocess
import re
import shutil

# --- CONFIGURATION ---
INPUT_FILE = "novel.txt"
OUTPUT_FOLDER = "audiobook_output"
TEMP_FOLDER = "temp_chunks"
STATE_FILE = "state.json"
PIPER_EXE = "./piper"  # Path to your piper executable
PIPER_MODEL = "en_US-lessac-medium.onnx"
CHUNK_SIZE = 2000  # Characters per chunk (adjust as needed)

def clean_text(text):
    """Basic cleaning to remove excessive whitespace."""
    return re.sub(r'\s+', ' ', text).strip()

def split_into_chunks(text, size):
    """Splits text into chunks of roughly 'size' characters."""
    words = text.split(' ')
    chunks = []
    current_chunk = []
    current_length = 0
    
    for word in words:
        current_chunk.append(word)
        current_length += len(word) + 1
        if current_length >= size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"last_completed_chunk": -1, "total_chunks": 0}

def save_state(index, total):
    with open(STATE_FILE, 'w') as f:
        json.dump({"last_completed_chunk": index, "total_chunks": total}, f)

def run_piper(text, output_wav):
    """Calls Piper TTS via subprocess."""
    command = [
        PIPER_EXE,
        "--model", PIPER_MODEL,
        "--output_file", output_wav
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    process.communicate(input=text.encode('utf-8'))

def convert_to_mp3(input_wav, output_mp3):
    """Converts WAV to MP3 using ffmpeg."""
    subprocess.run([
        'ffmpeg', '-y', '-i', input_wav, 
        '-codec:a', 'libmp3lame', '-qscale:a', '2', 
        output_mp3
    ], check=True, capture_output=True)

def main():
    # 1. Setup Folders
    os.makedirs(TEMP_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # 2. Read and Chunk Text
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        full_text = clean_text(f.read())
    
    chunks = split_into_chunks(full_text, CHUNK_SIZE)
    total_chunks = len(chunks)
    
    # 3. Load Resume State
    state = load_state()
    start_index = state["last_completed_chunk"] + 1
    print(f"Total Chunks: {total_chunks}. Resuming from Chunk {start_index}...")

    # 4. Processing Loop
    for i in range(start_index, total_chunks):
        print(f"--- Processing Chunk {i+1}/{total_chunks} ---")
        
        wav_path = os.path.join(TEMP_FOLDER, f"chunk_{i}.wav")
        mp3_path = os.path.join(TEMP_FOLDER, f"chunk_{i}.mp3")

        # Generate Audio
        run_piper(chunks[i], wav_path)
        
        # Convert to MP3
        convert_to_mp3(wav_path, mp3_path)
        
        # Cleanup WAV immediately to save space
        if os.path.exists(wav_path):
            os.remove(wav_path)
            
        # Update State
        save_state(i, total_chunks)

    # 5. Final Concatenation
    print("All chunks completed. Joining into final MP3...")
    
    # Create a list file for ffmpeg
    list_file_path = os.path.join(TEMP_FOLDER, "file_list.txt")
    with open(list_file_path, 'w') as f:
        for i in range(total_chunks):
            f.write(f"file 'chunk_{i}.mp3'\n")

    final_output = os.path.join(OUTPUT_FOLDER, "final_audiobook.mp3")
    
    # Run ffmpeg concat
    subprocess.run([
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0', 
        '-i', list_file_path, '-c', 'copy', final_output
    ], check=True)

    print(f"Success! Audiobook saved to: {final_output}")
    
    # Optional: Wipe temp folder and state on 100% completion
    # shutil.rmtree(TEMP_FOLDER)
    # os.remove(STATE_FILE)

if __name__ == "__main__":
    main()
