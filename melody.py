import random
from note import Note, getTones, getSemitones

class MelodyGenerator:
    def __init__(self, bars, metrum, lowest, highest, first, last,
                 restProb, valueProb, intervalWeight, semitoneWeight, intervalToSemitoneRatio):
        """
        :param bars: number of bars to be generated
        :param metrum: metrum /4
        :param lowest: lowest note in ambitus
        :param highest: highest note in ambitus
        :param first: first note height (-1 for random)
        :param last: last note height (-1 for random)
        :param restProb: probability of a rest (0 - 1)
        :param valueProb: probabilities of each note in a bar (0 - 1)
        :param intervalWeight: weight of each interval occurring
        :param semitoneWeight: weight of each semitone (note) occurring
        :param intervalToSemitoneRatio: bigger value for more interval based genereting, less for semitone based (0 - 1)
        """

        self.bars = bars
        self.metrum = metrum
        self.lowest = lowest
        self.highest = highest
        self.first = first
        self.last = last
        self.restProb = restProb
        self.valueProb = valueProb
        self.intervalWeight = intervalWeight
        self.semitoneWeight = semitoneWeight
        self.intervalToSemitoneRatio = intervalToSemitoneRatio
        self.prevNote = None
        self.currentBar = 0
        self.extendPrevious = False
        self.extendedPrevious = False

    def getBar(self):
        """
        Generate next bar of the song

        :return: list of notes within a bar
        """

        self.currentBar += 1
        points = []
        values = []

        # choosing places for notes
        for i in range(self.metrum * 4):
            if self.valueProb[i] >= random.uniform(0, 1):
                points.append(i)

        # calculating values
        if points[0] != 0:
            values.append(points[0])
            self.extendPrevious = True
            self.extendedPrevious = True

        for i in range(len(points) - 1):
            values.append(points[i + 1] - points[i])
        values.append(self.metrum * 4 - points[len(points) - 1])

        # generate heights for each note
        notes = []
        for value in values:

            # see if a note should be a rest
            if self.restProb > random.uniform(0, 1):
                pause = Note(0, value, True)
                notes.append(pause)
            else:
                note = None

                # generating first note
                if self.prevNote is None:
                    if self.first == -1:
                        note = Note(random.randint(self.lowest, self.highest), value)
                    else:
                        note = Note(self.first, value)

                # stretching the note from previous bar
                elif self.extendPrevious:
                    note = Note(self.prevNote.semitones, value)
                    self.extendPrevious = False

                # generating consecutive note so it fits chosen ambitus
                else:
                    while True:

                        # generate based on intervals
                        if self.intervalToSemitoneRatio > random.uniform(0, 1):
                            interval = random.choices(range(13), self.intervalWeight)[0]
                            toneDiff = getTones(interval)
                            if 0.5 > random.uniform(0, 1):
                                toneDiff *= -1
                                interval *= -1
                            pitch = self.prevNote.pitch + toneDiff
                            note = Note(getSemitones(pitch), value)
                            note.setAccidental(interval - self.prevNote.getInterval(note))

                        # generate based on semitones
                        else:
                            octave = self.prevNote.octave
                            semitones = random.choices(range(12), self.semitoneWeight)[0]
                            note = Note(octave * 12 + semitones, value)

                        # check if note is in ambitus
                        if note.semitones >= self.lowest and note.semitones <= self.highest:
                            break

                notes.append(note)
                self.prevNote = note

        # setting the last note
        if self.last != -1 and self.currentBar == self.bars:
            lastVal = notes[-1].value
            notes[-1] = Note(self.last, lastVal)

        return notes
