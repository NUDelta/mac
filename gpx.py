"""This module is used to create gpx files for iOS location simulation"""
import os
import sys
from pymongo import MongoClient


def gpx(db_connection=None):
    """
    Fetches data from a specified mongodb and converts location data into a gpx file.
    example of gpx file structure
    <gpx>
        <name>route1</name>
        <number>1</number>
        <wpt lat="42.046908" lon="-87.679314">
          <ele>0</ele>
          <time>2016-12-29T00:01:00Z</time>
          <name>pt0</name>
        </wpt>
    </gpx>

    Inputs:

    """
    # query mongodb for data
    query = {'user': 'kgarg'}
    query_results = db_connection.locations.find(query).sort('_id', -1)

    # create gpx file
    header = '<gpx>\n'
    header_end = '</gpx>'
    wpt_end = '</wpt>'
    indent = '  '

    cnt = 0
    current_user = ''
    for query_result in query_results:
        # get data from query
        coords = query_result['coordinates']
        user = query_result['user']

        # make a file for each route for each user
        if current_user == '':
            current_user = user
        elif current_user != user:
            current_user = user
            cnt = 0

        directory = './%s-gpx-routes/' % (user)
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_name = directory + '%s_%d.gpx' % (user, cnt)

        # prepare output string
        out_str = ''
        out_str += header

        # create coordinate outputs
        for coord in coords:
            lat = coord[0]
            lng = coord[1]
            waypoint = indent + '<wpt lat=\"%f\" lon=\"%f\">\n' % (lat, lng)
            out_str += waypoint
            out_str += indent + wpt_end + '\n'

        out_str += header_end

        # write file
        with open(file_name, 'w') as out_file:
            out_file.write(out_str)

        # increment user route counter
        cnt += 1


if __name__ == '__main__':
    # setup mongo connection
    URI = 'mongodb://127.0.0.1/'
    DBNAME = 'movement-model'

    CLIENT = MongoClient(URI)
    DB = CLIENT[DBNAME]

    # run and export gpx file
    gpx(DB)
