from os import stat
from flask import Flask, redirect, url_for, render_template, request, session
import api

app = Flask (__name__)
app.secret_key = "youtube"

@app.route("/", methods= ["POST", "GET"])
def login():
    if(request.method == "GET"):
        return render_template("loginpage.html")
    else:
        session['pname'] = request.form['pl']
        print(session['pname'])
        playListName = request.form['pl']
        return redirect(url_for('display'))

@app.route("/display")
def display():
    input = session['pname'] + ' Playlist'
    # print ('input is'," ",input)
    searchplaylist=api.searchPlaylist(input)
    plDetails = api.getPLdetails(searchplaylist)
    videosInPl = api.getVideosInPL(plDetails) 
    stats = api.computeStats(videosInPl)
    durationOfPl = api.computeDurationofPlaylist(videosInPl)

    final = searchplaylist
    

    for j in plDetails:
        final[j]['plcount'] = plDetails[j]['plcount'] 
    for j in stats:
        final[j]['likes'] = stats[j]['likes']
        final[j]['viewCount'] = stats[j]['viewCount']
    for j in durationOfPl:
        final[j]['duration'] = durationOfPl[j]
        
    print(final)
    final = api.checkapi(final)
    count=1
    data = {}
    for i in final:
        data[str(count)]=final[i]
        count+=1
    print(data)
    return render_template('display.html',input = input,data=data)

#     y= getPLdetails(x,'pandas')
#     z=getVideosInPL(y)
#     computeStats(z)

if __name__ == "__main__":
    app.run(debug=True)