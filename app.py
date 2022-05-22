from flask import Flask, redirect, url_for, render_template, request, session
import api

app = Flask (__name__)
app.secret_key = "youtube"

@app.route("/", methods= ["POST", "GET"])
def login():
    if(request.method == "GET"):
        return render_template("loginpage.html")
    else:
        session['pname'] = request.form
        print(session)
        playListName = request.form['pl']
        return playListName

@app.route("/display")
def display():
    input = session['pname'] + ' playlist'
    searchPlaylist=api.searchPlaylist(input)
    plDetails = api.getPLdetails(searchPlaylist)
    videosInPl = api.getVideosInPL(plDetails) 
    stats = api.computeStats(videosInPl)
    durationOfPl = api.computeDurationofPlaylist(videosInPl)


    

#     y= getPLdetails(x,'pandas')
#     z=getVideosInPL(y)
#     computeStats(z)

if __name__ == "__main__":
    app.run(debug=True)