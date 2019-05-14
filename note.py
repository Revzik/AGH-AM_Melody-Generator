import random


def getSemitones(pitch):
    """
    Convert chromatic steps into semitones

    :param pitch: chromatic steps (35 is c 1 line)
    :return: number of semitones (60 is c 1 line)
    """

    tone = pitch % 7
    octave = int(pitch / 7)
    if tone < 3:
        return octave * 12 + tone * 2
    else:
        return octave * 12 + tone * 2 - 1


def getTones(interval):
    """
    Convert interval in semitones (0 - 12) to chromatic steps

    :param interval: interval in semitones (0 - 12)
    :return: chromatic steps
    """

    if interval == 6:
        if 0.5 > random.uniform(0, 1):
            return 4
        else:
            return 3
    elif interval < 2:
        return interval
    elif interval < 4:
        return interval - 1
    elif interval < 6:
        return interval - 2
    elif interval < 9:
        return interval - 3
    elif interval < 11:
        return interval - 4
    else:
        return interval - 5


def getPitch(semitones):
    """
    Convert semitones into chromatic steps

    :param semitones: number of semitones (60 is c 1 line)
    :return: chromatic steps (35 is c 1 line)
    """

    return int(semitones / 12) * 7 + getTones(semitones % 12)


class Note:
    def __init__(self, semitones=0, value=4, pause=False):
        """
        Class representing note

        :param semitones: number of semitones (like midi but 60 is c 1 line)
        :param value: value of the note in number of sixteenths
        :param pause: should be a pause

        :att semitones: like above
        :att pitch: number of chromatic steps
        :att tone: note represented by a number (0 - 7)
        :att octave: note's octave (5 is 1 line)
        :att value: like above
        :att pause: like above
        """

        self.semitones = semitones
        self.pitch = getPitch(semitones)
        self.tone = self.pitch % 7
        self.octave = int(self.pitch / 7)
        self.accidental = semitones - getSemitones(self.pitch)
        self.value = value
        self.pause = pause

    def setAccidental(self, accidental):
        """
        Change note's accidental and if essential perform enharmonic change

        :param accidental: accidental's number of semitones
        """

        self.accidental = accidental
        self.semitones += accidental
        if self.accidental > 2 or self.accidental < -2:
            self.pitch = getPitch(self.semitones)
            self.tone = self.pitch % 7
            self.octave = int(self.pitch / 7)
            self.accidental = 0
            self.accidental = self.semitones - getSemitones(self.pitch)

    def getInterval(self, note):
        """
        :param note: note to calculate the interval between
        :return: interval between notes
        """
        return note.semitones - self.semitones

    def translate(self):
        """
        Translate the object into lilypond note
        order: tone -> accidental -> octave -> value

        :return: string containing lilypond note
        """
        note = ""

        # adding tone
        if self.pause:
            note = note + "r"
        else:
            if self.tone == 0:
                note = note + "c"
            elif self.tone == 1:
                note = note + "d"
            elif self.tone == 2:
                note = note + "e"
            elif self.tone == 3:
                note = note + "f"
            elif self.tone == 4:
                note = note + "g"
            elif self.tone == 5:
                note = note + "a"
            elif self.tone == 6:
                note = note + "b"

        # adding accidentals
        if not self.pause:
            if self.accidental == 2:
                note = note + "isis"
            elif self.accidental == 1:
                note = note + "is"
            elif self.accidental == -1:
                note = note + "es"
            elif self.accidental == -2:
                note = note + "eses"

        # adding octave
        if not self.pause:
            if self.octave == 0:
                note = note + ",,,,"
            elif self.octave == 1:
                note = note + ",,,"
            elif self.octave == 2:
                note = note + ",,"
            elif self.octave == 3:
                note = note + ","
            elif self.octave == 5:
                note = note + "'"
            elif self.octave == 6:
                note = note + "''"
            elif self.octave == 7:
                note = note + "'''"
            elif self.octave == 8:
                note = note + "''''"
            elif self.octave == 9:
                note = note + "'''''"
            elif self.octave == 10:
                note = note + "''''''"

        # adding rythmic value
        if self.value == 1:
            note = note + "16"
        elif self.value == 2:
            note = note + "8"
        elif self.value == 3:
            note = note + "8."
        elif self.value == 4:
            note = note + "4"
        elif self.value == 5:
            note = note + "4~ " + note + "16"
        elif self.value == 6:
            note = note + "4."
        elif self.value == 7:
            note = note + "4~ " + note + "8~ " + note + "16"
        elif self.value == 8:
            note = note + "2"
        elif self.value == 9:
            note = note + "2~ " + note + "16"
        elif self.value == 10:
            note = note + "2~ " + note + "8"
        elif self.value == 11:
            note = note + "2~ " + note + "8~ " + note + "16"
        elif self.value == 12:
            note = note + "2."
        elif self.value == 13:
            note = note + "2~ " + note + "4~ " + note + "16"
        elif self.value == 14:
            note = note + "2~ " + note + "4~ " + note + "8"
        elif self.value == 14:
            note = note + "2~ " + note + "4~ " + note + "8~ " + note + "16"
        elif self.value == 16:
            note = note + "1"

        return note + " "
