import datetime
import numpy
import pandas
from davitpy import pydarn


class SDUtils(object):
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
        self.startTime = startTime
        self.endTime = endTime
        self.radar = radar
        self.fileType = fileType
        self.filtered = filtered

    def fetch_data(self):
        """
        Fetch data using davitpy routine. Remember to fetch
        fitacf3 files, we need to use Kevin's code from the 
        develop branch in davitpy.
        """
        dataPtr = pydarn.sdio.radDataOpen(self.startTime, self.radar,\
                    self.endTime, filtered=self.filtered,\
                    fileType=self.fileType)
        if dataPtr is not None:
            return pydarn.sdio.radDataReadAll(dataPtr)
        return None

    def convert_to_df(self):
        """
        Convert the data pointer from davitpy holding
        SuperDARN data to a dataframe.
        """
        dataRecList = self.fetch_data()
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
        # Convert int cols to int16, they are being stored as 
        # floats now! This is memory efficient!
        intCols = [ "qflg", "gate", "gflg", "beam" ]
        sdDF[intCols] = sdDF[intCols].astype(numpy.int16)
        print sdDF.head()
        print "------------------"
        print sdDF.dtypes

if __name__ == "__main__":
    startTime = datetime.datetime(2017,12,2)
    endTime = datetime.datetime(2017,12,3)
    radar = 'bks'
    fileType = 'fitacf3'
    sdObj = SDUtils(startTime, endTime, radar, fileType)
    sdObj.convert_to_df()