import librosa, os
import numpy as np
import pandas as pd
from pydub import AudioSegment

MARGINR = 25
MARGINL = 35

def separateNotes(filename, tempFolder):
  os.system(f"rm -rf {tempFolder}")
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

def getFeatures(tempFolder):
  notes = []

  noteFiles = os.listdir(tempFolder)
  noteFiles.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))

  print()
  for n, noteFile in enumerate(noteFiles):
    print(f"\033[1AProcessing {noteFile} ({n+1}/{len(noteFiles)})")
    y, sr = librosa.load(f"{tempFolder}/{noteFile}")

    spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)
    logSpectrogram = librosa.amplitude_to_db(spectrogram, ref=np.max)

    frequencies, magnitudes = librosa.piptrack(y=y, sr=sr)
    estimatedPitch = frequencies[np.argmax(magnitudes, axis=0)]

    harmonic, _ = librosa.effects.hpss(y)

    notes.append({
      "pitch": round(np.mean([x for x in estimatedPitch[0] if x > 0]), 2),
      "spectrogram": logSpectrogram,
      "spectrogramLength": logSpectrogram.shape[1],
      "harmonic": harmonic,
      "harmonicMax": np.max(harmonic)
    })

  os.system(f"rm -rf {tempFolder}")
  return notes
  
def extractFeatures(filename, tempFolder="notesTemp"):
  print("Separating notes")
  onsetTimes = separateNotes(filename, tempFolder)
  print("Extracting features")
  notes = getFeatures(tempFolder)
  print("Done\n")
  return notes, onsetTimes

if __name__ == "__main__":
  notes, onsetTimes = extractFeatures("media/testing/lengthtest1.wav")
  print(notes)
  print(onsetTimes)