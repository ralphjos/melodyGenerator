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
  def createModel(self, corpus, laplace = 0):
    """
    Creates and returns a model, given a corpus.
    
    Assumes that each song in the corpus contains at least one note.
    """
    noteDists = collections.defaultdict(Counter)
    # Go through each song, adding to the count for P(next note|note)
    for song in corpus:
      previousNote = None
      for note in song:
        if previousNote is not None:
          noteDists[previousNote][note] += 1
        previousNote = note

    for note in noteDists:
      # Apply Laplace smoothing
      # noteDists[note].incrementAll(Note.allNotes(), laplace)
      # Normalize all the next note distributions
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
    cum_train_error = 0.0
    cum_test_error = 0.0
    for i in range(numFolds):
      (train, test) = self.splitTrainAndTestSets(i)
      model = self.modelCreator.createModel(train, laplace = 1)
      train_error = self.getTrainError(model, train)
      test_error = self.testModel(model, test)[2]
      print i, "Training error:", train_error, "Test error:", test_error
      cum_train_error += train_error
      cum_test_error += test_error
      
    avg_train_error = cum_train_error / numFolds
    avg_test_error = cum_test_error / numFolds
    print "Avg training error:", avg_train_error
    print "Avg testing error:", avg_test_error

  # TODO: Could make this faster by taking error as 1 - max(P(next note|note)) * P(note)?
  def getTrainError(model, trainSet):
    return self.testModel(model, trainSet)[2]

  def testModel(self, model, testSet):
    """
    Tests the model on the testSet.

    Returns the correct_count, incorrect_count, and error.

    Assumes every song has a first note.
    """
    predictor = Predictor(model)
    correct_count = 0
    incorrect_count = 0
    for song in testSet:
      for actual_next_note in song:
        predicted_next_note = predictor.predictNextNote()
        if actual_next_note == predicted_next_note:
          correct_count += 1
        else:
          incorrect_count += 1
    
    total_count = incorrect_count + correct_count
    error = incorrect_count / float(total_count)
    return correct_count, incorrect_count, error

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
