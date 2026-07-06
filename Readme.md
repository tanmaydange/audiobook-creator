# 📖 Audiobook Creator

This project provides a complete workflow for converting text novels into high-quality, natural-sounding **MP3 audiobooks**.

It uses **Piper TTS**, an open-source neural text-to-speech engine that runs entirely locally on your machine—ensuring privacy and avoiding the robotic voices typical of older TTS systems.

## ✨ Features

* **Natural Voice:** Uses neural-network-based models for realistic speech.
* **Local Processing:** No internet connection required after the initial setup.
* **Automatic Chunking:** Automatically splits large novels into smaller segments to handle API/memory limits.
* **Final MP3 Export:** Combines all segments into a single, portable MP3 file.
* **Gutenberg Ready:** Includes logic to clean header/footer metadata from text files.

---

## 🛠️ Prerequisites

Before starting, ensure you have the following installed on your Linux Mint system:

* **Python 3.10+**
* **FFmpeg** (Required for MP3 encoding)
* **Git** (Optional, for version control)

```bash
sudo apt update
sudo apt install -y ffmpeg python3-venv python3-pip

```

---

## 🚀 Installation & Setup

### 1. Clone or Create the Directory

```bash
mkdir audiobook-creator
cd audiobook-creator

```

### 2. Set Up Virtual Environment

```bash
python3 -m venv pyvenv
source pyvenv/bin/activate

```

### 3. Install Dependencies

Create a `requirements.txt` file and install:

```bash
pip install -r requirements.txt

```

### 4. Download the Neural Voice Model

The project uses the `en_US-lessac-medium` voice. You must download the model (`.onnx`) and its configuration (`.json`):

```bash
mkdir models
wget -P models/ https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/en_US-lessac-medium/en_US-lessac-medium.onnx
wget -P models/ https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/en_US-lessac-medium/en_US-lessac-medium.onnx.json

```

---

## 📋 Usage Guide

### Step 1: Prepare the Text

Download your novel from [Project Gutenberg](https://www.gutenberg.org/) as a Plain Text file. Place it in the project folder.

### Step 2: Run the Conversion

1. Open `create_audiobook.py`.
2. Change the `INPUT_TEXT_FILE` variable to match your filename (e.g., `dracula.txt`).
3. Run the script:

```bash
python3 create_audiobook.py

```

### Step 3: Enjoy

Once the script finishes, you will find a file named `Novel_Audiobook_Final.mp3` in your project directory.

---

## 📁 Project Structure

```text
.
├── model/                  # Voice model files (.onnx, .json)
├── pysrc/temp_wav_files/          # Auto-created/deleted during processing
├── pyvenv/                    # Python virtual environment
├── pysrc/create_audiobook.py      # The main processing script
├── requirements.txt         # Python dependencies
└── input/your_novel.txt           # Your input file

```

---

## 🛠️ Troubleshooting

* **Slow Processing:** Neural TTS is CPU intensive. On older hardware, a full novel may take 30-60 minutes to render.
* **Audio Quality:** If the voice is too fast or slow, you can adjust the Piper flags in the `subprocess.run` command within `create_audiobook.py` (e.g., adding `"--length_scale", "1.1"` for slower speech).
* **Memory Errors:** If the script crashes, try lowering the `MAX_CHARS_PER_CHUNK` value in the script.

## ⚖️ License

This project is open-source. Piper TTS models are subject to their own respective licenses (usually Creative Commons). Project Gutenberg texts are generally Public Domain in the USA.

