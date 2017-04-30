"""This module is used to create gpx files for iOS location simulation"""
import os
import sys
import json
from pymongo import MongoClient


def gpx(user_routes):
    """
    Converts list of dicts with user and their routes into a gpx file for iOS location simulation

    Example of gpx file structure:
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
        Example below:
        [
        {
            'user': 'user name',
            'route': [[latitude, longitude], [latitude, longitude], [latitude, longitude]...]
        }
        ...
        ]

    Output:
        saves gpx files based on user's name and count of routes
    """
    # create gpx file
    header = '<gpx>\n'
    header_end = '</gpx>'
    wpt_end = '</wpt>'
    indent = '  '

    users = {}
    for user_route in user_routes:
        # get data from query
        user = user_route['user']
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

    The MongoDB must contain a collection with documents containing at least the information below
    (latitude, longtiude are numbers):
    [
    {
        "_id": {
            "$oid":"58d9879554890e000996ddb5"
            },
        "created":1490651029,
        "coordinates": [[latitude, longitude], [latitude, longitude], [latitude, longitude]...],
        "user": "user name",
        "lastModified":1490651029
    }
    ...
    ]

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

    # format data into correct format for gpx()
    output_data = []
    for query_result in query_results:
        # get data from query
        curr_data = {'user': query_result['user'], 'route': query_result['coordinates']}
        output_data.append(curr_data)

    # return data
    return output_data


def fetch_data_json(data_file):
    """
    Fetches data from a JSON file and formats it into a format recognizable by gpx.

    The JSON file must be formatted as follows (latitude, longtiude are numbers):
    [
    {
            "user": "user name",
            "coordinates": [[latitude, longitude], [latitude, longitude], [latitude, longitude]...]
    },
    ...
    ]

    Output:
        (list of dicts): list of dicts containing a user name and a route for each user
    """
    # read in file
    with open(data_file) as data_file:
        data_array = json.load(data_file)

    # format data into correct format for gpx()
    output_data = []
    for data in data_array:
        # get data from query
        curr_data = {'user': data['user'], 'route': data['coordinates']}
        output_data.append(curr_data)

    # return data
    return output_data


if __name__ == '__main__':
    # run and export gpx file
    try:
        if sys.argv[1] == 'mongodb':
            gpx(fetch_data_mongodb())
        elif sys.argv[1] == 'json':
            gpx(fetch_data_json(sys.argv[2]))
        else:
            raise IndexError
    except IndexError:
        print 'Incorrect usage: gpx.py <mongodb|json> <json-filepath>'
        sys.exit(1)
