import sys, csv, os
from ExtendedPoint import ExtendedPoint as EP
import ExtendedPoint

__author__ = ['Paul Schrum']

class ExtendedPointSequence(list):

    possible_coordinate_systems = ["XY", "LatLong"]
    _coordinate_system = "XY"

    def __init__(self):
        pass

    def set_coordinate_system(self, coordiante_system):
        if coordiante_system not in self.possible_coordinate_systems:
            raise ValueError("{0} is not an allowed coordiante system."
                             .format_map(coordiante_system))
        self._coordinate_system = coordiante_system

    def computeAllPointInformation(self):
        """
        For each triplet of points in the list of points, compute the
        attribute data for the arc (circular curve segment) that starts
        at point 1, passes through point 2, and ends at point 3.  Then
        assign the curve data to point 2 for safe keeping.
        :param self: This list of points to be analyzed. These must be ordered spatially or the results are meaningless.
        :return: None
        """
        for pt1, pt2, pt3 in zip(self[:-2],
                                 self[1:-1],
                                 self[2:]):
            ExtendedPoint.compute_arc_parameters(pt1, pt2, pt3)

    def writeToCSV(self, fileName):
        """
        Write all points in the point list to the indicated file, expecting
        the points to be of type ExtendedPoint.
        :param self:
        :return: None
        """
        with open(fileName, 'w') as f:
            headerStr = EP.header_list()
            f.write(headerStr + '\n')
            for i, point in enumerate(self):
                writeStr = str(point)
                f.write(writeStr + '\n')

def CreateExtendedPointSequenceFromLatLong(lat_long_point_sequence):
    returnSequence = ExtendedPointSequence()
    returnSequence.set_coordinate_system('LatLong')
    for a_point in lat_long_point_sequence:
        new_extended_point = EP(a_point.lon, a_point.lat)

        # try: new_extended_point.time = a_point.time
        # except AttributeError: pass
        new_extended_point.add_attr('time', a_point)
        new_extended_point.add_attr('speed', a_point)

        returnSequence.append(new_extended_point)


    return returnSequence


def CreateExtendedPointSequenceFromXYcsv(csvFileName, coordianteMode='LatLong'):
    '''
    Factory method. Use this instead of variable = ExtendedPointList().
    Args:
        csvFileName: The path and filename of the csv file to be read.
    Returns: New instance of an ExtendedPointList.
    '''
    newEPL = ExtendedPointSequence()
    with open(csvFileName, mode='r') as f:
        rdr = csv.reader(f)
        count = 0
        for aRow in rdr:
            if count == 0:
                header = aRow
                count += 1
                xIndex = header.index('X')
                yIndex = header.index('Y')
            else:
                x = float(aRow[xIndex])
                y = float(aRow[yIndex])
                newEPL.append(EP(x, y))
    return newEPL

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Running tests.")
        test_dir = os.path.join(os.getcwd(), 'testData', 'NCstatePlane')
        inFileName = os.path.join(test_dir, "Y15A_Computed.csv")
        outFileName = os.path.join(test_dir, "Y15A_Computed_temp.csv")
    else:
        inFileName = sys.argv[1]
        outFileName = sys.argv[2]

    aPointList = CreateExtendedPointSequenceFromXYcsv(inFileName)
    aPointList.computeAllPointInformation()
    aPointList.writeToCSV(outFileName)

