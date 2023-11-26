import librosa, os, shutil
import numpy as np
import pandas as pd
from pydub import AudioSegment
from termcolor import colored

MARGINR = 25
MARGINL = 35

def separateNotes(filename, tempFolder):
  shutil.rmtree(tempFolder, ignore_errors=True)
  os.makedirs(tempFolder)

  y, sr = librosa.load(filename)

  onsetFrames = librosa.onset.onset_detect(y=y, sr=sr)
  onsetTimes = librosa.frames_to_time(onsetFrames, sr=sr)
  onsetTimesMs = [int(x * 1000) for x in onsetTimes]
  # onsetTimesMs.insert(0, 0)

  audio = AudioSegment.from_wav(filename)
  for i in range(len(onsetTimesMs)-1):
    audio[onsetTimesMs[i]-MARGINR:onsetTimesMs[i+1]-MARGINL].export(f"{tempFolder}/note{i}.wav", format="wav")
  audio[onsetTimesMs[i+1]-MARGINR:].export(f"{tempFolder}/note{i+1}.wav", format="wav")

  return onsetTimes

def getFeatures(tempFolder, lang):
  notes = []

  noteFiles = os.listdir(tempFolder)
  noteFiles.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))

  print(colored("    " + str(len(noteFiles)) + (" notes detected" if lang == 'eng' else ' нот розпізнано' if lang == 'ukr' else ' нот распознано'), "cyan"))

  print()
  for n, noteFile in enumerate(noteFiles):
    print(colored(f"\033[1A    {'Processing' if lang == 'eng' else 'Опрацювання' if lang == 'ukr' else 'Загрузка'} {noteFile} ({n+1}/{len(noteFiles)})", "cyan"))
    y, sr = librosa.load(f"{tempFolder}/{noteFile}")

    spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)
    logSpectrogram = librosa.amplitude_to_db(spectrogram, ref=np.max)

    rms = librosa.feature.rms(y=y)

    frequencies, magnitudes = librosa.piptrack(y=y, sr=sr)
    estimatedPitch = frequencies[np.argmax(magnitudes, axis=0)]

    harmonic, _ = librosa.effects.hpss(y)

    notes.append({
      "pitch": round(np.mean([x for x in estimatedPitch[0] if x > 0]), 2),
      "spectrogram": logSpectrogram,
      "spectrogramLength": logSpectrogram.shape[1],
      "harmonic": harmonic,
      "harmonicMax": np.max(harmonic),
      "rms": rms,
      "amplitude": y,
    })

  # os.system(f"rm -rf {tempFolder}")
  return notes
  
def extractFeatures(filename, tempFolder="notesTemp", lang="eng"):
  print(colored("    " + ("Separating notes" if lang == "eng" else "Розділення нот" if lang == "ukr" else "Разделение нот"), "cyan"))
  onsetTimes = separateNotes(filename, tempFolder)
  print(colored("    " + ("Analyzing notes" if lang == "eng" else "Аналіз нот" if lang == "ukr" else "Анализ нот"), "cyan"))
  notes = getFeatures(tempFolder, lang=lang)
  return notes, onsetTimes

if __name__ == "__main__":
  notes, onsetTimes = extractFeatures("media/testing/resttest1.wav")
  for n, note in enumerate(notes):
    df = pd.DataFrame(note["spectrogram"])
    df.to_csv(f"spects/spect_{n}.csv", index=False)