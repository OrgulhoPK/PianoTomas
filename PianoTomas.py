from mido import MidiFile, merge_tracks
import sys
import os
import locale
from collections import defaultdict

# =========================================================
# 🌍 IDIOMA DO SISTEMA
# =========================================================
lang, _ = locale.getdefaultlocale()
lang = (lang or "en")[:2]

TEXTS = {
    "pt": {
        "title": "😄🎹 PianoTomas",
        "found": "Arquivos MIDI encontrados:",
        "choose": "Digite o NÚMERO do MIDI que deseja converter:",
        "selected": "✔ MIDI selecionado:",
        "converting": "Convertendo...",
        "success": "✔ Arquivo .ahk gerado com sucesso!",
        "follow": "✔ Me ajude seguindo e assistindo meus vídeos no YouTube/gaming.",
        "exit": "Pressione Enter para sair..."
    },
    "en": {
        "title": "😄🎹 PianoTomas",
        "found": "MIDI files found:",
        "choose": "Enter the NUMBER of the MIDI you want to convert:",
        "selected": "✔ Selected MIDI:",
        "converting": "Converting...",
        "success": "✔ .ahk file generated successfully!",
        "follow": "✔ Help me out by following me and watching my videos on YouTube/gaming.",
        "exit": "Press Enter to exit..."
    },
    "es": {
        "title": "😄🎹 PianoTomas",
        "found": "Archivos MIDI encontrados:",
        "choose": "Ingrese el NÚMERO del MIDI que desea convertir:",
        "selected": "✔ MIDI seleccionado:",
        "converting": "Convirtiendo...",
        "success": "✔ Archivo .ahk generado con éxito!",
        "follow": "✔ Ayúdame siguiéndome y viendo mis videos en YouTube/gaming.",
        "exit": "Presione Enter para salir..."
    },
    "fr": {
        "title": "😄🎹 PianoTomas",
        "found": "Fichiers MIDI trouvés :",
        "choose": "Entrez le NUMÉRO du MIDI à convertir :",
        "selected": "✔ MIDI sélectionné :",
        "converting": "Conversion en cours...",
        "success": "✔ Fichier .ahk généré avec succès !",
        "follow": "✔ Aidez-moi en me suivant et en regardant mes vidéos sur YouTube/gaming.",
        "exit": "Appuyez sur Entrée pour quitter..."
    },
    "de": {
        "title": "😄🎹 PianoTomas",
        "found": "Gefundene MIDI-Dateien:",
        "choose": "Geben Sie die NUMMER des MIDI ein, das konvertiert werden soll:",
        "selected": "✔ Ausgewähltes MIDI:",
        "converting": "Wird konvertiert...",
        "success": "✔ .ahk-Datei erfolgreich erstellt!",
        "follow": "✔ Unterstütze mich, indem du mir folgst und meine YouTube-/Gaming-Videos ansiehst.",
        "exit": "Drücken Sie Enter zum Beenden..."
    },
    "zh": {
        "title": "😄🎹 PianoTomas",
        "found": "找到的 MIDI 文件：",
        "choose": "输入要转换的 MIDI 编号：",
        "selected": "✔ 已选择 MIDI：",
        "converting": "正在转换...",
        "success": "✔ 已成功生成 .ahk 文件！",
        "follow": "✔ 欢迎关注我并观看我的 YouTube / 游戏视频。",
        "exit": "按 Enter 键退出..."
    }
}

T = TEXTS.get(lang, TEXTS["en"])

# =========================================================
# ⚙️ CONFIGURAÇÕES MUSICAIS
# =========================================================
MAX_CHORD_NOTES = 4
DEFAULT_TEMPO = 500000
START_OCTAVE = 3
MIN_OCTAVE = 2
MAX_OCTAVE = 4

NOTE_KEYS = {
    0: "Numpad1", 2: "Numpad2", 4: "Numpad3", 5: "Numpad4",
    7: "Numpad5", 9: "Numpad6", 11: "Numpad7",
    1: "F1", 3: "F2", 6: "F3", 8: "F4", 10: "F5",
}

def note_to_octave(note):
    return note // 12 - 1

def clamp_octave(o):
    return max(MIN_OCTAVE, min(MAX_OCTAVE, o))

def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

# =========================================================
# 🎛️ INTERFACE
# =========================================================
base_path = get_base_path()

print(T["title"])
print("=" * 40)
print(T["found"], "\n")

midis = sorted(f for f in os.listdir(base_path) if f.lower().endswith(".mid"))

if not midis:
    print("❌ No MIDI files found.")
    input(T["exit"])
    sys.exit()

for i, m in enumerate(midis, 1):
    print(f" {i:2d} - {m}")

print("\n" + T["choose"])
try:
    choice = int(input("> "))
    midi_name = midis[choice - 1]
except:
    input(T["exit"])
    sys.exit()

