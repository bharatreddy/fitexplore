import datetime
import numpy
import pandas
from davitpy import pydarn
import glob
import feather
import pytz


class SDDataUtils(object):
    """
    Given a filetype fitacf/fitacf3 and fitex
    get the data from sd database and convert
    to dataframe.
    """
    def __init__(self, startTime, endTime, radar,\
             fileType, filtered=False):
        """
        setup parameters
        """
        # we'll need a timzone info to compare times
        # with pandas.
        if startTime.tzname() is None:
            self.startTime = pytz.utc.localize(startTime)
            # There is 
        else:
            self.startTime = startTime
        if startTime.tzname() is None:
            self.endTime = pytz.utc.localize(endTime)
        else:
            self.endTime = endTime
        self.radar = radar
        self.fileType = fileType
        self.filtered = filtered

    def fetch_data_ptr(self):
        """
        Fetch data using davitpy routine. Remember to fetch
        fitacf3 files, we need to use Kevin's code from the 
        develop branch in davitpy.
        """
        dataPtr = pydarn.sdio.radDataOpen(self.startTime.replace(tzinfo=None), self.radar,\
                    self.endTime.replace(tzinfo=None), filtered=self.filtered,\
                    fileType=self.fileType)
        if dataPtr is not None:
            return pydarn.sdio.radDataReadAll(dataPtr)
        return None

    def get_sd_data(self, saveToDisk=False):
        """
        Convert the data pointer from davitpy holding
        SuperDARN data to a dataframe.
        """
        # Check if we have a saved version of the DF as feather file
        # create a search pattern for the filename
        # The pattern below will not satisfy all the cases, but I'm
        # at this point assuming the start date will be the same
        fileFound = False
        fSrchPtrn = "/tmp/" + self.startTime.strftime("%Y%m%d") +\
                        "*" + self.fileType + ".feather"
        print fSrchPtrn
        # see if we can find any matching files
        for fthrFLoc in glob.iglob(fSrchPtrn):
            fthrFname = fthrFLoc.split("/tmp/")[1]
            fileStartTime = datetime.datetime.strptime( \
                        fthrFname.split("__")[0], "%Y%m%d-%H%M" )
            # assign a timezone
            fileStartTime = pytz.utc.localize(fileStartTime)
            fileEndTime = datetime.datetime.strptime( \
                        fthrFname.split("__")[1], "%Y%m%d-%H%M" )
            fileEndTime = pytz.utc.localize(fileEndTime)
            if ( (fileStartTime <= self.startTime) &\
                             (fileEndTime >= self.endTime) ):
                print "feather file found--->", fthrFLoc
                fileFound = True
                # read the file
                sdDF = feather.read_dataframe(fthrFLoc)
                # Filter the dataframe so that the starttime
                # and endtime are as input (remember the start
                # and end times could be different in the file stored)
                sdDF = sdDF[ (sdDF["date"] >= self.startTime) &\
                            (sdDF["date"] <= self.endTime)\
                                    ].reset_index(drop=True)
                # the datetime column is in UTC
                return (self.fileType, sdDF)
        print "feather file not found...reading from sd-data..."
        # If not read data from sd-data using davitpy!
        dataRecList = self.fetch_data_ptr()
        if dataRecList is None:
            return None
        # we'll create a dataframe with all the data
        # To keep things simple (at this moment), I'm
        # not using multi-indexed dataframe.
        # Initialize empty arrays for the data
        # these will later be converted to a DF
        qflgArr = numpy.empty([0])
        gateArr = numpy.empty([0])
        velArr = numpy.empty([0])
        spwArr = numpy.empty([0])
        pwrArr = numpy.empty([0])
        gflgArr = numpy.empty([0])
        dtArr = numpy.empty([0])
        bmArr = numpy.empty([0])
        for nrec, rec in enumerate(dataRecList):
        #     print numpy.array(rec.fit.qflg )
            if rec is None:
                continue
            if rec.fit is None:
                continue
            if rec.fit.v is None:
                continue
            qflgArr = numpy.concatenate( ( qflgArr,\
                                    numpy.array(rec.fit.qflg ) ) )
            gateArr = numpy.concatenate( ( gateArr,\
                                     numpy.array(rec.fit.slist ) ) )
            velArr = numpy.concatenate( ( velArr,\
                                         numpy.array(rec.fit.v ) ) )
            spwArr = numpy.concatenate( ( spwArr,\
                                         numpy.array(rec.fit.w_l ) ) )
            pwrArr = numpy.concatenate( ( pwrArr,\
                                         numpy.array(rec.fit.p_l ) ) )
            gflgArr = numpy.concatenate( ( gflgArr,\
                                         numpy.array(rec.fit.gflg ) ) )
            # date and bmnum are a little different
            dtArr = numpy.concatenate( ( dtArr,\
                            numpy.full( (len(rec.fit.qflg)), rec.time) ) )
            bmArr = numpy.concatenate( ( bmArr,\
                            numpy.full( (len(rec.fit.qflg)), rec.bmnum) ) )
            outFileType = rec.fType
        if outFileType != self.fileType:
            print "*****READING DATA FROM A DIFERENT FILE FORMAT*****"
        sdDF = pandas.DataFrame( {
            "qflg" : qflgArr,
            "gate" : gateArr,
            "vel" : velArr,
            "spw" : spwArr,
            "pwr" : pwrArr,
            "gflg" : gflgArr,
            "date" : dtArr,
            "beam" : bmArr,
            })
        # assign UTC timezone to the date columns, this becomes
        # important when you render the data in a browser!
        sdDF["date"] =  sdDF["date"].dt.tz_localize('UTC')
        # Convert int cols to int16, they are being stored as 
        # floats now! This is memory efficient!
        intCols = [ "qflg", "gate", "gflg", "beam" ]
        sdDF[intCols] = sdDF[intCols].astype(numpy.int16)
        # Now we'll try and save the DF in the /tmp/ folder
        # for future use.
        if saveToDisk:
            outDfFName = self.startTime.strftime("%Y%m%d-%H%M") + "__" +\
                     self.endTime.strftime("%Y%m%d-%H%M") +\
                      "__" + outFileType + ".feather"
            feather.write_dataframe( sdDF, "/tmp/" + outDfFName )
        # return the dataframe and fileType for plotting
        return (outFileType, sdDF)

if __name__ == "__main__":
    startTime = datetime.datetime(2017,12,2,12)
    endTime = datetime.datetime(2017,12,3,18)
    radar = 'bks'
    fileType = 'fitacf3'
    sdObj = SDDataUtils(startTime, endTime, radar, fileType)
    outDF = sdObj.get_sd_data(saveToDisk=True)