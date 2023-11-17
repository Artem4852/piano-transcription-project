import librosa, os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

shapes = []
# Load audio file
for n in range(len(os.listdir("notesTemp"))):
  y, sr = librosa.load(f'notesTemp/note{n}.wav', sr=None)
  print(f"Note {n} - {y.shape}")
  shapes.append(y.shape)

print(max(shapes))

# pd.DataFrame(y).to_csv("yraw.csv", index=False)

# Plot waveform, one over anoteher
# plt.figure(figsize=(10, 4))
# librosa.display.waveshow(y, sr=sr)
# plt.xlabel('Time')
# plt.ylabel('Amplitude')
# plt.title('Audio Waveform')
# plt.show()