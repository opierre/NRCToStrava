import os
import sys
from io import BytesIO
from xml.etree import ElementTree as et

from tcx_format.TrainingCenterDatabase import TrainingCenterDatabase
from tcx_format.Activities import Activities
from tcx_format.Activity import Activity
from tcx_format.Lap import Lap

from utils.functions import jsonReader, prepareLap, epochToReadable


class Generator:

    def __init__(self, jsonTxt):
        """ Generate TCX Structure """

        """ Store json """
        self.data = jsonTxt

        """ Get TrainingCenterDatabase element """
        self.root = TrainingCenterDatabase().root

        """ Create Activities from TrainingCenterDatabase """
        self.activities = Activities(self.root).activities

        """ Create Activity from Activities and start_epoch_ms as Id """
        self.activity = Activity(self.activities, self.data['start_epoch_ms']).activity

        """ Prepare values for Lap structure """
        distanceMeters, calories, structValues = prepareLap(self.data)

        """ Create Lap from Activity and summaries values """
        self.lap = Lap(self.activity, self.data['start_epoch_ms'], self.data['active_duration_ms'],
                       distanceMeters, calories, structValues)


def export(_tcxObject, _startTime, _activityID):
    """ Export TCX object to export directory as .tcx file """

    ''' Find directory where are will be stored TCX exports '''
    exportDir = os.path.join(os.path.dirname(__file__), '..\\TCX_exports')
    if not os.path.exists(exportDir):
        os.makedirs(exportDir)

    ''' Build export name '''
    activityTimeDate = _startTime[0:10] + '_' + _startTime[11:13] + '-' + _startTime[14:16] + '-' + _startTime[17:19]
    filePathTcx = os.path.join(exportDir, ('NikePlus_' + activityTimeDate + '_' + _activityID + '.tcx'))

    ''' Write TCX file '''
    f = BytesIO()
    elementTree = et.ElementTree(_tcxObject.root)
    elementTree.write(f, encoding="utf-8", xml_declaration=True)
    with open(filePathTcx, 'wb') as myFile:
        myFile.write(f.getvalue())
        print('Exporting ' + filePathTcx[(filePathTcx.rfind('/') + 1):] + ' completed successfully')


def convert(nikePlusActivityID):
    """ Main function to convert data """

    idExists = False
    activityData = None

    ''' Find directory where are stored JSON exports '''
    activitiesDir = os.path.join(os.getcwd(), 'NRC_activities')

    ''' Find specific export with nikePlusActivityID in its filename '''
    for filename in os.listdir(activitiesDir):
        if filename.find(nikePlusActivityID) != -1:
            idExists = True
            activity_file = os.path.join(activitiesDir, filename)
            activityData = jsonReader(activity_file)
            break

    if idExists:
        ''' Build TCX Structure '''
        tcx = Generator(activityData)

        ''' Export TCX file '''
        export(tcx, epochToReadable(activityData['start_epoch_ms']), activityData['id'])
    else:
        print("Looking for a file with " + str(nikePlusActivityID) + " in its name failed.")


if __name__ == '__main__':
    if len(sys.argv) == 2:
        convert(sys.argv[1])
    else:
        print("usage: nrcToTcx.py <NikeID>")
