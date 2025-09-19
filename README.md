
<!--
pip install git+https://github.com/m-bain/whisperx.git
pip install ffmpeg-python
pip install srt
-->


## Prerequisites

### 1. Install Python

1. Download Python 3.12 (or later) from [https://www.python.org/downloads/mac-osx/](https://www.python.org/downloads/mac-osx/).  
2. Open the downloaded `.pkg` file and follow the instructions to install Python.  
3. Verify Python installation:

```bash
python3 --version
````

---

### 2. Install Homebrew (if not installed)

Homebrew is a package manager for macOS:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

---

### 3. Install FFmpeg

FFmpeg is required to extract audio from videos:

```bash
brew install ffmpeg
```

Verify installation:

```bash
ffmpeg -version
```

---

### 4. Install Project Dependencies

1. Open Terminal and navigate to the project folder.
2. Create a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

then run
```bash
python3 index.py
```

---

### 5. Fix SSL Certificate Issues (if needed)

If Python fails to verify SSL certificates:

1. Run the Python installer helper:

```bash
open /Applications/Python\ 3.x/Install\ Certificates.command
```

Replace `3.x` with your Python version (e.g., `3.12`).


---

## Running the Script

1. Place your video file as `input.mp4` inside the `input/` folder of the repo.
2. Run the main script:

```bash
python3 index.py
```

3. After processing, the word-level subtitles will be saved as `subtitles.csv` in the project folder.

---

## Input / Output

* **Input:** `input/input.mp4`
* **Output:** `subtitles.csv`