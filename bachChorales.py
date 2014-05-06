from music21 import *
import util
import model

melodies = []
BWVNumbers = [250, 251, 252, 253, 255, 260, 262, 263, 264, 267, 268, 271, 284, \
              287, 290, 292, 293, 294, 296, 298, 302, 303, 307, 308, 317, 318, \
              322, 325, 329, 332, 336, 339, 340, 346, 347, 348, 355, 359, 360, \
              361, 365, 367, 370, 371, 373, 375, 376, 377, 378, 379, 380, 384, \
              385, 386, 387, 388, 389, 392, 393, 394, 395, 397, 398, 401, 402, \
              407, 411, 414, 415, 422, 426, 427, 428, 429, 430, 431, 432, 433, \
              436, 438]
threeFour = 0
fourFour = 0
twoTwo = 0
twoFour = 0

def getKey(stream):
    """
    Input: any music21 Stream (a Score, Part, Measure, etc.)
    Output: a tuple representing the key of the Stream
            For example, if the key is A minor, the return value 
            will be ('A', 'minor')
    """
    music21KeySignature = stream.flat.getElementsByClass(key.KeySignature)
    if len(music21KeySignature.elements) == 0:
        return None
    elif len(music21KeySignature.elements) >= 2:
        print "More than two keys detected.\n"
    pitchAndMode = music21KeySignature.elements[0].pitchAndMode
    return pitchAndMode

def getTimeSignature(stream):
    timeSignatures = stream.flat.getElementsByClass(meter.TimeSignature)
    if len(timeSignatures) != 1:
        return len(timeSignatures)
    return timeSignatures[0]

def getScaleDegree(pitchAndMode, note):
    """
    Given a note and a pitchAndMode, return the scale degree of the note.
    """
    pi = pitchAndMode[0]
    mode = pitchAndMode[1]
    ref_scale = None
    if pitchAndMode[1] == "major":
        ref_scale = scale.MajorScale(pi)
    else:
        ref_scale = scale.MinorScale(pi)
    degree = ref_scale.getScaleDegreeAndAccidentalFromPitch(pitch.Pitch(note.name))
    return degree

def getFromCorpus(i):
    chorale = corpus.parse('bach/bwv' + str(i))
    melody = chorale.getElementById('Soprano')
    if melody != None:
        if getTimeSignature(melody).ratioString == "4/4" and getKey(melody)[1] == "major":
            melodies.append(melody)
            return
    melody = chorale.getElementById('S.')
    if melody != None:
        if getTimeSignature(melody).ratioString == "4/4" and getKey(melody)[1] == "major":
            melodies.append(melody)
            return
    melody = chorale.getElementsByClass(stream.Part)[0]
    if getTimeSignature(melody).ratioString == "4/4" and getKey(melody)[1] == "major":
        melodies.append(melody)
        return
        
def loadMelodies():
    """
    Loads the melodies from BWV 250-438, minus a few
    For some reason, chorales 274, 275, and 409 are 
    missing from the corpus, hence the need for multiple loops
    """
    for i in BWVNumbers:
        getFromCorpus(i)
    """
    for i in range(250, 274):
        getFromCorpus(i)
    for i in range (278, 281):
        getFromCorpus(i)
    for i in range (282, 304):
        getFromCorpus(i)    
    for i in range (305, 362):
        getFromCorpus(i)
    for i in range (363, 366):
        getFromCorpus(i)
    for i in range (367, 409): 
        getFromCorpus(i)   
    for i in range(410, 439):
        getFromCorpus(i)
    """
    return melodies

def run():
    def showChorale(i):
        chorale = corpus.parse('bach/bwv' + str(i))
        chorale.show('musicxml')
        chorale.show('text')
    loadMelodies()
    """
    loadMelodies()
    i = 0
    while (i < len(melodies)):
        print i, getKey(melodies[i]), getTimeSignature(melodies[i]), "\n" 
        i += 1
    """
    """
    getFromCorpus(307)
    melodies[0].show('musicxml')
    """
    """
    noteList = melodies[0].flat.getElementsByClass(note.Note)
    print len(noteList)
    for each in noteList:
        print each
    melodies[0].show('musicxml')
    """
    #print len(melodies)
    #melodies[49].show('musicxml')
    #melodies[107].show('musicxml')
