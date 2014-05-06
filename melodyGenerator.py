import music21
import bachChorales
from model import *

def main():
  modelCreator = ModelCreator()

  corpus = bachChorales.loadMelodies()

  crossValidator = CrossValidator(corpus, modelCreator)
  crossValidator.run()

def test():
  modelCreator = BasicModelCreator()

  corpus = bachChorales.loadOneMelody()
  corpus[0].show()
  corpus = modelCreator.normalizeCorpus(corpus)
  corpus[0].show("text")

  model = modelCreator.createModel(corpus)
  print model.dists

if __name__ == "__main__":
  main()
  # test()
