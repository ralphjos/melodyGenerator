import util
import collections

class Model:
  def __init__(self, dists):
    self.dists = dists
  def getNextNoteDistribution(self, evidence):
    """
    Returns a probability distribution for the next note,
    based on the evidence 
    """
    return self.dists[evidence]

class ModelCreator:
  def createModel(self, corpus):
    """
    Creates and returns a model, given a corpus.
    
    Assumes that each song in the corpus contains at least one note.
    """
    noteDists = collections.defaultdict(Counter)
    # Go through each song, adding to the count for P(next note|note)
    for song in corpus:
      note = song.nextNote()
      while song.hasNextNote():
        nextNote = song.nextNote()
        noteDists[note][nextNote] += 1

    # Normalize all the next note distributions
    for note in noteDists:
      noteDists[note].normalize()

    model = Model(noteDists)
    return model

class Predictor:
  """
  Predicts the next note, based on previous notes.

  Usage:
  >>> predictor = Predictor(model)
  >>> nextNote = Note.startOfSongNote()
  >>> while nextNote != Note.endOfSongNote():
  >>>   nextNote = predictor.predictAndSetNextNote()
  """

  def __init__(self, model):
    self.model = model
    self.state = [Note.startOfSongNote()]

  def setState(self, state):
    """
    Sets the state for the predictor (for example, all previous notes).
    """
    self.state = state

  def predictNextNote(self):
    """
    Predicts and returns the next note.
    """
    dist = self.getNextNoteDistribution()
    return dist.argMax()

  def getNextNoteDistribution(self):
    return self.model.getNextNoteDistribution(self.state[-1])

  def setNextNote(self, note):
    """
    Adds the next note to the state.
    """
    self.state.append(note)

  def predictAndSetNextNote(self):
    nextNote = self.predictNextNote()
    self.setNextNote(nextNote)
    return nextNote

class Generator(Predictor):
  """
  Generates new notes from an underlying model.
  """
  def predictNextNote(self):
    dist = self.getNextNoteDistribution()
    return util.sampleFromCounter(dist)

class CrossValidator():
  def __init__(self, corpus, modelCreator, numFolds = 10):
    self.corpus = corpus
    self.modelCreator = modelCreator
    self.numFolds = numFolds

  def run(self):
    for i in range(numFolds):
      (train, test) = self.splitTrainAndTestSets(i)
      model = modelCreator.createModel(train)
      predictor = Predictor(model)
      

  def splitTrainAndTestSets(self, n):
    """
    Splits the corpus into train and test sets by placing every nth
    song in the test set. n should be between 0 and numFolds-1, inclusive.
    """
    train = []
    test = []
    for i in range(len(self.corpus)):
      if i % self.numFolds == n:
        test.append(self.corpus[i])
      else:
        train.append(self.corpus[i])
    return train, test
