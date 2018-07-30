import argparse
import os.path
import pandas as pd
from xml.etree import ElementTree as etree
from scipy.io.wavfile import *
import pdb

def getArgs():
    parser = argparse.ArgumentParser(
        description='creates small wav file audio samples from a single large file')
    parser.add_argument(
        '-x', '--xmlfile', type=str, help='eaf/xml story markup filename', required=True)
    parser.add_argument(
        '-a', '--audiofile', type=str, help='32-bit wav file', required=True)
    parser.add_argument(
        '-o', '--outputdir', type=str, help='directory into which audio samples are written', required=True)
    # Array for all arguments passed to script
    args = parser.parse_args()
    # Assign args to variables
    xmlFile = args.xmlfile
    audioFile = args.audiofile
    outputDir = args.outputdir
    return xmlFile, audioFile, outputDir


def getAllTimes(filename):
   xmlDoc = etree.parse(filename)
   timeSlotElements = xmlDoc.findall("TIME_ORDER/TIME_SLOT")
   audioTiers = xmlDoc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION")
   timeIDs = [x.attrib["TIME_SLOT_ID"] for x in timeSlotElements]
   times = [int(x.attrib["TIME_VALUE"]) for x in timeSlotElements]
   audioIDs = [x.attrib["ANNOTATION_ID"] for x in audioTiers]
   tsRef1 = [x.attrib["TIME_SLOT_REF1"] for x in audioTiers]
   tsRef2 = [x.attrib["TIME_SLOT_REF2"] for x in audioTiers]
   d = {"id": audioIDs, "t1": tsRef1, "t2": tsRef2}
   tbl_t1 = pd.DataFrame({"id": audioIDs, "t1": tsRef1})
   tbl_t2 = pd.DataFrame({"id": audioIDs, "t2": tsRef2})
   tbl_times = pd.DataFrame({"id": timeIDs, "timeValue": times})
   tbl_t1m = pd.merge(tbl_t1, tbl_times, left_on="t1", right_on="id")
   tbl_t2m = pd.merge(tbl_t2, tbl_times, left_on="t2", right_on="id")
   tbl_raw = pd.merge(tbl_t1m, tbl_t2m, on="id_x")
   tbl = tbl_raw.drop(["id_y_x", "id_y_y"], axis=1)
     # still need to rename, maybe also reorder columns
   tbl.columns = ["lineID", "t1", "start", "t2", "end"]
   list(tbl.columns)
   tbl = tbl[["lineID", "start", "end", "t1", "t2"]]
   return(tbl)

def test_getAllTimes():
   filename_xml = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
   tbl_times = getAllTimes(filename_xml)
   assert(tbl_times.shape == (41, 5))
   assert(list(tbl_times.columns) == ["lineID", "start", "end", "t1", "t2"])
   (a28_start, a28_end) = tbl_times.loc[tbl_times['lineID'] == 'a28'][['start', 'end']].iloc[0].tolist()
   assert(a28_start == 93905)
   assert(a28_end == 96368)

def extractAndWrite(audioFile, tbl, outputDir):
   rate, mtx = read(audioFile)
   mtx.shape
   mtx.shape[0]/rate   # 5812410, 2
   samples = mtx.shape[0]
   duration = mtx.shape[0] / rate
   phraseCount = tbl.shape[0]
   pdb.set_trace()
   for i in range(phraseCount):
       print(i)
       phraseID, start, end = tbl.ix[i].tolist()[0:3]
       startSeconds = start/1000
       endSeconds = end/1000
       startIndex = int(round(startSeconds * rate))
       endIndex   = int(round(endSeconds * rate))
       phrase = mtx[startIndex:endIndex,]
       sampleFilename = "%s/%s.wav" % (outputDir, phraseID)
       print("--- writing %d samples to %s" % (phrase.shape[0], sampleFilename))
       write(sampleFilename, rate, phrase)

def testMain():
    xmlFile = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder.eaf"
    audioFile = "../testData/monkeyAndThunder/AYA1_MonkeyandThunder-32bit.wav"
    outputDir = "monkeyTest"
    tbl = getAllTimes(xmlFile)
    extractAndWrite(audioFile, tbl, outputDir)


# if (__name__ == "__main__"):
#    xmlFile, audioFile, outputDir = getArgs()
#    assert(os.path.exists(xmlFile))
#    assert(os.path.exists(audioFile))
#    assert(os.path.exists(outputDir))
#
#    tbl = getAllTimes(xmlFile)
#    extractAndWrite(audioFile, tbl, outputDir)
