from common import getTrainingData, loadModel, np, fixLengthPredictions
from addons.sheet import extractData
from sklearn.metrics import accuracy_score

pitchClf = loadModel("pitchClassifier")
lengthClf = loadModel("lengthClassifier")

for i in range(4):
  filename = f"lengthtest{i+1}"
  # filename = f"test"
  X, pitchY, lengthY, _ = getTrainingData(filename, training=False)

  pitchX = [([note["pitch"], np.max(note["harmonic"]), np.mean(note["harmonic"]), np.max(note["spectrogram"]), np.mean(note["spectrogram"])]) for note in X]
  lengthX = [[note["pitch"], np.max(note["harmonic"]), len(note["harmonic"].flatten().tolist()), note["spectrogramLength"]] for note in X]

  predictionsPitch = pitchClf.predict(pitchX)
  predictionsLength = lengthClf.predict(lengthX)

  predictionsLength = fixLengthPredictions(predictionsLength)

  print(f"Predictions for {filename}:")
  print(list(predictionsPitch))
  print(list(predictionsLength))
  print(f"Accuracy score pitch: {round(accuracy_score(pitchY, predictionsPitch)*100, 2)}%")
  print(f"Accuracy score length: {round(accuracy_score(lengthY[:-1], predictionsLength[:-1])*100, 2)}%")
  print()

  extractData(predictionsPitch, predictionsLength, None, "media/results/"+filename+"results")