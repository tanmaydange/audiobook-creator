import os

# --- Step 1: Prepare and Save the New Text File ---
input_filename = '../input/The-Collected-Short-Stories-Jeffrey-Archer.txt'
output_filename = '../input/novel_prepared_for_audio.txt'

def prepare_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. Basic Cleaning (Removes Gutenberg Headers/Footers)
    start_tag = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_tag = "*** END OF THE PROJECT GUTENBERG EBOOK"
    if start_tag in text:
        text = text.split(start_tag, 1)[1]
    if end_tag in text:
        text = text.split(end_tag, 1)[0]

    # 2. Apply your Pause Logic (Replacing punctuation with line breaks)
    text = text.replace(". ", ".\n\n") 
    text = text.replace("? ", "?\n\n")
    text = text.replace("! ", "!\n\n")
    
    # 3. Final cleanup of whitespace (Optional)
    # text = "\n".join([line.strip() for line in text.splitlines() if line.strip()])
    
    return text

# Run the preparation
cleaned_text = prepare_text(input_filename)

# Save as a new file
with open(output_filename, 'w', encoding='utf-8') as f:
    f.write(cleaned_text)

print(f"Success! Narrator-ready text saved to: {output_filename}")

