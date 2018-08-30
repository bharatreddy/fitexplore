import pandas
import altair as alt
import sd_data_utils


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
        self.plotParam = plotParam
        self._sdData_ = self.load_sd_df()

    def load_sd_df(self):
        """
        Get superdarn data in a DF
        """
        sdDataObj = sd_data_utils.SDDataUtils(self.startTime, self.endTime,\
                        self.radar, self.fileType, filtered=self.filtered)
        dataDF = sdDataObj.get_sd_data(saveToDisk=True)

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
        chart = alt.Chart(dfx).mark_circle(size=60).encode(
            x=alt.X('time', axis=alt.Axis(title='Time (UT)')),
            y=alt.Y('vel', axis=alt.Axis(title='Velocity [m/s]')),
            color='beam',
            tooltip=['vel', 'spw', 'pwr']
        ).properties(
            title='Fitacf3 Vel vs time plot'
        ).interactive()
        return chart.to_json()


if __name__ == "__main__":
    startTime = datetime.datetime(2017,12,2)
    endTime = datetime.datetime(2017,12,3)
    radar = 'bks'
    fileType = 'fitacf3'
    sdPltObj = SDPlotUtils(startTime, endTime, radar, fileType)
    xx = sdObj.get_sd_data(saveToDisk=True)        