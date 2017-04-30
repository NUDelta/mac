# MAC (MAterial Crowdsourcing)
MAC is a module for generating GPX files to simulate geolocation routes in iOS.

## Setup
We use **Python 2.7** for the GPX file generator. We recommend using the **anaconda** package manager to setup and maintain environments. To install this, we recommend installing [Miniconda](https://conda.io/miniconda.html). Don't make a conda envrionment yet as we will do this in the next step.

### Create a conda env with required packages
Open Terminal and navigate to the cloned repository. Run `conda env create -n mac -f environment.yml` to create a new conda env and install all the required packages for our project. Then, run `source activate mac` to start the virtual environment. Note that you will need to source the environment each time you wish to use or view our code. When finished, you can run  `source deactivate` to stop the virtual environment.

### Installation without Conda
If you prefer not to use conda, run `pip install -r requirements.txt`. We do still recommend using a [virtual environment](http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/) as it is a good practice to keep dependencies isolated between projects.

## Usage
### GPX file generation
MAC supports GPX file generation from a MongoDB or JSON file. Generated files will be put into directories at same level of the `gpx.py` file labeled by user names. 
#### MongoDB
1. Please see and modify the `fetch_data_mongodb()` function to connect to your personal MongoDB.
2. Run `python gpx.py mongodb` to fetch data and create GPX files for each route of each user pulled from your database.
#### JSON
1. Create a JSON file with the following format (latitude, longitude are numbers):
```
[
    {
        "user": "user name",
        "coordinates": [[latitude, longitude], [latitude, longitude], [latitude, longitude]...]
    },
    ...
]
```
2. Run `python gpx.py json json-file-path.json`

### Visualizing Routes
We have included a barebones iOS project for visualizing routes. Once GPX file creation is done, open the `mac-ios` project in Xcode and add the desired GPX file to your project by dragging and dropping it under the `mac-ios` folder. Run the project on an iPad Simulator (you can use iPhone, if desired, but we find the visualization is much easier to see on iPad). Near the debug console will be a location arrow that, when clicked, will let you select a GPX file to simulate location with.

This same process can be done on other iOS projects using the Simulator and on tethered devices.
