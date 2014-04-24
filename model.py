class Model:
  def getNextNoteDistribution(self, evidence):
    """
    Returns a probability distribution for the next note,
    based on the evidence 
    """
    raiseNotDefined()

class ModelCreator:
  def createModel(self, corpus):
    """
    Creates and returns a model, given a corpus.
    """
    raiseNotDefined()

class Predictor:
  """
  Predicts next note, based on previous notes.
  """

  def __init__(self, model):
    self.model = model
    #TODO: Set this to start of song, start of phrase
    self.state = None

  def setState(self, state):
    """
    Sets the state for the predictor (for example, all previous notes).
    """
    raiseNotDefined()

  def predictNextNote(self):
    """
    Predicts and returns the next note.
    """
    raiseNotDefined()

  def getNextNoteDistribution(self):
    raiseNotDefined()

  def setNextNote(self, note):
    """
    Adds the next note to the state.
    """
    raiseNotDefined()

def Generator(Predictor):
  """
  "Predicts" the next note based on probability distribution.
  """

