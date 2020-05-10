import glob
import os
import sys
from requests.exceptions import ConnectionError
from configparser import ConfigParser
from stravalib import Client, exc


def uploadFile(stravaClient, filename):
    """ Upload a single file """

    try:
        stravaClient.upload_activity(
            activity_file=open(filename, 'r'),
            data_type='tcx',
            description='Imported from NikeRunClub',
            activity_type='run'
        )

    except ConnectionError:
        print('Internet connection failed')
        return
    except exc.ActivityUploadFailed as inst:
        print('Exception occurred: ' + str(inst))
        return

    print('Uploading ' + filename + ' to Strava completed successfully')


def main():

    """ Get access token from stravaupload.cfg """
    config = ConfigParser()
    config.read('./scripts/.stravaupload.cfg')

    if config.has_option('access', 'clientid'):
        client_id = config.get('access', 'clientid')
    else:
        print('No access/clientid found in .stravaupload.cfg')
        sys.exit(0)

    if config.has_option('access', 'token'):
        access_token = config.get('access', 'token')
    else:
        print('No access/token found in .stravaupload.cfg')
        sys.exit(0)

    if config.has_option('access', 'clientsecret'):
        client_secret = config.get('access', 'clientsecret')
    else:
        print('No access/clientsecret found in .stravaupload.cfg')
        sys.exit(0)

    """ Exchange code for token """
    stravaClient = Client()
    stravaClient.exchange_code_for_token(
        client_id=client_id,
        client_secret=str(client_secret),
        code=str(access_token)
    )

    """ Check if input is a single file or a directory """
    if len(sys.argv) == 1:
        ''' Find directory where are stored TCX converted files '''
        tcxDir = os.path.join(os.getcwd(), 'TCX_exports')

        ''' Set TCX pattern to finf files ending with .tcx '''
        tcxPattern = os.path.join(tcxDir, '*.tcx')
        filenames = glob.glob(tcxPattern)

        if len(filenames) == 0:
            sys.exit('No .tcx found in ' + str(sys.argv[1]) + ' directory')
        else:
            for idx, filename in enumerate(filenames):
                uploadFile(stravaClient, filename)
    elif os.path.isfile(sys.argv[1]):
        uploadFile(stravaClient, sys.argv[1])
    else:
        sys.exit('usage: stravaupload.py <filename.tcx>')


if __name__ == '__main__':
    main()
