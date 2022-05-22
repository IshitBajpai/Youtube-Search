from traceback import print_tb
from googleapiclient.discovery import build
from requests import request
import os
import re
from datetime import timedelta


key = 'AIzaSyA5QDUfbdWNSjkVr-ypMYmxI2eXOyjB6sQ'
yt = build('youtube', 'v3', developerKey = key)


def searchPlaylist(search): # channelid : { playlistname Channeltitle}
    search_request = yt.search().list(
        part = 'snippet',
        maxResults = 2, 
        q =  search  # modify this later
    )
    search_response = search_request.execute()
    channel_id = {}         # stores channel id along with the playlist
    for i in search_response['items']:
        channel_id[i['snippet']["channelId"]]={ 'pltitle':i['snippet']['title'] , 'ctitle' : i['snippet']['channelTitle'] }
    print(channel_id)
    return channel_id


def getChannedetails(channel_id):
    pass

def getPLdetails(channel_id): # pass channel id dictionary
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
    #print(pl)
    return pl

def getVideosInPL (pl): # returns vid with video title and pltitle , pass above value
    plVid = {}
    for j in pl:
            nextPageToken = None
            count = 1
            platylistvidforchannel = {}
            while True:

                plVid_request = yt.playlistItems().list (
                    part = 'snippet,contentDetails,id',
                    playlistId = pl[j]['plid'],
                    maxResults = 50,
                    pageToken = nextPageToken
                )

                
                plVid_response = plVid_request.execute()
                #print(plVid_response)
                for i in plVid_response['items']:
                    platylistvidforchannel[count] = {'videoid':i['contentDetails']['videoId'] ,'videotitle': i['snippet']['title'] , 'pltitle': pl[j]['pltitle']  }
                    count += 1
            
                nextPageToken = plVid_response.get('nextPageToken')
                if(nextPageToken == None):
                    break
                
            plVid[j] = platylistvidforchannel
            

    print(plVid)
    print()
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

def computeStats(plvid):
    stats = {}
    for i in plvid:
        likes = 0
        viewCount = 0
        commentCount = 0 
        for j in plvid[i]:
            vid = plvid[i][j]['videoid']
            Vid_request = yt.videos().list (
                part = 'statistics',
                id = vid
            )
            vid_response = Vid_request.execute()
            #print(vid_response)

            likes += int(vid_response['items'][0]['statistics']['likeCount'])
            viewCount += int(vid_response['items'][0]['statistics']['viewCount'])
            commentCount += int(vid_response['items'][0]['statistics']['commentCount'])

        stats[i] = {'likes':likes,'viewCount':viewCount,'commentCount':commentCount}
    print(stats)
    return stats


def computeDurationofPlaylist(plvid): 
    durations ={}
    hour = re.compile(r'(\d+)H')
    min = re.compile(r'(\d+)M')
    sec = re.compile (r'(\d+)S')
    for i in plvid:
        total_seconds = 0 
        for j in plvid[i]:
            vid = plvid[i][j]['videoid']
            vid_request = yt.videos().list (
                part = 'contentDetails',
                id = vid
            )
            vid_response = vid_request.execute()

            duration = vid_response['items'][0]['contentDetails']['duration']
            hours = hour.search(duration)
            minutes = min.search(duration)
            seconds = sec.search(duration)

            if(hours!=None):
                hours = int(hours.group(1))
            else:
                hours=0
            if(minutes!=None):
                minutes = int(minutes.group(1))
            else:
                minutes=0
            if(seconds!=None):
                seconds = int(seconds.group(1))
            else:
                seconds = 0
          

            All_seconds = timedelta(
                hours=hours,
                minutes = minutes,
                seconds=seconds
            ).total_seconds()
            
            total_seconds += int(All_seconds)

        minutes , seconds = divmod(total_seconds,60)
        hours , minutes = divmod(minutes,60)
        total_duration = "H:"+str(int(hours))+" M:"+str(int(minutes))+" S:"+str(int(seconds))
        # print(total_duration)
        durations[i]={'duration':total_duration}
    print(durations)
    return duration

# def main():
#     # keyword = input("Enter Playlist word to search")
#     # search = keyword + " playlist"

#     x=searchPlaylist(2)
#     y= getPLdetails(x,'pandas')
#     z=getVideosInPL(y)
#     computeStats(z)
#     print()
#     computeDurationofPlaylist(z)

   

# if __name__ == "__main__":
#     main()


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
 