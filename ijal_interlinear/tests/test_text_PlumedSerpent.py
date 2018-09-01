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

    test_toHTML()

def test_toHTML():

    print("--- test_toHTML")
    
    text = Text("../testData/plumedSerpent/TRS Plumed Serpent Legend 05-15-2017.eaf",
                "../testData/plumedSerpent/audioPhrases",
                grammaticalTermsFile=None,
                quiet=False)

    text.getTable(0)

    htmlText = text.toHTML()
    filename = "plumedSerpent.html"
    f = open(filename, "w")
    f.write(indent(htmlText))
    f.close()
    os.system("open %s" % filename)

if __name__ == '__main__':
    runTests()
