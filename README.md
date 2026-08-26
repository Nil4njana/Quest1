# Audio Frame Identifier

A speech-based video search system that finds the **first occurrence of a spoken dialogue in a video** and extracts the corresponding video frame.

The system does not depend on subtitles or on-screen text. Instead, it uses **word-level speech transcription** to determine when a dialogue is spoken and maps that timestamp back to the original video to extract the corresponding frame.

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

# Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3.11** | Core application and pipeline implementation |
| **Faster-Whisper** | Speech-to-text transcription with word-level timestamps |
| **FFmpeg** | Audio extraction and video frame extraction |
| **FFprobe** | Video/audio metadata, duration, and frame-rate detection |
| **yt-dlp** | Downloading videos from supported online sources |
| **pytest** | Automated unit and integration testing |
| **PowerShell** | Development and command-line execution environment |

### Example

Input

```text
Video:
<video URL>

Dialogue:
My mind rebels at stagnation

Choose Approach:
1.Full transcription
2.Progressive transcription
Approach 1/2: 1

**Output**:
