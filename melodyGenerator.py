import music21
import bachChorales
from model import *

def main():
  modelCreator = ModelCreator(Model)

  corpus = bachChorales.getMelodiesFromPickle()

  tester = Tester(corpus, modelCreator)
  tester.runCrossValidation()

def test():
  modelCreator = BasicModelCreator(Model)

  corpus = bachChorales.loadOneMelody()
  # corpus[0].show()
  corpus = modelCreator.normalizeCorpus(corpus)
  # corpus[0].show("text")

  tester = Tester(corpus, modelCreator)

  model = modelCreator.createModel(corpus)
  print model.dists
  print tester.testModel(model, corpus)

if __name__ == "__main__":
  main()
  # test()
