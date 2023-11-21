from common import getTrainingFiles, getTrainingData, trainCLF, padRms, np
import pickle

loadData = False

trainingFiles = getTrainingFiles(True, False, True)
trainingFiles.sort()


X, y, rawX = [], [], []
for n, _file in enumerate(trainingFiles):
  if loadData: continue
  print(f"Processing {_file} - {n+1}/{len(trainingFiles)}")
  localX, _, _, localY = getTrainingData(_file, tempFolder="restsTemp")
  rawX += localX
  y += localY
  for note in localX:
    X.append([note["pitch"], note["harmonicMax"], np.mean(note["harmonic"]), note["rms"]])
    # X.append([note["pitch"], note["rms"], note["amplitude"]])

if loadData:
  rawX = pickle.load(open("models/data/restsX.pkl", "rb"))
  X = [[note["pitch"], note["harmonicMax"], np.mean(note["harmonic"]), note["rms"]] for note in rawX]
  # X = [[note["pitch"], note["rms"], note["amplitude"]] for note in rawX]
  y = pickle.load(open("models/data/restsY.pkl", "rb"))
else:
  pickle.dump(rawX, open("models/data/restsX.pkl", "wb"))
  pickle.dump(y, open("models/data/restsY.pkl", "wb"))

print("Padding")
X = [[piece[0]] + padRms(piece[1], n) for n, piece in enumerate(X)]
# X = [[piece[0]] + padRms(piece[1]) + padAmplitude(piece[2], n) for n, piece in enumerate(X)]

print("Training")
trainCLF(X, y, True, "restsClassifierAlt")