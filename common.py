import numpy as np
import pandas as pd
import os, joblib, pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from addons.features import extractFeatures
from addons.sheet import labelData, extractData, key

longestSpectrogram = 300
longestHarmonic = 120000
longestAmpl = 200000

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

def getTrainingFiles(dotted=False, allpitches=False, spaces=False, combinations=False, alllengths=False):
  return [f.split('.')[0] for f in os.listdir("media/training") if "wav" in f and (not "allpitches2" in f or allpitches) and (not "dotted" in f.lower() or dotted) and (not "spaces" in f.lower() or spaces) and (not "combinations" in f.lower() or combinations) and (not "alllengths" in f.lower() or alllengths)]

def getTrainingData(filename, mode=0, training=True, tempFolder="notesTemp", predicting=False, lang="eng"):
  X, yp, yl, yr = [], [], [], []
  if not predicting: pitchLabels, lengthLabels, restsLabels = labelData(f"media/{'training' if training else 'testing'}/{filename}.mxl")
  notes, _ = extractFeatures(f"media/{'training' if training else 'testing'}/{filename}.wav" if not predicting else filename+".wav", tempFolder, lang=lang)
  for n, note in enumerate(notes):
    X.append(note)
    if not predicting:
      yp.append(pitchLabels[n])
      yl.append(np.array(lengthLabels[n]) + (np.array(restsLabels[n]) if not training else 0))
      yr.append(restsLabels[n])
  
  return X, yp, yl, yr

def padSpectrogram(spectrogram):
  cols = longestSpectrogram - len(spectrogram[0])
  padWidthSpect = ((0, 0), (0, cols))
  paddedSpect = np.pad(spectrogram, padWidthSpect, mode='constant', constant_values=-100)
  paddedSpect = paddedSpect.flatten().tolist()
  return paddedSpect

def padHarmonic(harmonic):
  cols = longestHarmonic - len(harmonic)
  padWidthHarm = ((0, cols))
  paddedHarm = np.pad(harmonic, padWidthHarm, mode='constant', constant_values=-100).tolist()
  return paddedHarm

def padRms(rms, n=None):
  # pd.DataFrame(rms).T.to_csv(f"rms/{n}.csv", index=False)
  cols = longestSpectrogram - len(rms[0])
  if n: print(f"\033[1APadding note {n} - {cols}")
  padWidthRms = ((0, 0), (0, cols))
  paddedRms = np.pad(rms, padWidthRms, mode='constant', constant_values=-100).tolist()
  return paddedRms[0]

def padAmplitude(amplitude, n=None):
  cols = longestAmpl - len(amplitude)
  # print(f"\033[1APadding note {n} - {cols}")
  padWidthAmpl = ((0, cols))
  paddedAmpl = np.pad(amplitude, padWidthAmpl, mode='constant', constant_values=-100).tolist()
  return paddedAmpl

def trainCLF(X, y, save=True, filename="classifier"):
  X = np.array(X); y = np.array(y)
  model = RandomForestClassifier()
  model.fit(X, y)
  if save: saveModel(model, filename)
  return model

def fixLengthPredictions(predictions, rests):
  key = [0.25, 0.5, 1.0, 2.0, 4.0]
  # lengthPredData = [key[int(str(x if x not in [0, 1] else "0"+str(x))[:-1])] * (1.5 if int(str(x)[-1]) else 1) for x in predictions]
  lengthPredData = [x/4 for x in predictions]
  rests = rests/4
  print(lengthPredData)
  print(rests)

  total = 0
  perfectuntil = 0
  measure = 2
  for n, note in enumerate(lengthPredData):
    total += note
    if total == 4.0: total, perfectuntil, measure = 0, n, measure+1
    elif total > 4 and total - rests[n] > 4: 
      if n == len(lengthPredData)-1: break
      print(f"Likely an error begins before/at note {n} on measure {measure} with length {note}. Total is {total}")
      for j, note in enumerate(lengthPredData[perfectuntil:n]):
        if total - note/3 != 4.0: 
          continue
        print(f"Error caused by note {j} on measure {measure} with lengths {note}\nThe index of the note in the pred data is {j+perfectuntil}")
        lengthPredData[j+perfectuntil] = note/1.5
        total, perfectuntil, measure = 0, n, measure+1
    elif total > 4 and total - rests[n] < 4: total -= 4; perfectuntil = n; measure += 1
    print(n, total, note, rests[n])

  return [int((str(key.index(pred-rests[n]))+"0") if pred-rests[n] in key else (str(key.index((pred-rests[n])/1.5)) + "1")) for n, pred in enumerate(lengthPredData)]

def convertNotes(predictionsPitch, predictionsLength, predictionsRests):
  notes = []
  for n, pred in enumerate(predictionsPitch):
    pitch = f"{key['pitch'][int(str(pred)[1])]}{'#' if int(str(pred)[2]) else ''}{str(pred)[0]}"
    length = predictionsLength[n]-predictionsRests[n]
    if length <= 0: length = predictionsLength[n]
    notes.append({"visual": f"{pitch} {length}", "pitch": pitch, "length": length})
    if predictionsRests[n] != 0 and predictionsLength[n]-predictionsRests[n] > 0: notes.append({"visual": f"Rest {predictionsRests[n]}", "length": predictionsRests[n]})
  return notes