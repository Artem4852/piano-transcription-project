from common import getTrainingFiles, getTrainingData, trainCLF, padHarmonic, padSpectrogram, np

trainingFiles = getTrainingFiles(True, False, True)
trainingFiles.sort()

X, y = [], []
for n, _file in enumerate(trainingFiles):
  print(f"Processing {_file} - {n+1}/{len(trainingFiles)}")
  localX, _, _, localY = getTrainingData(_file, tempFolder="restsTemp")
  y += localY
  for note in localX:
    X.append([note["pitch"], np.max(note["harmonic"]), note["harmonic"], note["spectrogram"]])

print("Padding")
X = [[piece[0], piece[1]] + padHarmonic(piece[2]) + padSpectrogram(piece[3]) for piece in X]
# print(y)

print("Training")
trainCLF(X, y, True, "restsClassifier")