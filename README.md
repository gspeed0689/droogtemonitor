# Interactief Droogtemonitor

The KNMI, the Dutch weather service, has a page to monitor the precipitation from April through the end of September. 
[This page](https://www.knmi.nl/nederland-nu/klimatologie/droogtemonitor) while informative, does not unlock the data enclosed into an explorable format. 

This Streamlit app makes the data slightly more interactive. 

## How to install

Clone this repository

    git clone https://github.com/gspeed0689/droogtemonitor.git
    cd droogtemonitor

Create a virtual environment and sync

    uv sync

Change directory into the dashboard folder and start the streamlit app. 

    cd interactief-droogtemonitor
    streamlit run Interactief-Droogtemonitor.py

## How to use

Open browser to location reported from starting command

Explore the most important years and several indexes over the dry season. 

![](./assets/interactief-droogtemonitor-01.png)

Explore the decadal averages

![](./assets/interactief-droogtemonitor-02.png)

## Future improvements

* Download the latest raw data from the KNMI
* Add a map and visualize ERA precipitation data over the years vs the most up to date data