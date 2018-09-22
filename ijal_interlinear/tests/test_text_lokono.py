import re
import sys
sys.path.append("..")
from text import *
import importlib
import os
import pdb
#----------------------------------------------------------------------------------------------------
pd.set_option('display.width', 1000)
#----------------------------------------------------------------------------------------------------

def runTests():

    test_constructor()
    test_forConsistentLineTierStructure()
    test_toHTML()

def test_constructor():

    print("--- test_constructor")

    text = Text("../testData/lokono/LOKONO_IJAL_2.eaf",
                audioPath=None,
                grammaticalTermsFile=None)

    assert(text.validInputs())

def test_traverseStructure():

    print("--- test_traverseStructure")
    text = Text("../testData/lokono/LOKONO_IJAL_2.eaf",
                audioPath=None,
                grammaticalTermsFile=None)
    text.traverseStructure()

def exploreMapping():

    text = Text("../testData/lokono/LOKONO_IJAL_2.eaf",
                audioPath=None,
                grammaticalTermsFile=None)
    text.getTable(0)


def test_toHTML():

    print("--- test_toHTML")

    text = Text("../testData/lokono/LOKONO_IJAL_2.eaf",
                audioPath=None, #"../testData/lokono/audioPhrases",
                grammaticalTermsFile="../testData/monkeyAndThunder/grammaticalTerms.txt",
                tierGuideFile="../testData/lokono/tierGuide.yaml")

    text.getTable(0)

    htmlText = text.toHTML()
    filename = "monkeyAndThunder.html"
    f = open(filename, "w")
    f.write(indent(htmlText))
    f.close()
    os.system("open %s" % filename)

if __name__ == '__main__':
    runTests()
