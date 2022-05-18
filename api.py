from traceback import print_tb
from googleapiclient.discovery import build
from requests import request

key = 'AIzaSyA5QDUfbdWNSjkVr-ypMYmxI2eXOyjB6sQ'
yt = build('youtube', 'v3', developerKey = key)


def searchPlaylist(search): # channelid : { playlistname Channeltitle}
    search_request = yt.search().list(
        part = 'snippet',
        maxResults = 2, 
        q = 'pandas playlist'   # modify this later
    )
    search_response = search_request.execute()
    channel_id = {}         # stores channel id along with the playlist
    for i in search_response['items']:
        channel_id[i['snippet']["channelId"]]={ 'pltitle':i['snippet']['title'] , 'ctitle' : i['snippet']['channelTitle'] }
    print(channel_id)
    return channel_i


def getChannedetails(channel_id):
    pass

def getPLdetails(channel_id,keyword): # pass channel id dictionary
    pl = {} 
    for i in channel_id:
        print('channel id :',i)
        pl_request = yt.playlists().list(
            part = 'snippet,contentDetails',
            channelId = i ,
            maxResults = 100
        )
        pl_response = pl_request.execute()   # all playlist now filter with the help of keyword
        for j in pl_response['items']:
            #print('plylist name :',j['snippet']['title'])
            if ( channel_id[i]['pltitle'] == j['snippet']['title'] ):
                pl[i] =  { 'plid' : j['id'] , 'pltitle' : j['snippet']['title'] , 'plcount': j['contentDetails']['itemCount']}
                #print(j['id']," : ",j['snippet']['title'] )
    #print(pl_response)
    print(pl)
    return pl

def getVideosInPL (pl): # returns vid with video title and pltitle
    for j in pl:
            plVid_request = yt.playlistItems().list (
                part = 'snippet,contentDetails,id',
                playlistId = pl[j]['plid']
            )

            plVid = {}
            plVid_response = plVid_request.execute()
            for i in plVid_response['items']:
                plVid[i['contentDetails']['videoId']] = {'videotitle': i['snippet']['title'] , 'pltitle': pl[j]['pltitle']  }
    print(plVid)
    return plVid

def computelikes(plvid):
    for i in plvid:
        inital_pl = plvid[i]['pltitle']
        break
    likes = 0
    viewCount = 0
    commentCount = 0 
    videoCount = 0

    d ={}
    for i in plvid:
        if(inital_pl != plvid[i]['pltitle']):
            d['inital_pl']  
            inital_pl = plvid[i]['pltitle']
            likes = 0
            viewCount = 0
            commentCount = 0 
            videoCount = 0

        if(inital_pl == plvid[i]['pltitle']):
            videoCount += 1
            Vid_request = yt.playlistItems().list (
                part = 'statistics',
                id = i
            )
            likes += i['statistics']['likeCount']
            viewCount += i['statistics']['viewCount']
            commentCount += i['statistics']['commentCount']


def displayall (): # number of videos , channel name , total time , 
    pass

def main():
    # keyword = input("Enter Playlist word to search")
    # search = keyword + " playlist"

    x=searchPlaylist(2)
    y= getPLdetails(x,'pandas')
    getVideosInPL(y)

   

if __name__ == "__main__":
    main()


""" 
1. Build API
2. Sned Request to API
3. Execute the request

# request = yt.channels().list(
#     part = 'statistics',
#     forUsername = 'sentdex'
# )
# response = request.execute()

"""
 