midi_path = os.path.join(base_path, midi_name)
print(f"\n{T['selected']} {midi_name}")
print(T["converting"], "\n")

# =========================================================
# 🎼 ENGINE MUSICAL
# =========================================================
mid = MidiFile(midi_path)
merged = merge_tracks(mid.tracks)

current_tempo = DEFAULT_TEMPO
time_us = 0
events = []

for msg in merged:
    time_us += msg.time * current_tempo / mid.ticks_per_beat
    if msg.type == "set_tempo":
        current_tempo = msg.tempo
    elif msg.type == "note_on" and msg.velocity > 0:
        events.append((int(time_us), msg.note))

grouped = defaultdict(list)
for t, n in events:
    grouped[t].append(n)

times = sorted(grouped)

ahk = ["l::"]
current_oct = START_OCTAVE
last_time = 0

for t in times:
    sleep = max(1, int((t - last_time) / 1000))
    ahk.append(f"Sleep, {sleep}")
    last_time = t

    notes = grouped[t]
    by_oct = defaultdict(list)
    for n in notes:
        by_oct[note_to_octave(n)].append(n)

    target_oct = clamp_octave(max(by_oct, key=lambda x: len(by_oct[x])))

    while current_oct < target_oct:
        ahk.append("SendInput {Numpad9}")
        current_oct += 1
    while current_oct > target_oct:
        ahk.append("SendInput {Numpad0}")
        current_oct -= 1

    chord = []
    for n in notes:
        octv = note_to_octave(n)
        pitch = n % 12
        if pitch == 0 and octv == current_oct + 1:
            chord.append("Numpad8")
        elif octv == current_oct:
            if pitch in NOTE_KEYS:
                chord.append(NOTE_KEYS[pitch])

    chord = list(dict.fromkeys(chord))[:MAX_CHORD_NOTES]
    if not chord:
        continue

    ahk.append("SendInput " + "".join(f"{{{k} down}}" for k in chord))
    ahk.append("Sleep, 25")
    ahk.append("SendInput " + "".join(f"{{{k} up}}" for k in chord))

ahk.append("'::Pause")

# =========================================================
# 💾 SALVAR AHK
# =========================================================
out_name = os.path.splitext(midi_name)[0] + ".ahk"
with open(os.path.join(base_path, out_name), "w", encoding="utf-8") as f:
    f.write("\n".join(ahk))

print(T["success"])
print(T["follow"])
print("✔ https://www.youtube.com/@pkdorevil")
input("\n" + T["exit"])
from mido import MidiFile, merge_tracks
import sys
import os
import locale
from collections import defaultdict

# =========================================================
# 🌍 IDIOMA DO SISTEMA
# =========================================================
lang, _ = locale.getdefaultlocale()
lang = (lang or "en")[:2]

TEXTS = {
    "pt": {
        "title": "😄🎹 PianoTomas",
        "found": "Arquivos MIDI encontrados:",
        "choose": "Digite o NÚMERO do MIDI que deseja converter:",
        "selected": "✔ MIDI selecionado:",
        "converting": "Convertendo...",
        "success": "✔ Arquivo .ahk gerado com sucesso!",
        "follow": "✔ Me ajude seguindo e assistindo meus vídeos no YouTube/gaming.",
        "exit": "Pressione Enter para sair..."
    },
    "en": {
        "title": "😄🎹 PianoTomas",
        "found": "MIDI files found:",
        "choose": "Enter the NUMBER of the MIDI you want to convert:",
        "selected": "✔ Selected MIDI:",
        "converting": "Converting...",
        "success": "✔ .ahk file generated successfully!",
        "follow": "✔ Help me out by following me and watching my videos on YouTube/gaming.",
        "exit": "Press Enter to exit..."
    },
    "es": {
        "title": "😄🎹 PianoTomas",
        "found": "Archivos MIDI encontrados:",
        "choose": "Ingrese el NÚMERO del MIDI que desea convertir:",
        "selected": "✔ MIDI seleccionado:",
        "converting": "Convirtiendo...",
        "success": "✔ Archivo .ahk generado con éxito!",
        "follow": "✔ Ayúdame siguiéndome y viendo mis videos en YouTube/gaming.",
        "exit": "Presione Enter para salir..."
    },
    "fr": {
        "title": "😄🎹 PianoTomas",
        "found": "Fichiers MIDI trouvés :",
        "choose": "Entrez le NUMÉRO du MIDI à convertir :",
        "selected": "✔ MIDI sélectionné :",
        "converting": "Conversion en cours...",
        "success": "✔ Fichier .ahk généré avec succès !",
        "follow": "✔ Aidez-moi en me suivant et en regardant mes vidéos sur YouTube/gaming.",
        "exit": "Appuyez sur Entrée pour quitter..."
    },
    "de": {
        "title": "😄🎹 PianoTomas",
        "found": "Gefundene MIDI-Dateien:",
        "choose": "Geben Sie die NUMMER des MIDI ein, das konvertiert werden soll:",
        "selected": "✔ Ausgewähltes MIDI:",
        "converting": "Wird konvertiert...",
        "success": "✔ .ahk-Datei erfolgreich erstellt!",
        "follow": "✔ Unterstütze mich, indem du mir folgst und meine YouTube-/Gaming-Videos ansiehst.",
        "exit": "Drücken Sie Enter zum Beenden..."
    },
    "zh": {
        "title": "😄🎹 PianoTomas",
        "found": "找到的 MIDI 文件：",
        "choose": "输入要转换的 MIDI 编号：",
        "selected": "✔ 已选择 MIDI：",
        "converting": "正在转换...",
        "success": "✔ 已成功生成 .ahk 文件！",
        "follow": "✔ 欢迎关注我并观看我的 YouTube / 游戏视频。",
        "exit": "按 Enter 键退出..."
    }
}

