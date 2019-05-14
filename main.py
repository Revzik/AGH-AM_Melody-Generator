# Melody Generator for Lilypond
#
# by Bartłomiej Piekarz

from melody import MelodyGenerator
from note import *
import lyTranslator

DEBUG = False

if __name__ == "__main__":
    if DEBUG:
        print("--- DEBUG ---")
    else:
        f = open("score.ly", "w+")
        mel = MelodyGenerator(32,       # bars
                              4,        # metrum /4
                              60,       # lowest
                              84,       # highest
                              -1,       # first (-1 for random)
                              -1,       # last (-1 for random)
                              0.03,     # rest probability
                              [0.95, 0.1, 0.3, 0.1,
                               0.7, 0.1, 0.3, 0.1,
                               0.9, 0.1, 0.3, 0.1,
                               0.7, 0.1, 0.3, 0.1],     # note probability (has to be at least 4 * metrum)
                              # 1,  2m,  2w,  3m,  3w,   4, 4zw,   5,  6m,  6w,  7m,  7w,   8   interval weights
                              [20,   1,  20,   1,  20,  20,   1,  20,   1,  20,   1,  20,  20],
                              # c, c#,  d, d#,  e,  f, f#,  g, g#,  a, a#,  h   note (in semitones) weights
                              [1,   0,  1,  0,  1,  1,  0,  1,  0,  1,  0,  1],
                              0.3)    # ratio between interval and semitones generation (less = more based on semitones)
        transpose = 'c'     # key for the song to be transposed to

        f.write(lyTranslator.init())
        f.write(lyTranslator.startSection(mel.metrum, transpose))

        score = ""
        for i in range(mel.bars):
            if mel.extendedPrevious and mel.prevNote is not None:
                score = score[:-1] + "~ "
                mel.extendedPrevious = False
            score = score + "\n\t\t"
            for note in mel.getBar():
                score = score + note.translate()
        f.write(score)

        f.write(lyTranslator.endSection())
