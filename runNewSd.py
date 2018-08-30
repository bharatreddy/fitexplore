from flask import Flask, render_template, request, jsonify
import sd_plot_utils
app = Flask(__name__)

@app.route("/")
def starter():
    return render_template('index.html')

@app.route("/<pagename>")
def regularpage( pagename=None ):
    """
    if route not found
    """
    return "No such page as " + pagename + " please go back!!! "    

### Altair Data Routes
@app.route("/defaultplot")
def data_bar():
	startTime = datetime.datetime(2017,12,2)
    endTime = datetime.datetime(2017,12,3)
    radar = 'bks'
    fileType = 'fitacf3'
    sdPltObj = sd_plot_utils.SDPlotUtils(startTime, endTime, radar, fileType)
    return sdPltObj.full_vel_time_plot()

if __name__ == "__main__":
    app.debug=True
    app.run()