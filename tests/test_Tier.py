from .context import Tier
from xml.etree import ElementTree as etree
import unittest


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_constructor(self):
        print("--- test_constructor")
        xmlFile = open("./testData/daylight77a.eaf", 'r')
        tree = etree.parse(xmlFile)
        tierElement = tree.getroot().findall('TIER')[0]
        tier0 = Tier(tierElement)
        assert(tier0.getId() == "speech")
        assert(tier0.getType() == "default-lt")
        assert(tier0.getParent() == None)
        assert(len(tier0.getAnnotationElements()) == 2)



if __name__ == '__main__':
    unittest.main()
