"""This module is used to create gpx files for iOS location simulation"""
import os
import sys
from pymongo import MongoClient


def gpx(user_routes):
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
        user_routes (list of dicts): list of dicts containing a user name and a route for each user
    """
    # create gpx file
    header = '<gpx>\n'
    header_end = '</gpx>'
    wpt_end = '</wpt>'
    indent = '  '

    users = {}
    for user_route in user_routes:
        # get data from query
        user = user_route['name']
        coords = user_route['route']

        # make a file for each route for each user
        if user not in users:
            users[user] = 1
        else:
            users[user] += 1

        directory = './%s-gpx-routes/' % (user)
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_name = directory + '%s_%d.gpx' % (user, users[user])

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


def fetch_data_mongodb():
    """
    Fetches data from a mongodb and formats it into a format recognizable by gpx.

    Output:
        (list of dicts): list of dicts containing a user name and a route for each user
    """
    # setup mongo connection
    uri = 'mongodb://127.0.0.1/'
    db_name = 'movement-model'
    collection_name = 'locations'

    client = MongoClient(uri)
    db_connection = client[db_name]

    # query mongodb for data
    query_results = db_connection.locations.find().sort('_id', -1)

    # format data into correct format
    output_data = []
    for query_result in query_results:
        # get data from query
        curr_data = {'name': query_result['user'], 'route': query_result['coordinates']}
        output_data.append(curr_data)

    # return data
    return output_data


if __name__ == '__main__':
    # run and export gpx file
    try:
        if sys.argv[1] == 'mongodb':
            gpx(fetch_data_mongodb())
        elif sys.argv[1] == 'json':
            pass
        else:
            raise IndexError
    except IndexError:
        print 'Incorrect usage: gpx.py <mongodb|json> <json-filepath>'
        sys.exit(1)
