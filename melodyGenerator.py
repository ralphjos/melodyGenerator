import music21
import bachChorales
import model

def main():
  corpus = bachChorales.loadMelodies()
  corpus = flattenMelodies(corpus)
  modelCreator = ModelCreator()
  crossValidator = CrossValidator(corpus, modelCreator)
  crossValidator.run()

def flattenMelodies(melodies):
  flattened = []
  for song in melodies:
    flattened.append(song.flat.getElementsByClass(music21.note.Note)) 
  return flattened

if __name__ == "__main__":
  main()
