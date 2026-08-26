# Audio Frame Identifier

A speech-based video search system that finds the **first occurrence of a spoken dialogue in a video** and extracts the corresponding video frame.

The system does not depend on subtitles or on-screen text. Instead, it uses **word-level speech transcription** to determine when a dialogue is spoken and maps that timestamp back to the original video to extract the corresponding frame.

The system processes the video's audio using Faster-Whisper to obtain word-level timestamps, then uses normalized text matching and similarity scoring to locate the dialogue.
It supports both full-audio transcription and progressive chunk-based transcription, allowing the first qualifying occurrence to be found and mapped back to the corresponding video frame.

---

## Problem Statement

Given:

- A video URL
- A spoken dialogue to search for

the system identifies:

- Whether the dialogue occurs in the video
- The first occurrence of the dialogue
- The start and end timestamps
- The transcribed text that matched the query
- The similarity score
- The corresponding video frame
- The location where the extracted frame was saved

---

## Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3.11** | Core application and pipeline implementation |
| **Faster-Whisper** | Speech-to-text transcription with word-level timestamps |
| **FFmpeg** | Audio extraction and video frame extraction |
| **FFprobe** | Video/audio metadata, duration, and frame-rate detection |
| **yt-dlp** | Downloading videos from supported online sources |
| **pytest** | Automated unit and integration testing |
| **PowerShell** | Development and command-line execution environment |

---

## Project Structure

```text
Audio Frame Identifier/
│
│
├── data/
│   ├── raw/
│   │   └── Downloaded video files
│   │
│   ├── audio/
│       └── Extracted WAV audio files
│
├── outputs/
│   ├── frames/
│   │   └── Frames returned by dialogue searches
│   │
│   ├── transcripts/
│       └── Saved word-level transcripts
│
├── src/
│   ├── approach1/
│   │   └── Full-transcription dialogue search
│   │
│   ├── approach2/
│   │   └── Progressive/incremental transcription and search
│   │
│   └── common/
│       └── Shared functionality such as:
│           ├── video downloading
│           ├── audio extraction
│           ├── transcription
│           ├── text matching
│           ├── timestamp handling
│           └── frame extraction
│
├── tests/
│   ├── test_audio.py
│   ├── test_frame_extraction.py
│   ├── test_matching.py
│   ├── test_progressive_search.py
│   ├── test_progressive_transcription.py
│   ├── test_transcript.py
│   └── test_transcription.py
│
├── main.py
├── requirements.txt
├── pytest.ini
├── SYSTEM_REQUIREMENTS.md
├── USER_GUIDELINES.md
├── APPROACH.md
├── PROMPTS.txt
└── README.md
