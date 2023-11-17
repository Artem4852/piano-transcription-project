from common import getTrainingFiles, getTrainingData, trainCLF, np

trainingFiles = getTrainingFiles(True, True)
trainingFiles.sort()

X, y = [], []
for n, _file in enumerate(trainingFiles):
  print(f"Processing {_file} - {n+1}/{len(trainingFiles)}")
  localX, _, localY, _ = getTrainingData(_file, tempFolder="lengthTemp")
  y += localY
  for note in localX:
    X.append([note["pitch"], np.max(note["harmonic"]), len(note["harmonic"].flatten().tolist()), note["spectrogramLength"]])

trainCLF(X, y, True, "lengthClassifierNew")