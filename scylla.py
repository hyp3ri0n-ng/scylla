#!/var/www/scylla/scyllaenv/bin/python

import sys
sys.path.insert(0, '/var/www/scylla')
sys.path.insert(0, '/var/www/scylla/scyllaenv/lib/python3.5/site-packages')
from flask import Flask, jsonify, request, render_template, url_for
app = Flask(__name__)
import subprocess
from sh import ls
import json
#from base58 import b58encode
import os
from hurry.filesize import size
from functools import wraps
from flask import request, Response
from operator import itemgetter
from json2html import json2html
import glob
import requests
from flask import jsonify

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'sammy' and password == 'BasicPassword!'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

#@app.route('/regex', methods = ["POST"])
#def submit_name_regex():
#
    #request.getdata()
#    request_json = json.loads(request.data.decode('utf-8'))
#    regex = request_json["regex"]
#    print(request_json)
#    subprocess.Popen("/usr/bin/nohup find /home/ubuntu/all_unzipped -type f -exec /bin/grep " + regex + " {} + > /var/www/html/results/" + b58encode(regex).decode('utf-8'), shell=True)
#    return "h'ok"

#@app.route("/status")
def check_status():

    _dir = ls("-alhS", "/var/www/")
#    print(_dir)
    return str(_dir)

#@app.route("/grab")
def grab():
    f = open("/var/www/html/results/" + request.args.get("wut"))
    return f.read()

#@app.route("/")
#TODO: TURNED OFF AUTH
#@requires_auth
def index():
    
    user_agent = request.headers.get('User-Agent').lower()

    if "wget" in user_agent or "curl" in user_agent or "aria" in user_agent:
        return "Using cli tools to download all databases is discouraged. You are encouraged to download in browser. If this is not possible I would simply ask that you open up a browser with scylla.sh (to allow cryptomining) while you do so. Note: this is a simple user-agent string check, to bypass this message simply falsify your user-agent header to a common browser." ,409

@app.route("/")
@app.route("/search")
def search():
    size = 100
    _params = {"q" : request.args.get("q", default="*:*"), "size" : request.args.get("size", default="20"), "from" : request.args.get("from", default=0)}
    r = requests.get("http://localhost:9200/pw_data/_search", params = _params)

    if ":" not in _params["q"]:
        return "<h1> 500 Internal Server Error.</h1> You do not appear to be using Solr/Lucene query syntax.", 500
    
    #print(_params)
    #print(r.url)
    
    json_hits_num = r.json()["hits"]["total"]["value"]
    json_hits_raw = r.json()["hits"]["hits"]

    if 'Accept' in request.headers and request.headers['Accept'] == 'application/json':
        return jsonify(json_hits_raw)
    
    json_hits_filtered = [x["_source"] for x in json_hits_raw]
    print(json.dumps(json_hits_filtered))

    all_keys = []
    for hit in json_hits_filtered:
        all_keys += hit.keys()
    all_keys = list(set(all_keys))

    html = "<table id=\"results\">"
    html += "<tr>"
    for key in all_keys:
        html += "<th>" + key + "</th>"
    html += "</tr>"

    #TODO: this needs a helper function
    for hit in json_hits_filtered:
        html += "<tr>"
        for key in all_keys:
            print(key, hit)            
            try:
                html += "<th>" + hit[key] + "</th>"
            except:                
                html += "<th>" + "null" + "</th>"
        html += "</tr>"

    html += "</table>"
    
    #json_hits_html = json2html.convert(json = json.dumps(json_hits_filtered), table_attributes = 'id="search-table"')

    pages = int(json_hits_num/size)

    dbs = glob.glob("/home/ubuntu/bighd/normalized/07june_normed/*")
    dbs = [os.path.basename(db).split(".")[0] for db in dbs if "all" not in db]
    dbs = list(set(dbs))

    try:
        fields = requests.get("http://localhost:9200/pw_data/_mapping").json()["pw_data"]["mappings"]["properties"].keys()
    except KeyError:
        fields = []

#    print(_params)
    return render_template("index.html", params = _params, hits_num = json_hits_num, fields = fields, pages = range(0, pages), es_url = r.url, size = size, dbs = dbs, html_results = html )
    

if __name__ == "__main__":
    app.run(host = "0.0.0.0", threaded=True, port=8082, debug=True)
