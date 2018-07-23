from line import *

class DegenerateLine(Line):

    spokenText = None
    freeTranslation = None

    def __init__(self, doc, lineNumber):
        Line.__init__(self, doc, lineNumber)

    def show(self):
        print("i am a degenerate line")
        print(self.getTable())