T = TEXTS.get(lang, TEXTS["en"])

# =========================================================
# ⚙️ CONFIGURAÇÕES MUSICAIS
# =========================================================
MAX_CHORD_NOTES = 4
DEFAULT_TEMPO = 500000
START_OCTAVE = 3
MIN_OCTAVE = 2
MAX_OCTAVE = 4

NOTE_KEYS = {
    0: "Numpad1", 2: "Numpad2", 4: "Numpad3", 5: "Numpad4",
    7: "Numpad5", 9: "Numpad6", 11: "Numpad7",
    1: "F1", 3: "F2", 6: "F3", 8: "F4", 10: "F5",
}

def note_to_octave(note):
    return note // 12 - 1

def clamp_octave(o):
    return max(MIN_OCTAVE, min(MAX_OCTAVE, o))

def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

# =========================================================
# 🎛️ INTERFACE
# =========================================================
base_path = get_base_path()

print(T["title"])
print("=" * 40)
print(T["found"], "\n")

midis = sorted(f for f in os.listdir(base_path) if f.lower().endswith(".mid"))

if not midis:
    print("❌ No MIDI files found.")
    input(T["exit"])
    sys.exit()

for i, m in enumerate(midis, 1):
    print(f" {i:2d} - {m}")

print("\n" + T["choose"])
try:
    choice = int(input("> "))
    midi_name = midis[choice - 1]
except:
    input(T["exit"])
    sys.exit()

midi_path = os.path.join(base_path, midi_name)
print(f"\n{T['selected']} {midi_name}")
print(T["converting"], "\n")

# =========================================================
# 🎼 ENGINE MUSICAL
# =========================================================
mid = MidiFile(midi_path)
merged = merge_tracks(mid.tracks)

current_tempo = DEFAULT_TEMPO
time_us = 0
events = []

for msg in merged:
    time_us += msg.time * current_tempo / mid.ticks_per_beat
    if msg.type == "set_tempo":
        current_tempo = msg.tempo
    elif msg.type == "note_on" and msg.velocity > 0:
        events.append((int(time_us), msg.note))

grouped = defaultdict(list)
for t, n in events:
    grouped[t].append(n)

times = sorted(grouped)

ahk = ["l::"]
current_oct = START_OCTAVE
last_time = 0

for t in times:
    sleep = max(1, int((t - last_time) / 1000))
    ahk.append(f"Sleep, {sleep}")
    last_time = t

    notes = grouped[t]
    by_oct = defaultdict(list)
    for n in notes:
        by_oct[note_to_octave(n)].append(n)

    target_oct = clamp_octave(max(by_oct, key=lambda x: len(by_oct[x])))

    while current_oct < target_oct:
        ahk.append("SendInput {Numpad9}")
        current_oct += 1
    while current_oct > target_oct:
        ahk.append("SendInput {Numpad0}")
        current_oct -= 1

    chord = []
    for n in notes:
        octv = note_to_octave(n)
        pitch = n % 12
        if pitch == 0 and octv == current_oct + 1:
            chord.append("Numpad8")
        elif octv == current_oct:
            if pitch in NOTE_KEYS:
                chord.append(NOTE_KEYS[pitch])

    chord = list(dict.fromkeys(chord))[:MAX_CHORD_NOTES]
    if not chord:
        continue

    ahk.append("SendInput " + "".join(f"{{{k} down}}" for k in chord))
    ahk.append("Sleep, 25")
    ahk.append("SendInput " + "".join(f"{{{k} up}}" for k in chord))

ahk.append("'::Pause")

# =========================================================
# 💾 SALVAR AHK
# =========================================================
out_name = os.path.splitext(midi_name)[0] + ".ahk"
with open(os.path.join(base_path, out_name), "w", encoding="utf-8") as f:
    f.write("\n".join(ahk))

print(T["success"])
print(T["follow"])
print("✔ https://www.youtube.com/@pkdorevil")
input("\n" + T["exit"])

sys.exit(0)