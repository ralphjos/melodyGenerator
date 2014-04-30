from music21 import *
import util

melodies = []

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


def getScaleDegree(pitchAndMode, note):
    """
    Given a note and a pitchAndMode, return the scale degree of the note.
    """
    pi = pitchAndMode[0]
    mode = pitchAndMode[1]
    ref_scale = None
    if pitchAndMode[1] == "major":
        ref_scale = scale.MinorScale(pi)
    else:
        ref_scale = scale.MinorScale(pi)
    degree = ref_scale.getScaleDegreeAndAccidentalFromPitch(pitch.Pitch(note.name))
    return degree
    
    

def loadMelodies():
    """
    Loads the melodies from BWV 250-438, minus a few
    For some reason, chorales 274, 275, and 409 are 
    missing from the corpus, hence the need for multiple loops
    """
    for i in range(250, 251):
        chorale = corpus.parse('bach/bwv' + str(i))
        melodies.append(chorale.getElementById('Soprano')) 
    """
    for i in range(276, 409):
        chorale = corpus.parse('bach/bwv' + str(i))
        melodies.append(chorale.getElementById('Soprano'))
        
    for i in range(410, 439):
        chorale = corpus.parse('bach/bwv' + str(i))
        melodies.append(chorale.getElementById('Soprano'))
    """

def run():
    loadMelodies()
    print 'There are ' + str(len(melodies)) + ' melodies ready for use!\n'   
    # If you set up your music21 environment correctly, you can see that the first melody is the soprano part from BWV 250.
    # melodies[0].show('musicxml')
    melodies[0].show('text')
    print getScaleDegree(getKey(melodies[0]), note.Note(''))
    
run()
