#!/usr/bin/python

import argparse
import music21
import bachChorales
from model import *
import random

def main():
  parser = argparse.ArgumentParser(description='Generate melodies.')
  parser.add_argument('-t', '--test', help='test model')
  parser.add_argument('-d', '--debug', help='debug model')
  parser.add_argument('-m', '--model', nargs=1, default='one',
                    help='specify the model type')

  args = parser.parse_args()
  
  if args.model == 'basic':
    modelCreator = BasicModelCreator()
  else:
    modelCreator = ModelCreator()

  if args.debug:
    debugTest(modelCreator)
  elif args.test:
    fullTest(modelCreator)
  else:
    model = generateModel(modelCreator)
    generateSong(model)

def fullTest(modelCreator):
  print "loading corpus..."
  corpus = bachChorales.getMelodiesFromPickle()

  print "testing..."
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
  print "generating song..."
  generator = Generator(model, seed)
  generator.setNextNote(Note.startOfSong)

  song = music21.stream.Stream()
  while True:
    nextNote = generator.generateNextNote()
    if nextNote == Note.endOfSong:
      break
    song.append(nextNote)
#  song.show('text')
  song.show('musicxml')

def generateModel(modelCreator):
  print "loading corpus..."
  corpus = bachChorales.getMelodiesFromPickle()

  print "creating model..."
  corpus = modelCreator.normalizeCorpus(corpus)
  model = modelCreator.createModel(corpus)
  return model

if __name__ == "__main__":
  main()
