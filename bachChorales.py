from music21 import *
import util

melodies = []
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
    music21TimeSignature = stream.flat.getElementsByClass(meter.TimeSignature)
    return music21TimeSignature

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

def loadMelodies():
    """
    Loads the melodies from BWV 250-438, minus a few
    For some reason, chorales 274, 275, and 409 are 
    missing from the corpus, hence the need for multiple loops
    """
    """
    for i in range(250, 274):
        chorale = corpus.parse('bach/bwv' + str(i))
        melody = chorale.getElementById('Soprano')
        if melody != None:
            melodies.append(melody)
        else:
            melodies.append(chorale.getElementById('S.'))
    """
    for i in range(278, 409):
        chorale = corpus.parse('bach/bwv' + str(i))
        melody = chorale.getElementById('Soprano')
        if melody != None:
            melodies.append(melody)
            continue
        melody = chorale.getElementById('S.')
        if melody != None:
            melodies.append(melody)
            continue
        melody = chorale.getElementsByClass(stream.Part)[0]
        melodies.append(melody)
        
    for i in range(410, 439):
        chorale = corpus.parse('bach/bwv' + str(i))
        melodies.append(chorale.getElementById('Soprano'))

def run():
    #loadMelodies()
    chorale = corpus.parse('bach/bwv250')
    melody = chorale.getElementsByClass(stream.Part)[0]
    melody.show('musicxml')
    melody.show('text')
    #getKey(chorale)
    #print 'There are ' + str(len(melodies)) + ' melodies ready for use!\n'   
    # If you set up your music21 environment correctly, you can see that the first melody is the soprano part from BWV 250.
    # melodies[0].show('musicxml')
    # i = 0
    
    #while (i < len(melodies)):
    #    print i, getKey(melodies[i])
    #    i += 1
    #print getScaleDegree(getKey(melodies[0]), note.Note('C4'))
    
run()
