from line import *
import math

class CanonicalLine(Line):

    spokenText = None
    freeTranslation = None

    def __init__(self, doc, lineNumber):
        Line.__init__(self, doc, lineNumber)
        self.deduceStructure()
        self.parseWordsCalculateSpacing()

    def deduceStructure(self):
        tbl = self.tbl
        self.spokenTextRow = tbl[tbl["START"] >= 0].index.tolist()[0]; # always 0?
        self.rootID = tbl.ix[self.spokenTextRow, "ANNOTATION_ID"]
        tierBackPointers = tbl['ANNOTATION_REF'].tolist()[1:4]  # drop the leading nan
        spokenTextBackPointer = [value for value in tierBackPointers if value != self.rootID]
        self.wordRow = tbl.loc[tbl["ANNOTATION_ID"] == spokenTextBackPointer[0]].index.tolist()[0]
        self.glossRow = tbl.loc[tbl["ANNOTATION_REF"] == spokenTextBackPointer[0]].index.tolist()[0]
           # just one row left: it must be the freeTranslation row
        enumeratedRows = set([self.spokenTextRow, self.wordRow, self.glossRow])
        self.freeTranslationRow = list(set(range(4)).difference(enumeratedRows))[0]


    def show(self):
        print("--- CanonicalLine")
        print(self.getTable())


    def parseWordsCalculateSpacing(self):

        """
          the word tier: direct child of root, is parent to another tier (the gloss tier)
          gloss line: the only grandchild line among the four
          gloss line: the only row with ANNOTATION_REF neither NaN nor rootID
        """
        tbl = self.getTable()
        #rootID = self.deduceSpokenTextID()
        #tierBackPointers = tbl['ANNOTATION_REF'].tolist()[1:4]  # drop the leading nan
        #spokenTextBackPointer = [value for value in tierBackPointers if value != rootID]

        wordRawText = tbl.loc[self.wordRow, "TEXT"]
        glossRawText = tbl.loc[self.glossRow, "TEXT"]
        #wordRawText = tbl.loc[tbl["ANNOTATION_ID"] == spokenTextBackPointer[0]]["TEXT"].tolist()[0]
        #glossRawText = tbl.loc[tbl["ANNOTATION_REF"] == spokenTextBackPointer[0]]["TEXT"].tolist()[0]

        self.words = wordRawText.split("\t")
        self.glosses = glossRawText.split("\t")
        assert(len(self.words) == len(self.glosses))
        self.wordSpacing = []

        for i in range(len(self.words)):
            wordSize = len(self.words[i])
            glossSize = len(self.glosses[i])
            self.wordSpacing.append(max(wordSize, glossSize) + 1)

    def toHtml(self, htmlDoc):

        with htmlDoc.tag("div", klass="line-content"):
            with htmlDoc.tag("div", klass="line"):
                styleString = "grid-template-columns: %s;" % ''.join(["%dch " % p for p in self.wordSpacing])
                with htmlDoc.tag("div", klass="speech-tier"):
                    htmlDoc.text(self.getTable()['TEXT'][self.spokenTextRow])
                    with htmlDoc.tag("div", klass="phoneme-tier", style=styleString):
                        for word in self.words:
                           with htmlDoc.tag("div", klass="phoneme-cell"):
                              htmlDoc.text(word)
                    with htmlDoc.tag("div", klass="phoneme-tier", style=styleString):
                       for gloss in self.glosses:
                         with htmlDoc.tag("div", klass="phoneme-cell"):
                              htmlDoc.text(gloss)
                    with htmlDoc.tag("div", klass="freeTranslation-tier"):
                        htmlDoc.text(self.getTable()['TEXT'][self.freeTranslationRow])


