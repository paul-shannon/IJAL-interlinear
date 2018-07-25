from line import *

class DegenerateLine(Line):

    spokenText = None
    freeTranslation = None

    def __init__(self, doc, lineNumber):
        Line.__init__(self, doc, lineNumber)

    def show(self):
        print("i am a degenerate line")
        print(self.getTable())

    def toHtml(self, htmlDoc):
        with htmlDoc.tag("div", klass="line-content"):
            with htmlDoc.tag("div", klass="speech-tier"):
                htmlDoc.text(self.getTable()['TEXT'][0])
            with htmlDoc.tag("div", klass="freeTranslation-tier"):
                htmlDoc.text(self.getTable()['TEXT'][1])




