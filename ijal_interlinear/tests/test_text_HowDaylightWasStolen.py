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

    text = Text("../testData/harryMosesDaylight/daylight_1_4.eaf",
                "../testData/harryMosesDaylight/audioPhrases",
                grammaticalTermsFile=None,
                tierGuideFile="../testData/harryMosesDaylight/tierGuide.yaml")

     
    assert(text.validInputs())

def test_toHTML():

    print("--- test_toHTML")
    
    text = Text("../testData/harryMosesDaylight/daylight_1_4.eaf",
                "../testData/harryMosesDaylight/audioPhrases",
                grammaticalTermsFile=None,
                tierGuideFile="../testData/harryMosesDaylight/tierGuide.yaml")

    text.getTable(1)

    htmlText = text.toHTML()
    filename = "daylight.html"
    f = open(filename, "w")
    f.write(indent(htmlText))
    f.close()
    os.system("open %s" % filename)
    
if __name__ == '__main__':
    runTests()
