# test_AudioExtractor.py
#----------------------------------------------------------------------------------------------------
import re
import sys
sys.path.append("..")

from audioExtractor import *
#----------------------------------------------------------------------------------------------------

def runTests():
    test_constructor()
    test_determineStartAndEndTimes()
    test_extract()
    
def test_constructor():

    print("--- test_constructor")
    ea = AudioExtractor("../testData/harryMosesDaylight/daylight_1_4.wav",
                        "../testData/harryMosesDaylight/daylight_1_4.eaf",
                        "../testData/harryMosesDaylight/audioPhrases")
    assert(ea.validInputs)

def test_determineStartAndEndTimes():

    print("--- test_determineStartAndEndTimes")
    ea = AudioExtractor("../testData/harryMosesDaylight/daylight_1_4.wav",
                        "../testData/harryMosesDaylight/daylight_1_4.eaf",
                        "../testData/harryMosesDaylight/audioPhrases")
    tbl = ea.determineStartAndEndTimes()
    # print(tbl)
    assert(tbl.shape == (4, 5))
    assert(list(tbl.columns) == ["lineID", "start", "end", "t1", "t2"])
    (a4_start, a4_end) = tbl.loc[tbl['lineID'] == 'a4'][['start', 'end']].iloc[0].tolist()
    assert(a4_start == 17800)
    assert(a4_end == 22938)

def test_extract():
    print("--- test_determineStartAndEndTimes")
    ea = AudioExtractor("../testData/harryMosesDaylight/daylight_1_4.wav",
                        "../testData/harryMosesDaylight/daylight_1_4.eaf",
                        "../testData/harryMosesDaylight/audioPhrases")
    ea.extract(quiet=False)
    

if __name__ == '__main__':
    runTests()
    
