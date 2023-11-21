from common import getTrainingFiles, getTrainingData, trainCLF, np

trainingFiles = getTrainingFiles(True, True, alllengths=True)
trainingFiles.sort()

X, y = [], []
for n, _file in enumerate(trainingFiles):
  print(f"Processing {_file} - {n+1}/{len(trainingFiles)}")
  localX, _, localY, _ = getTrainingData(_file, tempFolder="lengthTemp")
  y += localY
  for note in localX:
    X.append([note["pitch"], len(note["harmonic"].flatten().tolist()), note["spectrogramLength"], note["spectrogramLength"], note["spectrogramLength"], note["spectrogramLength"]])

model = trainCLF(X, y, True, "lengthClassifierNewNew")

# start of training   16 08 57
# end of training     16 14 42
# total:              00 05 45