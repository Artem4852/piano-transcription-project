from common import getTrainingFiles, getTrainingData, trainCLF, np

trainingFiles = getTrainingFiles(False, True, False, True)
trainingFiles.sort()

X, y = [], []
for n, _file in enumerate(trainingFiles):
  print(f"Processing {_file} - {n+1}/{len(trainingFiles)}")
  localX, localY, _, _ = getTrainingData(_file, tempFolder="pitchTemp")
  y += localY
  for note in localX:
    X.append([note["pitch"], np.max(note["harmonic"]), np.mean(note["harmonic"]), np.max(note["spectrogram"]), np.mean(note["spectrogram"])])

trainCLF(X, y, True, "pitchClassifier")