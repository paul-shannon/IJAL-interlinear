import EAFParser as eaf

class iiGenerator:

    def __init__(self, filename):
       self.doc = eaf.parse(filename, silence=True)
       self.timeSlotElements = self.doc.get_TIME_ORDER().get_TIME_SLOT()
       self.linguisticTypeForTierElements = self.doc.get_LINGUISTIC_TYPE()
       self.tierElements = self.doc.get_TIER()
       self.tierLinguisticTypesTimeAlignable = self.getTierLinguisticTypesTimeAlignable()
       #self.alignedAnnotations = self.parseAlignableAnnotations()

    def getTimeSlotCount(self):
       return(len(self.timeSlotElements))

    def getTierCount(self):
       return(len(self.tierElements))

    def getLinguisticTypeCount(self):
       return(len(self.linguisticTypeForTierElements))

    def getTierLinguisticTypesTimeAlignable(self):
       ids = ([e.get_LINGUISTIC_TYPE_ID() for e in self.linguisticTypeForTierElements])
       timeAlignable = ([e.get_TIME_ALIGNABLE() for e in self.linguisticTypeForTierElements])
       result = {}
       for i in range(len(ids)):
          result[ids[i]] = timeAlignable[i]
       return(result)





