from flask import Flask, render_template, request

import requests
import json
import urllib2
import re

app = Flask(__name__)

@app.route('/')
def home():
    #return "PATTERN RECOGNITION IN GIST FILE"
    
    response = "Respose to the API call"
    
    req = buildAPIRequest("mssalemi")
    resp = makeGETRequest(req)
    response += ": " + str(resp.status_code)
    
    return render_template("index.html")

@app.route('/results', methods = ['POST'])
def results():
    results = "Results: "
    
    if request.method == 'POST':
        
        username = request.form["username"]
        API_request = buildAPIRequest(username)
        response = makeGETRequest(API_request)
        
        if (response.status_code == 200):
            results += str(response.status_code) + " - Username Found!"
        else:
            results += "'" + request.form["username"] + "' is not found!"
            return render_template("results.html", text=results)

        ### Works up to here
        gists = json.loads(response.text)
        
        for gist in gists:
            for key, value in gist["files"].iteritems():
                results += patternFoundInResponse(request.form["pattern"], value["raw_url"])
                results += " @ document ' " + str(key) + " '"
            
            results += "_____________________________"
        
        return render_template("results.html", text=results)

    else:
        return "results coult not be found"


def buildAPIRequest(username):
    return "https://api.github.com/users/" + username+ "/gists"

def makeGETRequest(api_request):
    return requests.get(api_request)

def patternFoundInResponse(pattern, URL):
    content = urllib2.urlopen(URL).read()
    matches = re.findall(pattern, content)
    
    if (len(matches) > 0):
        return "Pattern Found"
    else:
        return "No Pattern Found"

