from common import getTrainingData, loadModel, np
from addons.sheet import extractData
from sklearn.metrics import accuracy_score

clf = loadModel("pitchClassifier")

for i in range(4):
  filename = f"pitchtest{i+1}"
  X, y, _, _ = getTrainingData(filename, training=False)
  X = [([note["pitch"], np.max(note["harmonic"]), np.mean(note["harmonic"]), np.max(note["spectrogram"]), np.mean(note["spectrogram"])]) for note in X]

  predictions = clf.predict(X)

  print(f"Predictions for testing file {i+1}:")
  print(predictions)
  print(f"Accuracy score: {round(accuracy_score(y, predictions)*100, 2)}%")
  print()

  extractData(predictions, None, None, "media/results/"+filename+"results")