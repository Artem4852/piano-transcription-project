import music21
from music21 import converter, stream
import numpy as np

key = {
  "pitch": ["C", "D", "E", "F", "G", "A", "B"],
  "length": [0.25, 0.5, 1.0, 2.0, 4.0]
}

def labelData(filename):
  score = converter.parse(filename)
  scoreInfo = []

  for note in score.flatten().notesAndRests:
    if note.isRest:
      length = float(note.quarterLength)
      scoreInfo.append((0, None, length))
      continue
    pitch = note.pitch.nameWithOctave
    length = float(note.quarterLength)
    scoreInfo.append((1, pitch, length))

  pitchLabels, lengthLabels, restsLabels = [], [], []
  for n, (_type, pitch, length) in enumerate(scoreInfo):
    if _type == 0: continue
    octave = int(pitch[-1])
    note = pitch[0]

    totalRestsLength = 0
    for piece in scoreInfo[n:]:
      if piece[0] == 0:
        totalRestsLength += piece[2]
      else:
        break

    lengthLabel = str(key["length"].index(length) if length in key["length"] else key["length"].index(length/1.5))
    lengthLabel += "0" if length in key["length"] else "1"

    pitchLabels.append(int(f"{octave}{key['pitch'].index(note)}{1 if '#' in pitch else 0}"))
    lengthLabels.append(int(lengthLabel))
    restsLabels.append(totalRestsLength*4)
  
  return pitchLabels, lengthLabels, restsLabels

def extractData(pitchLabels, lengthLabels, restsLabels, filename):
  outputStream = stream.Stream()

  outputStream.append(music21.note.Rest(quarterLength=4.0))

  for n, pitchLabel in enumerate(pitchLabels):
    octave = str(pitchLabel)[0]
    note = key['pitch'][int(str(pitchLabel)[1])]
    sharp = "#" if int(str(pitchLabel)[2]) else ""

    lengthLabel = str(lengthLabels[n]) if lengthLabels[n] >= 10 else "0" + str(lengthLabels[n])
    length = key["length"][int(lengthLabel[0])]
    length *= 1.5 if int(lengthLabel[1]) else 1
    restLength = restsLabels[n]/4 if restsLabels else 0

    newNote = music21.note.Note(f"{note}{sharp}{octave}", quarterLength=length)
    outputStream.append(newNote)

    if restLength != 0: outputStream.append(music21.note.Rest(quarterLength=restLength))
  
  outputStream.write("mxl", fp=filename)