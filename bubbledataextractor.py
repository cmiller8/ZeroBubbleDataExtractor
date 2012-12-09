import pandas as pd
import os

#Location of the Cheng-style txt files from the data collection system
ZeroDataPath = '/Users/millerc/Dropbox/LowEx-BubbleZERO/Bubble Data'

#Location of code extractors and configuration csv - please specify which points are of interest and the time range
ExtractorCodePath = '/Users/millerc/Dropbox/CODE/ZeroBubbleData-V2'
ExtractorConfigFile = 'ExtractorConfigurationSpreadsheet - Sheet1.csv'

#Specify the FCL Bubble Point List. This spreadsheet must be fully accurate in order for the proper points to be extracted
#Please check this spreadsheet if there are any data inaccuracies
FCLBubblePointList = 'FCLBubbleZeroPointList - PointList.csv'

#Navigate to the folder with the extractor config and library file and open into panda dataframes
os.chdir(ExtractorCodePath)
ExtractorConfig = pd.read_csv(ExtractorConfigFile, parse_dates=[1,2])
PointLibrary = pd.read_csv(FCLBubblePointList,index_col='ClaytonDiagramAbbrev')

#Navigate to Bubble Zero Dataset folder
os.chdir(ZeroDataPath)

#Create a dictionary which maps the way pandas creates column labels and the channel numbers found in the point list
#spreadsheet
columnmapping = {1:'X1',2:'X2',3:'X3',4:'X4',5:'X5',6:'X6',7:'X7',8:'X8',9:'X9',10:'X10',11:'X11',12:'X12',13:'X13',
                 14:'X14',15:'X15',16:'X16'}

#Loop through the desired points in the extractor file, open the txt files, and extract the desired data to the dataframe
i=0
while i < len(ExtractorConfig.DesiredPoint):
#    print ExtractorConfig.ix[i]['DesiredPoint']

    #Get the txt filename and channel that the current desired point can be found in. If that point doesn't exist then throw error and continue
    #TODO: Add a more robust ability for the code to recognize whether a file has already been loaded once
    try:
        ClaytonLabel = ExtractorConfig.ix[i]['DesiredPoint']
        File = PointLibrary.get_value(ClaytonLabel,'StoreFilename')
        Channel = PointLibrary.get_value(ClaytonLabel,'Channel')
    except:
        print 'Error: Your Desired Point: '+ClaytonLabel+' isnt found in the Pointlist'
        i+=1; LastFileLoaded = 'None'
        continue

    if File != LastFileLoaded:
        print "Loading "+ClaytonLabel+" from "+ File + " Channel "+str(Channel)
        try:
            TempFileLoad = pd.read_csv(File,sep=';',header=None,index_col=0,parse_dates=True,na_values='NC')
        except IOError as e:
            print 'Error in loading Cheng file: '+str(e)
            i+=1;
            continue

    #Pull out the desired point and truncate the dates according to the config file
    DesiredPoint = TempFileLoad[columnmapping[Channel]].truncate(before=ExtractorConfig.TimeRangeBegin[i],
        after=ExtractorConfig.TimeRangeEnd[i])
#    DesiredPoint = DesiredPoint

    #If this is the first time loaded then configure the DesiredData frame, else merge the new data into Desired
    try:
        DesiredData
    except NameError:
        DesiredData = pd.DataFrame(DesiredPoint,columns=[ClaytonLabel])
    else:
        DataAdd = pd.DataFrame(DesiredPoint,columns=[ClaytonLabel])
        DesiredData = pd.merge(DesiredData,DataAdd,left_index=True,right_index=True,how='outer')
    print 'Finished Loading '+ClaytonLabel
    LastFileLoaded = File
    i+=1

os.chdir(ExtractorCodePath)


