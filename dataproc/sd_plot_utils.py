import pandas
import altair as alt
import sys
import sd_data_utils
import json
import pytz


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
        self.allParams = ['vel', 'spw', 'pwr']
        if plotParam not in self.allParams:
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
        pltTitle = self.startTime.strftime("%Y%m%d") + " (" + self._sdData_[0] + ")"
        if self.plotParam == "vel":
            ytitle = "Velocity [m/s]"
        if self.plotParam == "pwr":
            ytitle = "Power [dB]"
        if self.plotParam == "spw":
            ytitle = "Sp. Width [m/s]"
        # generate the actual plot
        sdDF = self._sdData_[1]
        # dealing with large rows
        alt.data_transformers.enable('json')
        # generate the plot
        chart = alt.Chart(sdDF, height=400, width=600).mark_circle(size=10).encode(
            x=alt.X('utchoursminutesseconds(date):T', axis=alt.Axis(title='Time (UT)')),
            y=alt.Y(self.plotParam, axis=alt.Axis(title=ytitle)),
            tooltip=['vel', 'spw', 'pwr']
        ).properties(
            title=pltTitle
        ).interactive()
        # save as json to pass on to the front end
        chart.save('/tmp/vel_time.json')
        with open('/tmp/vel_time.json') as f:
            data = json.load(f)
        f.close()
        return data

    def get_axis_label(self,param):
        """
        Depending on the param name create a label
        for the axis
        """
        if param == "vel":
            return "Velocity (m/s)"
        if param == "pwr":
            return "Power (dB)"
        if param == "spw":
            return "Spectral Width (m/s)"
        return "Unknown Param"

    def hist_sctr_cmpr_plot(self, cmprParam='spw'):
        """
        We'll generate a plot containing all the data
        in the dataframe!
        """
        # setup titles/labels
        xtitle = "Time (UT)"
        pltTitle = self.startTime.strftime("%Y%m%d") + " (" + self._sdData_[0] + ")"
        histLabel = self.get_axis_label(self.plotParam)
        histName = histLabel + ":N"
        # Now get the remaining parameter
        cmprParam = list( set( self.allParams ) - set( [self.plotParam] ) )
        # generate the actual plot
        sdDF = self._sdData_[1]
        # dealing with large rows
        alt.data_transformers.enable('json')
        # generate the plot
        # interval selection in the scatter plot
        pts = alt.selection(type="interval", encodings=["x"])
        # left panel: scatter plot
        points = alt.Chart().mark_point(filled=True, color="blue").encode(
            x=alt.X(cmprParam[0], axis=alt.Axis(title=self.get_axis_label(cmprParam[0]))),
            y=alt.Y(cmprParam[1], axis=alt.Axis(title=self.get_axis_label(cmprParam[1]))),
            color=alt.value("#1f77b4")
        ).transform_filter(
            pts.ref()
        ).properties(
            width=300,
            height=300
        )
        # right panel: histogram
        mag = alt.Chart().mark_bar().encode(
            x=histName,
            y="count()",
            color=alt.condition(pts, alt.value("#e84747"), alt.value("#1f77b4"))
        ).properties(
            selection=pts,
            width=300,
            height=300
        )
        # build the chart:
        chart = alt.hconcat(points, mag,
            data=sdDF
        ).transform_bin(
            histLabel,
            field=self.plotParam,
            bin=alt.Bin(maxbins=20)
        )
        # save as json to pass on to the front-end
        chart.save('/tmp/hist_cmpr.json')
        with open('/tmp/hist_cmpr.json') as f:
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