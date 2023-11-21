from common import getTrainingData, loadModel, padRms, np, fixLengthPredictions
from addons.sheet import extractData
from sklearn.metrics import accuracy_score

pitchClf = loadModel("pitchClassifier")
lengthClf = loadModel("lengthClassifierNewNew")
restsClf = loadModel("restsClassifierAlt")

for i in range(4):
  filename = f"resttest{i+1}"
  # filename = f"test"
  X, pitchY, lengthY, restsY = getTrainingData(filename, training=False)

  pitchX = [([note["pitch"], np.max(note["harmonic"]), np.mean(note["harmonic"]), np.max(note["spectrogram"]), np.mean(note["spectrogram"])]) for note in X]
  lengthX = [[note["pitch"], len(note["harmonic"].flatten().tolist()), note["spectrogramLength"], note["spectrogramLength"], note["spectrogramLength"], note["spectrogramLength"]] for note in X]
  restsX = [[note["pitch"]] + padRms(note["rms"]) for note in X]

  predictionsPitch = pitchClf.predict(pitchX)
  predictionsLength = lengthClf.predict(lengthX)
  predictionsRests = restsClf.predict(restsX)

  # predictionsLength = fixLengthPredictions(predictionsLength, predictionsRests)
  # print(predictionsLength)

  print(f"Predictions for {filename}:")
  print(list(predictionsPitch))
  print(list(predictionsLength))
  print([int(p) for p in lengthY])
  print(np.array(lengthX)[:, -1].tolist())
  print(list(predictionsRests))
  print(f"Accuracy score pitch: {round(accuracy_score(pitchY, predictionsPitch)*100, 2)}%")
  print(f"Accuracy score length: {round(accuracy_score(lengthY[:-1], predictionsLength[:-1])*100, 2)}%")
  print(f"Accuracy score rests: {round(accuracy_score(restsY[:-1], predictionsRests[:-1])*100, 2)}%")
  print()

  mask = lengthY[:-1] != predictionsLength[:-1]
  print(np.array(lengthY)[:-1][mask], predictionsLength[:-1][mask])

  extractData(predictionsPitch, predictionsLength, predictionsRests, "media/results/"+filename+"results")