import os
import pytz
import json
import datetime as dt


def epochToReadable(epochTime):
    """ Convert epoch value to human readable format - Ex: 1524591824431 --> 2018-04-24T17:43:44Z """

    finalTimeWithLocalUtc = dt.datetime.fromtimestamp(epochTime / 1000.0)
    utc = pytz.UTC
    finalTime = finalTimeWithLocalUtc.astimezone(utc)
    formattedTime = finalTime.strftime('%Y-%m-%dT%H:%M:%SZ')
    return formattedTime


def epochDifferenceToMilliSeconds(epochStart, epochEnd):
    """ Compute elapsed time in milliseconds between two epoch """

    startTime = dt.datetime.fromtimestamp(epochStart/1000.0)
    endTime = dt.datetime.fromtimestamp(epochEnd/1000.0)
    elapsedTime = abs(endTime - startTime)
    return elapsedTime.total_seconds()*1000.0


def jsonReader(jsonFilePath):
    """ Parse JSON file and return data """

    jsonFile = os.path.join(jsonFilePath)
    jsonData = open(jsonFile)
    data = json.load(jsonData)
    jsonData.close()
    return data


def prepareLap(data):
    """ Get all interesting values for building lap """

    structValues = []

    """ Get total distance in meters and calories """
    for metric in data['summaries']:
        if metric['metric'] == "distance":
            distanceMeters = metric['value'] * 1000.0
        elif metric['metric'] == "calories":
            calories = metric['value']

    """ Build struct to use """
    for metric in data['metrics']:
        if metric['type'] == "latitude":
            latitudes = metric['values']
        elif metric['type'] == "longitude":
            longitudes = metric['values']
        elif metric['type'] == "distance":
            distances = metric['values']

    for idxDist in range(0, len(distances)):
        if idxDist == 0:
            currentDistance = 0

        for idxLatLon in range(0, len(latitudes)):
            """ Get each difference in ms """
            diff = epochDifferenceToMilliSeconds(distances[idxDist]['start_epoch_ms'],
                                                 latitudes[idxLatLon]['start_epoch_ms'])

            if diff < 2500.0:
                currentDistance += distances[idxDist]['value']*1000.0

                structValues.append({"time": latitudes[idxLatLon]['start_epoch_ms'],
                                     "distance": currentDistance,
                                     "latitude": latitudes[idxLatLon]['value'],
                                     "longitude": longitudes[idxLatLon]['value']})
                break

    return distanceMeters, calories, structValues
