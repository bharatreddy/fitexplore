import pandas
import altair as alt
import sys
import sd_data_utils
import json


class SDPlotUtils(object):
    """
    A class to generate different plots
    from SD data using altair.
    """
    def __init__(self, startTime, endTime, radar,\
             fileType, filtered=False, plotParam="vel"):
        """
        setup parameters
        """
        self.startTime = startTime
        self.endTime = endTime
        self.radar = radar
        self.fileType = fileType
        self.filtered = filtered
        if plotParam not in ['vel', 'spw', 'pwr']:
            print "Choose a valid plotting parameter--> 'vel', 'spw', 'pwr'"
            return 
        self.plotParam = plotParam
        self._sdData_ = self.load_sd_df()

    def load_sd_df(self):
        """
        Get superdarn data in a DF
        """
        sdDataObj = sd_data_utils.SDDataUtils(self.startTime, self.endTime,\
                        self.radar, self.fileType, filtered=self.filtered)
        return sdDataObj.get_sd_data(saveToDisk=True)

    def full_vel_time_plot(self):
        """
        We'll generate a plot containing all the data
        in the dataframe!
        """
        # setup titles/labels
        xtitle = "Time (UT)"
        if self.plotParam == "vel":
            pltTitle = "Vel vs Time (" + self.fileType + ")"
            ytitle = "Velocity [m/s]"
        if self.plotParam == "pwr":
            pltTitle = "Power vs Time (" + self.fileType + ")"
            ytitle = "Power [dB]"
        if self.plotParam == "spw":
            pltTitle = "Sp. Width vs Time (" + self.fileType + ")"
            ytitle = "Sp. Width [m/s]"
        # generate the actual plot
        sdDF = self._sdData_[1]
        # dealing with large rows
        alt.data_transformers.enable('json')
        chart = alt.Chart(sdDF, height=400, width=600).mark_circle(size=10).encode(
            x=alt.X('utchoursminutesseconds(date):T', axis=alt.Axis(title='Time (UT)')),
            y=alt.Y('vel', axis=alt.Axis(title='Velocity [m/s]')),
            tooltip=['vel', 'spw', 'pwr']
        ).properties(
            title='Fitacf3 Vel vs time plot'
        ).interactive()
        chart.save('/tmp/t1.json')
        with open('/tmp/t1.json') as f:
            data = json.load(f)
        f.close()
        return data


if __name__ == "__main__":
    startTime = datetime.datetime(2017,12,2)
    endTime = datetime.datetime(2017,12,3)
    radar = 'bks'
    fileType = 'fitacf3'
    sdPltObj = SDPlotUtils(startTime, endTime, radar, fileType)
    xx = sdObj.get_sd_data(saveToDisk=True)        