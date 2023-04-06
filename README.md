# Visual Analytics Dashboard
Welcome to the group 13 visual analytics dashboard repository!
This dashboard is created using [Dash](https://dash.plotly.com/introduction) and [plotly express](https://plotly.com/python/plotly-express/) for the visualization elements and used pandas/numpy for data processing. No other plots were copied from external sources and all plots were created specifically for this project using the aforementioned frameworks. The data used for this project is from the [2017 VAST challenge](http://visualdata.wustl.edu/varepository/VAST%20Challenge%202017/challenges/Grand%20Challenge/)

## Set-up

1. install [**python 3.10+**](https://www.python.org/downloads/release/python-3100/)
2. Install pip dependencies 
`pip install -r requirements.txt`
3. run app.py: `python app.py`
4. go to `localhost:8050` in your browser of choice.


## File structure

data/MC1 containts the raw data from the challenge, processed data directly read in by the visualizations, and files that did the pre-processing or filtered the data at runtime.

in src/notebooks files are found that were used for testing and analyzing the association rules generated.

src/plots contains the files that produce the plots visible on the visual analytics tool.

src/menu.py generates the page elements that hold the filters and title.

app.py is the main file from which the project needs to be run. This holds the HTML structure for the page, as well as the callbacks that drive the interaction and behaviour of the visualizations.