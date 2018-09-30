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
    test_toHTML()

def test_constructor():

    print("--- test_constructor")
    
    text = Text("../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf",
                "../testData/monkeyAndThunder/audioPhrases",
                grammaticalTermsFile="../testData/monkeyAndThunder/grammaticalTerms.txt",
                tierGuideFile="../testData/monkeyAndThunder/tierGuide.yaml")
     
    assert(text.validInputs())

def test_toHTML():

    print("--- test_toHTML")
    
    text = Text("../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf",
                "../testData/monkeyAndThunder/audioPhrases",
                grammaticalTermsFile="../testData/monkeyAndThunder/grammaticalTerms.txt",
                tierGuideFile="../testData/monkeyAndThunder/tierGuide.yaml")
     
    text.getTable(0)
    
    htmlText = text.toHTML()
    filename = "monkeyAndThunder.html"
    f = open(filename, "w")
    f.write(indent(htmlText))
    f.close()
    os.system("open %s" % filename)



if __name__ == '__main__':
    runTests()
