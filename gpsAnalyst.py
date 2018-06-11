
import csv, os
from types import SimpleNamespace
import dateutil.parser

def Filter(aCollection, criteria):
    '''
    returns list of all items in the sequence which meet the criteria
    :param aCollection: collection to be filtered
    :param criteria: funct<item, bool> true if add to return list
    :return: list of items in sequence which meet criteria
    '''
    for item in aCollection:
        if criteria(item):
            yield item

def CountIf(aCollection, criteria):
    '''
    Counts all items in sequence
    :param aCollection: collection to be counted
    :param criteria: criteria for counting the items
    :return: the number of items which meet the criteria
    '''

    # from https://stackoverflow.com/a/2643910/1339950
    return sum(1 if criteria(x) else 0 for x in aCollection)

# import sys
# doThis = [4, 2, 7, 3, 0, 9]
# filtered = list(Filter(doThis, lambda itm: itm > 4))
# number = CountIf(doThis, lambda itm: itm < 7)
#
# sys.exit()

def _lookLikeHeaders(aRow, percentAlpha=0.8):
    total = len(aRow)
    isNotNumber = CountIf(aRow, lambda x: not x.isnumeric())
    return (isNotNumber / total) > percentAlpha

if __name__ == '__main__' and False:
    aList = ['a', '2', 'supercalif', '3.14159']
    assert _lookLikeHeaders(aList, 0.4)
    assert not _lookLikeHeaders(aList)

    print('Tests pass')
    import sys; sys.exit()

class HeaderInfo():
    def __init__(self, headerRow):
        if _lookLikeHeaders(headerRow):
            self.referenceDict = \
                {name: index for index, name in enumerate(headerRow)}
            self.isHeader = True
        else:
            self.isHeader = False
            raise NotImplemented("Not ready for headerless files.")

class dynamicCsvRecord:
    def __init__(self, dataList, headerInfo):
        pass


def createInstanceFromCsv(pathFileName):
    def _tryParseStr(aStr):
        try:
            return int(aStr)
        except ValueError:
            pass
        try:
            return float(aStr)
        except ValueError:
            pass
        try:
            return dateutil.parser.parse(aStr)
        except ValueError:
            return aStr

    with open(pathFileName, newline='') as csvfile:
        reader = csv.reader(csvfile)
        firstRow = next(reader)
        headerInfo = HeaderInfo(firstRow)
        csvfile.seek(0)
        startIndex = 1 if headerInfo.isHeader else 0
        allRows = [x.rstrip().split(',')
                   for x in csvfile][startIndex:]

        returnList = []
        for aRow in allRows:
            anInstance = SimpleNamespace()
            for attrName, attrIndex in headerInfo.referenceDict.items():
                valString = aRow[attrIndex]
                theValue = _tryParseStr(valString)
                setattr(anInstance, attrName, theValue)
            returnList.append(anInstance)
        return returnList

import simplekml
def getAsKML(pointSequence,
              saveToFileName,
              latAttribName='lat',
              longAttrName='lon'):
    """

    :param pointSequence:
    :param saveToFileName:
    :param latAttribName:
    :param longAttrName:
    :return: the kml file that was created to do this
    :rtype: simplekml.kml.Kml
    """
    kml = simplekml.Kml()
    prevTime = None
    for index, aPoint in enumerate(pointSequence):
        currTime = aPoint.time
        if index == 0:
            prevTime = currTime
        timeSpan = currTime - prevTime
        lat = getattr(aPoint, latAttribName)
        lon = getattr(aPoint, longAttrName)
        kml.newpoint(coords=[(lon, lat)])
        prevTime = currTime
    return kml

def saveAsKML(pointSequence,
              saveToFileName,
              latAttribName='lat',
              longAttrName='lon'):
    """

    :param pointSequence:
    :param saveToFileName:
    :param latAttribName:
    :param longAttrName:
    :return: the kml file that was created to do this
    :rtype: simplekml.kml.Kml
    """
    kml = getAsKML(pointSequence, saveToFileName, latAttribName='lat',
              longAttrName='lon')
    kml.save(saveToFileName)
    return kml

if __name__ == '__main__':
    testDir = os.path.join(os.getcwd(), 'testData')

    inputFile = os.path.join(testDir, r"GPS Readings Stationary NCSU Campus.csv")
    newInstance = createInstanceFromCsv(inputFile)

    import statistics

    lonList = [x.lon for x in newInstance]
    averageLon = statistics.mean(lonList)
    stdDevLon = statistics.stdev(lonList)
    rangeLon = min(lonList), max(lonList)

    latList = [x.lat for x in newInstance]
    averageLat = statistics.mean(latList)
    stdDevLat = statistics.stdev(latList)
    rangeLat = min(lonList), max(latList)

    from math import fabs
    aveLocation = 'N {0} W {1}'.format(averageLat, fabs(averageLon))

    dbg = True

    outFile = os.path.join(testDir, r"NCSU Campus Stationary.kml")
    saveAsKML(newInstance, outFile)

    import sys
    sys.exit()



