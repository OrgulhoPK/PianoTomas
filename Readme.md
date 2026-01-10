 # 🎹 MacroMaestro

**MacroMaestro** is a MIDI → AutoHotkey (.ahk) converter designed for **Guild Wars 2 piano macros**.

It allows you to:
- Convert MIDI files into playable AutoHotkey scripts
- Play melodies and chords accurately in-game
- Handle octave changes and chords (up to 4 notes)
- Avoid unnecessary octave switching
- Generate clean and readable `.ahk` files

---

## 🎮 Designed for Guild Wars 2

MacroMaestro follows the GW2 piano layout logic:
- Octave tabs
- Chord limits
- Melodic-aware note selection
- Accurate timing based on MIDI tempo

---

## ✨ Features

- 🎼 MIDI parsing with tempo awareness
- 🎹 Chord support (up to 4 notes)
- 🔁 Smart octave switching
- ⏱ Accurate timing (Sleep in ms)
- 📁 Auto-detect MIDI files in folder
- 🖥 Interactive CLI (choose MIDI by number)
- 📝 Generates ready-to-use `.ahk` scripts

---

## 🚀 How to use

### 1️⃣ Requirements
- Python 3.9+
- Windows
- AutoHotkey v1

### 2️⃣ Run
Place `MacroMaestro.py` in a folder with your `.mid` files and run:

```bash
python MacroMaestro.py

### 3️⃣ Select MIDI

The program will list all MIDI files:

1 - River Flows in You.mid
2 - Through The Fire And Flames.mid


Type the number and press ENTER.

### 4️⃣ Done!

A .ahk file will be generated in the same folder.

🛠 Planned features

 Executable (.exe) release

 Optional track filtering

 Visual debug mode

 Presets for different instruments

## 🧠 Notes

Drum tracks should be removed before conversion

Best results with clean piano MIDI files

You can edit the MIDI externally (Aria, Guitar Pro, etc.)

## ❤️ Support & Community

If you enjoy the project:

⭐ Star the repository

🧪 Test and give feedback

🎥 Follow me on YouTube:

👉 https://www.youtube.com/@pkdorevil

👉 Discord: orgulhopk

## ⚠ Disclaimer

This project is not affiliated with ArenaNet.