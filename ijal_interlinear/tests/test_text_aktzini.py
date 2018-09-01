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
    
    text = Text("../testData/aktzini/18-06-03Aktzini-GA.eaf",
                "../testData/aktzini/audioPhrases",
                grammaticalTermsFile=None,
                quiet=False)

    text.getTable(0)
    
    htmlText = text.toHTML()
    filename = "aktzini.html"
    f = open(filename, "w")
    f.write(indent(htmlText))
    f.close()
    os.system("open %s" % filename)

if __name__ == '__main__':
    runTests()
