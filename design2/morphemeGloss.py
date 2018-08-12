# MorphemeGloss.py: a class with which to capture, and rending into HTML, the morphemes of the spoken text, using
# standard grammatical terms:
#
#  grammatical terms are commonly abbreviated and printed in SMALL CAPITALS to keep them distinct
#  from translations, #  especially when they are frequent or important for analysis.
#      [see https://en.wikipedia.org/wiki/Interlinear_gloss#Structure]
#
# see the Leipzig Glossing Rules: https://www.eva.mpg.de/lingua/resources/glossing-rules.php
#
# in interlienar morphological glosses, punctuation separate the glosses:
#
#        .  equivalent to a space (separating words) in the morpheme line
#        -  or _ when a source language word corresponds to a phrase in the glossing language
#        =  separates clitics (a morpheme with syntactic characteristics of a word, but which
#           depends phonologically upon another word or phrase)
#        ~  reduplication
#
# david beck (email 12 aug 2018):
#
#    I usually leave the numbers in the abbreviations in normal font size, as well as punctuation
#    marks like the colon and the period (which are reserved characters for interlinear glossing). The
#    morpheme delimiters are also in regular sized type, and in the original GUI there was a field
#    where the user could list the symbols in use. – (n-dash), =, and • are the most common, but there
#    are others people are likely to use such as ~ (for reduplication), ^ (to add a floating tone to a
#    morph), and < > (for infixes). Another thing that we haven’t come up against yet is that there are
#    sometimes subscripts, most commonly used to label something as belonging to a particular class.
#------------------------------------------------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------------------------------------------------
import re
from pprint import pprint
import pdb
#------------------------------------------------------------------------------------------------------------------------
class MorphemeGloss:

   rawText = ""
   grammaticalTerms = []
   delimiters = "([=•\d\.–])"

   def __init__(self, rawText, grammaticalTerms):
     self.rawText = rawText
     self.grammaticalTerms = grammaticalTerms;

   def show(self):

      pprint(vars(self))

   def parse(self):
      """ identify terms, delimiters, plain words """
      self.parts = extractParts(self.delimiters, self.rawText)

   def getParts(self):
      return(self.parts)

   def toHTML(self);
      """ iterate over the parts list, idenitfy each grammaticalTerm
          wrap each of those in a <span class='grammticalTerm'> tag
      """
      return("nothing yet")


#------------------------------------------------------------------------------------------------------------------------
# non-class functions
#------------------------------------------------------------------------------------------------------------------------
def extractParts(delimiters, string):

   parts = re.split(delimiters, string)
   parts_noEmptyStrings = [part for part in parts if part != ""]
   return(parts_noEmptyStrings)
