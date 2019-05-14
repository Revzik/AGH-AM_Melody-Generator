

def init():
    return '\\version "2.18.2"\n\n' \
           '\\paper {\n\t#(set-paper-size "a4")\n}\n\n' \
           '\\layout {\n\tindent = 0\\in\n\tragged-last = ##f\n' \
           '\t\\context {\n\t\t\\Score\n\t}\n}\n\n'


def startSection(metrum, key):
    return '\\transpose c ' + key + ' {\n' \
           '\t\\absolute {\n\t\t\\key c \\major\n\t\t\\time ' + str(metrum) + '/4\n' \
           '\t\t\\override Score.BarNumber.break-visibility = ##(#f #t #t)\n'

def endSection():
    return '\n\t\t\\bar "||"\n\t}\n}'
