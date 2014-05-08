import music21
import bachChorales
from model import *
import argparse

def main():
  parser = argparse.ArgumentParser(description='Generate melodies.')
  parser.add_argument('-t', '--test', action='store_true',
                    help='test model')
  parser.add_argument('-d', '--debug', action='store_true',
                    help='debug model')
  parser.add_argument('-m', '--model', default='one',
                    help='specify the model type')

  args = parser.parse_args()

  if args.model == 'basic':
    print "Model: Basic"
    modelCreator = BasicModelCreator()
  else:
    print "Model: One-step lookahead"
    modelCreator = ModelCreator()

  if args.debug:
    debugTest(modelCreator)
  elif args.test:
    fullTest(modelCreator)
  else:
    model = generateModel(modelCreator)
    generateSong(model)

def fullTest(modelCreator):
  print "Loading corpus..."
  corpus = bachChorales.getMelodiesFromPickle()

  print "Running cross validation..."
  tester = Tester(corpus, modelCreator)
  tester.runCrossValidation()

def debugTest(modelCreator):
  corpus = bachChorales.loadOneMelody()
  # corpus[0].show()
  corpus = modelCreator.normalizeCorpus(corpus)
  # corpus[0].show("text")

  tester = Tester(corpus, modelCreator)

  model = modelCreator.createModel(corpus)
  print model.dists
  print tester.testModel(model, corpus)

def generateSong(model, seed = 0):
  print "Generating song..."
  generator = Generator(model, seed)
  generator.setNextNote(Note.startOfSong)

  song = music21.stream.Stream()
  while True:
    nextNote = generator.generateNextNote()
    if nextNote == Note.endOfSong:
      break
    song.append(nextNote)
  # song.show('text')
  song.show('musicxml')

def generateModel(modelCreator):
  print "Loading corpus..."
  corpus = bachChorales.getMelodiesFromPickle()

  print "Creating model..."
  corpus = modelCreator.normalizeCorpus(corpus)
  model = modelCreator.createModel(corpus)
  return model

if __name__ == "__main__":
  main()
