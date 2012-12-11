#Extractor Script

For the Bubble Zero Researchers to load Cheng's txt files into IPython in order to plot, manipulate, and export datafiles

##Getting Started
This code is designed to be utilized through an IPython console. The easiest way to get started is to download the free [Enthought Python Distribution (EPD)](http://www.enthought.com/products/epd_free.php) which includes all of the libraries required by the engine.

After installation of EPD, the `pandas` library will need to be upgraded to at least [Version 0.90](http://pandas.pydata.org/).

From the IPython console, navigate to the source code folder and run:

`run -t bubbledataextractor.py`

If the script executes without errors then your IPython console will have loaded a Pandas DataTable named `Desired Data` which can be exported, plotted, etc using Pandas data manipulation techniques.

A couple of examples:

To export a csv file:
    `DesiredData.to_csv('DesiredDataOutput.csv')`
To use matploblib within Pandas to plot:
    `DesiredData.plot(subplots=True)`

