from flask import Flask, render_template, request, jsonify
import os
import sys
import datetime
module_path = os.path.abspath(os.path.join('dataproc/'))
if module_path not in sys.path:
    sys.path.append(module_path)
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
@app.route("/fitbaseplot")
def generate_base_plot():
    startTime = datetime.datetime(2017,12,2,2)
    endTime = datetime.datetime(2017,12,2,3)
    radar = 'bks'
    fileType = 'fitacf3'
    sdPltObj = sd_plot_utils.SDPlotUtils(startTime, endTime, radar, fileType)
    return jsonify(sdPltObj.full_vel_time_plot())


@app.route("/updatebaseplot", methods=['POST'])
def update_plot():
    startTime = datetime.datetime(2017,12,2,2)
    endTime = datetime.datetime(2017,12,2,3)
    radar = 'bks'
    fileType = 'fitacf3'
    if request.method == 'POST':
       inpParams = request.get_json()
       print "hello----->"
       print inpParams
    sdPltObj = sd_plot_utils.SDPlotUtils(startTime, endTime, radar, fileType)
    return jsonify(sdPltObj.full_vel_time_plot())

@app.route("/histcmprplot")
def generate_hist_plot():
    startTime = datetime.datetime(2017,12,2,2)
    endTime = datetime.datetime(2017,12,2,3)
    radar = 'bks'
    fileType = 'fitacf3'
    sdPltObj = sd_plot_utils.SDPlotUtils(startTime, endTime, radar, fileType)
    return jsonify(sdPltObj.full_vel_time_plot())    

if __name__ == "__main__":
    app.debug=True
    app.run(host= '0.0.0.0',port=5000)