from flask import Flask, render_template, request, jsonify
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

if __name__ == "__main__":
    app.debug=True
    app.run()