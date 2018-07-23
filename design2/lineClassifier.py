class LineClassifier:

    tbl = None

    def __init__(self, tbl):
       self.tbl = tbl

    def run(self):
        tierCount = self.tbl.shape[0]
        tabbedTiers = ["\t" in t for t in self.tbl["TEXT"].tolist()]
        tabDelimitedTierCount = len([i for i, tabbed in enumerate(tabbedTiers) if tabbed])
        # pdb.set_trace()
        if(tierCount == 2 and tabDelimitedTierCount == 0):
            return("DegenerateLine")

            # a canonical line with just one word will have no delimiting tab in the word/gloss tiers
            # but most lines have multiple words, thus at least one tab, thus at least two tiers with tabs
        if(tierCount == 4 and tabDelimitedTierCount in [0,2]):
            return("CanonicalLine")

          # WordsAsElements Lines are distinguished by
          #  tier count >= 5 (spokenText, free translation, and one or more
          #    words in plain text each with two children, a morpheme and a gloss)

        if(tierCount >= 5 and tabDelimitedTierCount == 0):
            return("WordsAsElementsLine")

        return(None)
