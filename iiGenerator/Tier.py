class Tier:
   type = None
   id = None
   parent = None
   annotationElements = []   # Annotation will be a class, supporting ALIGNABLE and REF varieties

   def __init__(self, tierElement):
     self.type = tierElement.attrib.get('LINGUISTIC_TYPE_REF')
     self.parent = tierElement.attrib.get('PARENT_REF')
     self.id = tierElement.attrib.get('TIER_ID')
     self.annotationElements = tierElement.findall("ANNOTATION")

   def getType(self):
      return(self.type)

   def getParent(self):
      return(self.parent)

   def getId(self):
      return(self.id)

   def getAnnotationElements(self):
      return(self.annotationElements)

