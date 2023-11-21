import music21
from music21 import stream
import random

# octaves = [3, 4, 4, 5, 5, 6]
octaves = [3, 4, 5, 6]
notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
# notes = ['C', 'C', 'C#', 'D', 'D', 'D#', 'E', 'E', 'F', 'F', 'F#', 'G',  'G', 'G#', 'A',  'A', 'A#', 'B', 'B']
standardLengths = [0.25, 0.5, 1, 2, 4]
lengths = [[1.5], [1.5, 0.25], [2], [2, 0.25], [2, 0.5], [2, 0.75], [3]]
# lengths = [[0.25], [0.5], [0.75], [1], [1, 0.25], [1.5], [1.5, 0.25], [2], [2, 0.25], [2, 0.5], [2, 0.75], [3], [3, 0.25], [3, 0.5], [3, 0.75], [4]]
restlengths = [0, 0, 0.25, 0.5, 1, 2, 4]

allPitches = [note+str(octave) for octave in octaves for note in notes]

s = stream.Stream()
s.append(music21.note.Rest(length=4))
# for noteBefore in allPitches:
#   for noteAfter in allPitches:
#     n1 = music21.note.Note(noteBefore, quarterLength=2.0)
#     n2 = music21.note.Note(noteAfter, quarterLength=2.0)
#     s.append(n1)
#     s.append(n2)

# n = 0
# for _ in range(124):
#   if n == 4: n = 0
#   note = music21.note.Note(random.choice(allPitches))
#   note.duration.quarterLength = random.choice(length)
#   while n + note.duration.quarterLength > 4:
#     note.duration.quarterLength = random.choice(length)
#   n+=note.duration.quarterLength
#   if note.duration.quarterLength != 0: s.append(note)
#   restdur = random.choice(restlength)
#   while n + restdur > 4:
#     restdur = random.choice(restlength)
#   n+=restdur
#   if restdur == 0: continue
#   s.append(music21.note.Rest(restdur))

# generating training file for length model
for lengthGroup in lengths:
  for note in allPitches:
    n = music21.note.Note(note)
    n.duration.quarterLength = 4+lengthGroup[-1]
    if len(lengthGroup) != 1:
      additional = music21.note.Note(note, quarterLength=lengthGroup[0])
      additional.tie = music21.tie.Tie('start')
      s.append(additional)
    s.append(n)

s.write('musicxml', 'media/training/allLengthsAdditional.mxl')