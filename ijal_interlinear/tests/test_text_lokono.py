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
    test_toHTML(display=True)

def test_constructor():

    print("--- test_constructor")

    text = Text("../testData/lokono/LOKONO_IJAL_2.eaf",
                audioPath=None,
                grammaticalTermsFile=None,
                tierGuideFile="../testData/lokono/tierGuide.yaml")
    assert(text.validInputs())

def test_traverseStructure():

    print("--- test_traverseStructure")
    text = Text("../testData/lokono/LOKONO_IJAL_2.eaf",
                audioPath=None,
                grammaticalTermsFile=None,
                tierGuideFile="../testData/lokono/tierGuide.yaml")
    text.traverseStructure()

def exploreMapping():

    text = Text("../testData/lokono/LOKONO_IJAL_2.eaf",
                audioPath=None,
                grammaticalTermsFile=None,
                tierGuideFile="../testData/lokono/tierGuide.yaml")

    text.getTable(0)


def test_toHTML(display=False):

    print("--- test_toHTML")

    text = Text("../testData/lokono/LOKONO_IJAL_2.eaf",
                audioPath=None, #"../testData/lokono/audioPhrases",
                grammaticalTermsFile="../testData/monkeyAndThunder/grammaticalTerms.txt",
                tierGuideFile="../testData/lokono/tierGuide.yaml",
                quiet=False)

    text.getTable(0)

    htmlText = text.toHTML()
    if(display):
        filename = "lokono.html"
        f = open(filename, "w")
        f.write(indent(htmlText))
        f.close()
        os.system("open %s" % filename)

if __name__ == '__main__':
    runTests()
