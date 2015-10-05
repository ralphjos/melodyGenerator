from music21 import *
import glob

def loadCorpus():
  melodies = []
  files = glob.glob("English-corpus/*.corpus.txt")
  for f in files:
    melody = readFile(f)
    if melody:
      melodies.append(melody)
  print "total major melodies: ", len(melodies)
  return melodies

def readFile(fname):
  print fname
  f = open(fname)
  f.readline()

  key = f.readline().split('>')[1][:-5]
  mode = key[-5:]
  tonic = key[:-6]
  if tonic.endswith('b'):
    tonic = tonic[:-1] + '-'
  if mode == 'minor':
    return None

  s1 = stream.Stream()
  for line in f:
    if line.startswith('<token'):
      line = line.split()
      orignote = line[2][10:]
      tone = line[3][5:]
      interval = line[4][9:].split('>')[0]
      s1.append(orignoteToNote(orignote))
  #s1.show()
  if mode == 'major':
    s1 = transposeToC(s1, tonic)
  print tonic, mode
  #s1.show()
  return s1

def intervalToC(pitch):
    """ 
    Given a pitch, determine the minimum number of half steps to C.
    """
    interval = (60 - pitch.midi) % 12
    if interval >= 6:
        interval -= 12
    return interval

def transposeToC(stream, key):
    interval = intervalToC(pitch.Pitch(key))
    rtn = stream.transpose(interval)
    return rtn 

def orignoteToNote(orignote):
  if orignote.endswith("''"):
    octave = '6'
    orignote = orignote[:-2]
  elif orignote.endswith("'"):
    octave = '5'
    orignote = orignote[:-1]
  elif orignote.endswith('--'):
    octave = '2'
    orignote = orignote[:-2]
  elif orignote.endswith('-'):
    octave = '3'
    orignote = orignote[:-1]
  else: octave = '4'
  
  if orignote.endswith('bb'):
    orignote = orignote[:-2] + '--'
  if orignote.endswith('b'):
    orignote = orignote[:-1]
    orignote = orignote + '-'

  #print orignote, octave
  return note.Note(orignote + octave)

if __name__ == "__main__":
  f = 'English-corpus/ALLTHETI.corpus.txt'
  readFile(f)

