import sys
import unittest
from morphemeGloss import *
#------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
sampleLines = ["HAB=3A=MOUTH•cry",
               "1S=walk–INC",
               "HAB=3A=work=IAM",
               "PROG=1A=know–INTR",
               "more",
               "1PRO"
               ]
#----------------------------------------------------------------------------------------------------
def runTests():

    test_constructor()

def test_constructor():

    grammaticalTerms = open("abbreviations.txt").read().split("\n")
    mg = MorphemeGloss(sampleLines[0], grammaticalTerms)

def test_extractParts():
    """ this test operates on the global (i.e., non-member) function
        helpful in exploring the problems space, setting the stage
        for the class-based method below
    """

    print("--- test_extractParts")

    delimiters = "([=•\d\.–])"
    parts = extractParts(delimiters, sampleLines[0])
    assert(parts == ['HAB', '=', '3', 'A', '=', 'MOUTH', '•', 'cry'])

    parts = extractParts(delimiters, sampleLines[1])
    assert(parts == ['1', 'S', '=', 'walk', '–', 'INC'])

def test_parse():
    grammaticalTerms = open("abbreviations.txt").read().split("\n")
    mg = MorphemeGloss(sampleLines[0], grammaticalTerms)
    mg.parse()
    assert(mg.getParts() == ['HAB', '=', '3', 'A', '=', 'MOUTH', '•', 'cry'])
