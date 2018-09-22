# text.py: a class to represent a complete IJAL interlinear text, and to transform its
# represention in ELAN xml (eaf) format, accompanied by audio, into html
#----------------------------------------------------------------------------------------------------
import re
import sys
import os
import yaml
import unittest
from line import *
from canonicalLine import *
from degenerateLine import *
from lineClassifier import *
import importlib
pd.set_option('display.width', 1000)
import pdb
#----------------------------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------------------------------------------------
class Text:

   xmlFilename = ''
   audioPath = ''
   grammaticalTermsFile = None
   grammaticalTerms = []
   xmlDoc = None
   htmlDoc = None
   lineCount = 0
   quiet = True

   def __init__(self, xmlFilename, audioPath, grammaticalTermsFile, tierGuideFile, quiet=True):
     self.xmlFilename = xmlFilename
     self.audioPath = audioPath
     self.grammaticalTermsFile = grammaticalTermsFile
     self.tierGuideFile = tierGuideFile
     self.validInputs()
     self.quiet = quiet
     self.xmlDoc = etree.parse(self.xmlFilename)
     self.lineCount = len(self.xmlDoc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))
     with open(tierGuideFile, 'r') as f:
        self.tierGuide = yaml.load(f)
     self

   def validInputs(self):
     assert(os.path.isfile(self.xmlFilename))
     assert(os.path.isfile(self.tierGuideFile))
     assert(self.audioPath == None or os.path.isdir(self.audioPath))
     if(not self.grammaticalTermsFile == None):
        assert(os.path.isfile(self.grammaticalTermsFile))
        self.grammaticalTerms = open(self.grammaticalTermsFile).read().split("\n")
        assert(len(self.grammaticalTerms) > 0)
     return(True)

   def getTable(self, lineNumber):
     x = Line(self.xmlDoc, lineNumber)
     return(x.getTable())

   def traverseStructure(self):
      lineNumbers = range(self.lineCount)
      for i in lineNumbers:
         x = Line(self.xmlDoc, i)
         tbl = x.getTable()
         print("%d: %d tiers" % (i, tbl.shape[0]))



   def toHTML(self, lineNumber=None):

     htmlDoc = Doc()

     if(lineNumber == None):
        lineNumbers = range(self.lineCount)
     else:
        lineNumbers = [lineNumber]

     htmlDoc.asis('<!DOCTYPE html>')
     with htmlDoc.tag('html', lang="en"):
        with htmlDoc.tag('head'):
            htmlDoc.asis('<meta charset="UTF-8">')
            htmlDoc.asis('<link rel="stylesheet" href="ijal.css">')
            htmlDoc.asis('<script src="ijalUtils.js"></script>')
            with htmlDoc.tag('body'):
                for i in lineNumbers:
                    x = Line(self.xmlDoc, i)
                    with htmlDoc.tag("div",  klass="line-wrapper"):
                        tbl = x.getTable()
                        lineID = tbl.ix[0]['ANNOTATION_ID']
                        classifier = LineClassifier(tbl)
                        classification = classifier.run()
                        if(not self.quiet):
                           print("%3d: %s" % (i, classification))
                        with htmlDoc.tag("div", klass="line-sidebar"):
                            x.htmlLeadIn(htmlDoc, self.audioPath)
                        if(classification == "CanonicalLine"):
                            xc = CanonicalLine(self.xmlDoc, i, self.grammaticalTerms)
                            xc.toHtml(htmlDoc)
                        elif(classification == "DegenerateLine"):
                            xd = DegenerateLine(self.xmlDoc, i)
                            xd.toHtml(htmlDoc)
     self.htmlDoc = htmlDoc
     self.htmlText = htmlDoc.getvalue()
     return(self.htmlText)

