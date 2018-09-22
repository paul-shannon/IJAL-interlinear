from line import *
import math

class WordsAsElementsLine(Line):

    spokenText = None
    freeTranslation = None

    def __init__(self, doc, lineNumber, grammaticalTerms=[]):
        Line.__init__(self, doc, lineNumber, grammaticalTerms)
        self.deduceStructure()

    def guidedDeduceStructure(self):

    def deduceStructure(self):
        tbl = self.tbl
        #pdb.set_trace()
        self.spokenTextRow = tbl[tbl["START"] >= 0].index.tolist()[0]; # always 0?
        self.rootID = tbl.ix[self.spokenTextRow, "ANNOTATION_ID"]
        allIDs = set(tbl["ANNOTATION_ID"].tolist())
        parentIDs = set(tbl["ANNOTATION_REF"].tolist())

           # the free translation row is a direct child of root, but has no children
           # the remaining direct children of root are the word elements
        directChildrenOfRoot = tbl.loc[tbl["ANNOTATION_REF"] == self.rootID]["ANNOTATION_ID"].tolist()
        tiersWithChildren = tbl["ANNOTATION_REF"].tolist()
        translationRowID_asSet = set(directChildrenOfRoot).difference(set(tiersWithChildren))
        translationRowID = [x for x in translationRowID_asSet][0]
        self.freeTranslationRow = tbl.loc[tbl["ANNOTATION_ID"] == translationRowID].index.tolist()[0]

          # get the ID of the word elements, direct children of root, each with two
          # children: a word and a gloss
        wordIDs = [x for x in set(directChildrenOfRoot).difference(translationRowID_asSet)]
        wordIDs.sort()

          # loop over the wordIDs, assign each pair of children to word and gloss lists respectively
        self.words = []
        self.glosses = []
        for wordID in wordIDs:
           kidIDs = tbl.loc[tbl["ANNOTATION_REF"] == wordID]["ANNOTATION_ID"].tolist()
           self.words.append(tbl.ix[tbl["ANNOTATION_ID"] == kidIDs[0]]["TEXT"].tolist()[0])
           self.glosses.append(tbl.ix[tbl["ANNOTATION_ID"] == kidIDs[1]]["TEXT"].tolist()[0])
        assert(len(self.words) == len(self.glosses))
        print("word count: %d" % len(self.words))
        self.wordSpacing = []

        for i in range(len(self.words)):
            wordSize = len(self.words[i])
            glossSize = len(self.glosses[i])
            self.wordSpacing.append(max(wordSize, glossSize) + 1)

    def identifyStructure(self):
        tbl = self.tbl
        tierClass = ["unknown" for i in range(tbl.shape[0])]
        #pdb.set_trace()
        self.spokenTextRow = tbl[tbl["START"] >= 0].index.tolist()[0]; # always 0?
        self.rootID = tbl.ix[self.spokenTextRow, "ANNOTATION_ID"]
        self.spokenTextID = self.rootID
        tierClass[which(tbl, self.spokenTextID)] = "spokenText"
        allIDs = set(tbl["ANNOTATION_ID"].tolist())
        parentIDs = set(tbl["ANNOTATION_REF"].tolist())
        directChildrenOfRootIDs = set(tbl.loc[tbl["ANNOTATION_REF"] == self.rootID]["ANNOTATION_ID"].tolist())
        self.directChildrenOfRootIDs = sorted(directChildrenOfRootIDs)
           # terminals are the word glosses, elements which are neither parentIDs nor directChildrenOfRoot
        self.morphemeGlossIDs = sorted(allIDs.difference(parentIDs).difference(self.directChildrenOfRootIDs))  # gloss ids
        self.morphemeIDs = tbl.loc[tbl["ANNOTATION_ID"].isin(self.morphemeGlossIDs)]["ANNOTATION_REF"].tolist()
           # the free translation row is a direct child of root, but has no children
           # the remaining direct children of root are the word elements
        directChildrenCount = len(self.directChildrenOfRootIDs)
        pdb.set_trace()
           # perhaps the last directChildOfRoot is always the free translation line?
        indices = [which(tbl, i) for i in self.morphemeIDs]
        self.freeTranslationID = self.directChildrenOfRootIDs[directChildrenCount - 1]

    def show(self):
        print("--- WordsAsElementsLine")
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


def which(tbl, id):
   return(tbl.index[tbl["ANNOTATION_ID"] == id].tolist()[0])

