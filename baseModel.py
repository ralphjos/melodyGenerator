class BaseModel(Model):
  def getNextNoteDistribution(self, evidence):
    """
    Returns a probability distribution for the next note,
    based on the evidence 
    """
    raiseNotDefined()

class BaseModelCreator(ModelCreator):
  def createModel(self, corpus):
    """
    Creates and returns a model, given a corpus.
    """
    raiseNotDefined()
