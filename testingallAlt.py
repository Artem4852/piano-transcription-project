from common import getTrainingData, loadModel, padRms, padAmplitude, np, fixLengthPredictions
from addons.sheet import extractData
from sklearn.metrics import accuracy_score

pitchClf = loadModel("pitchClassifier")
lengthClf = loadModel("lengthClassifierNew")
restsClf = loadModel("restsClassifierAlt")

for i in range(4):
  filename = f"resttest{i+1}"
  # filename = f"test"
  X, pitchY, lengthY, restsY = getTrainingData(filename, training=False)

  pitchX = [([note["pitch"], np.max(note["harmonic"]), np.mean(note["harmonic"]), np.max(note["spectrogram"]), np.mean(note["spectrogram"])]) for note in X]
  lengthX = [[note["pitch"], np.max(note["harmonic"]), len(note["harmonic"].flatten().tolist()), note["spectrogramLength"]] for note in X]
  restsX = [[note["pitch"]] + padRms(note["rms"]) for note in X]
  # restsX = [[note["pitch"]] + padRms(note["rms"]) + padAmplitude(note["amplitude"]) for note in X]

  predictionsPitch = pitchClf.predict(pitchX)
  predictionsLength = lengthClf.predict(lengthX)
  predictionsRests = restsClf.predict(restsX)

  # predictionsLength = fixLengthPredictions(predictionsLength, predictionsRests)
  # print(predictionsLength)

  print(f"Predictions for {filename}:")
  print(list(predictionsPitch))
  print(list(predictionsLength))
  print(list(predictionsRests))
  print(f"Accuracy score pitch: {round(accuracy_score(pitchY, predictionsPitch)*100, 2)}%")
  print(f"Accuracy score length: {round(accuracy_score(lengthY[:-1], predictionsLength[:-1]-predictionsRests[:-1])*100, 2)}%")
  print(f"Accuracy score rests: {round(accuracy_score(restsY, predictionsRests)*100, 2)}%")
  print()

  extractData(predictionsPitch, predictionsLength, predictionsRests, "media/results/"+filename+"results")