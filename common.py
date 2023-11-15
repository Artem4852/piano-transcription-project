import numpy as np
import os, joblib, pickle
from sklearn.ensemble import RandomForestClassifier
from addons.features import extractFeatures
from addons.sheet import labelData, extractData, key

def saveData(data, filename):
  os.makedirs("models/data", exist_ok=True)
  with open(filename, 'wb') as f:
    pickle.dump(data, f)

def loadData(filename):
  with open(filename, 'rb') as f:
    return pickle.load(f)

def saveModel(model, filename):
  joblib.dump(model, f"models/{filename}.pkl")

def loadModel(filename):
  return joblib.load(f"models/{filename}.pkl")

def getTrainingFiles(dotted=False, allpitches=False, spaces=False, combinations=False):
  return [f.split('.')[0] for f in os.listdir("media/training") if "wav" in f and (not "allpitches2" in f or allpitches) and (not "dotted" in f.lower() or dotted) and (not "spaces" in f.lower() or spaces) and (not "combinations" in f.lower() or combinations)]

def getTrainingData(filename, mode=0, training=True, tempFolder="notesTemp"):
  X, yp, yl, yr = [], [], [], []
  pitchLabels, lengthLabels, restsLabels = labelData(f"media/{'training' if training else 'testing'}/{filename}.mxl")
  notes, _ = extractFeatures(f"media/{'training' if training else 'testing'}/{filename}.wav", tempFolder)
  for n, note in enumerate(notes):
    X.append(note)
    yp.append(pitchLabels[n])
    yl.append(lengthLabels[n])
    yr.append(restsLabels[n])
  
  return X, yp, yl, yr

def trainCLF(X, y, save=True, filename="classifier"):
  X = np.array(X); y = np.array(y)
  classifier = RandomForestClassifier()
  classifier.fit(X, y)
  if save: saveModel(classifier, filename)
  return classifier

def fixLengthPredictions(predictions):
  key = [0.25, 0.5, 1.0, 2.0, 4.0]
  lengthPredData = [key[int(str(x if x not in [0, 1] else "0"+str(x))[:-1])] * (1.5 if int(str(x)[-1]) else 1) for x in predictions]

  total = 0
  perfectuntil = 0
  measure = 2
  for n, note in enumerate(lengthPredData):
    total += note
    if total == 4.0: total, perfectuntil, measure = 0, n, measure+1
    elif total > 4: 
      if n == len(lengthPredData)-1: break
      print(f"Likely an error begins before/at note {n} on measure {measure} with length {note}. Total is {total}")
      for j, note in enumerate(lengthPredData[perfectuntil:n]):
        if total - note/3 != 4.0: 
          continue
        print(f"Error caused by note {j} on measure {measure} with lengths {note}\nThe index of the note in the pred data is {j+perfectuntil}")
        lengthPredData[j+perfectuntil] = note/1.5
        total, perfectuntil, measure = 0, n, measure+1
  
  return [int((str(key.index(pred))+"0") if pred in key else (str(key.index(pred/1.5)) + "1")) for pred in lengthPredData]