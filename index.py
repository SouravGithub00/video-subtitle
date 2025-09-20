import os
import ffmpeg
import whisperx
import pandas as pd
import argparse

# -----------------------------
# 0. Parse command-line arguments
# -----------------------------
parser = argparse.ArgumentParser(description="Process video to generate subtitles.")
parser.add_argument("--start", type=float, required=False, help="Start time in seconds (optional)")
parser.add_argument("--end", type=float, required=False, help="End time in seconds (optional)")
parser.add_argument("--language", type=str, required=False, help="Language code (optional)")
args = parser.parse_args()

# -----------------------------
# Handle optional start and end arguments
# -----------------------------
start_time = args.start if args.start is not None else 0
end_time = args.end if args.end is not None else None
language = args.language if args.language is not None else None

# -----------------------------
# 0. Setup paths
# -----------------------------
input_dir = "input"
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# -----------------------------
# 1. Extract audio from video
# -----------------------------
video_file = os.path.join(input_dir, "input.mp4")
audio_file = os.path.join(input_dir, "audio.wav")

input_kwargs = {}
if start_time:
    input_kwargs['ss'] = start_time
if end_time:
    input_kwargs['to'] = end_time


# Convert video to mono 16kHz wav (needed for WhisperX)
(
    ffmpeg
    .input(video_file, **input_kwargs)
    .output(audio_file, ac=1, ar=16000)
    .overwrite_output()
    .run()
)

# -----------------------------
# 2. Load WhisperX model
# -----------------------------
device = "cpu"   # change to "cuda" if you have a GPU
batch_size = 16

input_args = {}
if language:
    input_args['language'] = language

model = whisperx.load_model("small", device, compute_type="float32", **input_args)

# -----------------------------
# 3. Transcribe audio
# -----------------------------
result = model.transcribe(audio_file, batch_size=batch_size)

print("Detected Language:", result["language"])

# -----------------------------
# 4. Word-level alignment
# -----------------------------
model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
aligned_result = whisperx.align(result["segments"], model_a, metadata, audio_file, device=device)


# -----------------------------
# 4. Save word-level timestamps to CSV
# -----------------------------
rows = []
for segment in aligned_result["segments"]:
    for word in segment["words"]:
        rows.append({
            "word": word["word"],
            "start": word["start"] + start_time,
            "end": word["end"] + start_time
        })

df = pd.DataFrame(rows)
output_csv_path = os.path.join(output_dir, "subtitles.csv")
df.to_csv(output_csv_path, index=False)

print(f"✅ Word-level subtitles saved to {output_csv_path}")