from traceback import print_tb
from googleapiclient.discovery import build
from requests import request
import os
import re
from datetime import timedelta


key = 'AIzaSyA5QDUfbdWNSjkVr-ypMYmxI2eXOyjB6sQ'
yt = build('youtube', 'v3', developerKey=key)


def searchPlaylist(search):  # channelid : { playlistname Channeltitle}
    search_request = yt.search().list(
        part='snippet',
        maxResults=3,
        q=search  # modify this later
    )
    search_response = search_request.execute()
    channel_id = {}         # stores channel id along with the playlist
    for i in search_response['items']:
        channel_id[i['snippet']["channelId"]] = {
            'pltitle': i['snippet']['title'], 'ctitle': i['snippet']['channelTitle']}
    # print(channel_id)
    return channel_id


def getPLdetails(channel_id):  # pass channel id dictionary
    pl = {}
    for i in channel_id:
        # print('channel id :',i)
        pl_request = yt.playlists().list(
            part='snippet,contentDetails',
            channelId=i,
            maxResults=50
        )
        # all playlist now filter with the help of keyword
        pl_response = pl_request.execute()
        for j in pl_response['items']:
            # print('plylist name :',j['snippet']['title'])
            if (channel_id[i]['pltitle'] == j['snippet']['title']):
                pl[i] = {'plid': j['id'], 'pltitle': j['snippet']
                    ['title'], 'plcount': j['contentDetails']['itemCount']}
                # print(j['id']," : ",j['snippet']['title'] )
    # print(pl_response)
    # print(pl)
    return pl


def getVideosInPL(pl):  # returns vid with video title and pltitle , pass above value
    plVid = {}
    for j in pl:
            nextPageToken = None
            count = 1
            platylistvidforchannel = {}
            while True:

                plVid_request = yt.playlistItems().list(
                    part='snippet,contentDetails,id',
                    playlistId=pl[j]['plid'],
                    maxResults=50,
                    pageToken=nextPageToken
                )

                plVid_response = plVid_request.execute()
                # print(plVid_response)
                for i in plVid_response['items']:
                    platylistvidforchannel[count] = {
                        'videoid': i['contentDetails']['videoId'], 'videotitle': i['snippet']['title'], 'pltitle': pl[j]['pltitle']}
                    count += 1

                nextPageToken = plVid_response.get('nextPageToken')
                if(nextPageToken == None):
                    break

            plVid[j] = platylistvidforchannel

    # print(plVid)
    # print()
    return plVid


def computeStats(plvid):
    stats = {}
    for i in plvid:
        count = 0
        likes = 0
        viewCount = 0
        commentCount = 0
        for j in plvid[i]:
            count += 1
            vid = plvid[i][j]['videoid']
            Vid_request = yt.videos().list(
                part='statistics',
                id=vid
            )
            vid_response = Vid_request.execute()
            print(vid_response['items'])

            # some error here --?    
            likes += int(vid_response['items'][0]['statistics']['likeCount'])
            viewCount += int(vid_response['items']
                                [0]['statistics']['viewCount'])
            commentCount += int(vid_response['items']
                                    [0]['statistics']['commentCount'])

        likes = int(likes/count)
        viewCount = int(viewCount/count)
        stats[i] = {'likes': likes, 'viewCount': viewCount,
            'commentCount': commentCount}
    # print(stats)
    return stats


def computeDurationofPlaylist(plvid):
    durations = {}
    hour = re.compile(r'(\d+)H')
    min = re.compile(r'(\d+)M')
    sec = re.compile(r'(\d+)S')
    for i in plvid:
        total_seconds = 0
        for j in plvid[i]:
            vid = plvid[i][j]['videoid']
            vid_request = yt.videos().list(
                part='contentDetails',
                id=vid
            )
            vid_response = vid_request.execute()

            duration = vid_response['items'][0]['contentDetails']['duration']
            hours = hour.search(duration)
            minutes = min.search(duration)
            seconds = sec.search(duration)

            if(hours != None):
                hours = int(hours.group(1))
            else:
                hours = 0
            if(minutes != None):
                minutes = int(minutes.group(1))
            else:
                minutes = 0
            if(seconds != None):
                seconds = int(seconds.group(1))
            else:
                seconds = 0

            All_seconds = timedelta(
                hours=hours,
                minutes=minutes,
                seconds=seconds
            ).total_seconds()

            total_seconds += int(All_seconds)

        minutes, seconds = divmod(total_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        total_duration = "H:"+str(int(hours))+" M:" + \
                                  str(int(minutes))+" S:"+str(int(seconds))
        # print(total_duration)
        durations[i] = total_duration
    # print(durations)
    return durations


def getComments(plvid):
    comments = {}
    for i in plvid:
        for j in plvid[i]:
            vid = plvid[i][j]['videoid']
            comments_request = yt.commentThreads().list(
                part='snippet',
                videoId=plvid[i][j]['videoid']
            )
            comment_response = comments_request.execute()
            for item in comment_response['items']:
                print(item['snippet']['topLevelComment']
                      ['snippet']['textDisplay'])
                print()

        # print(plvid[i])
        # for j in plvid[i]:
        #     print(plvid[i][j]['videoid'])
            # comments_request = yt.commentThreads().list (
            #     part = 'snippet',
            #     videoId = plvid[i][j]['videoid']
            # )
        #     comment_response = comments_request.execute()
        #     for i in comment_response['items']:
        #         print (i['snippet'])
        #         print()


def checkapi(final):  # checks for single videos
    print(final)
    hour = re.compile(r'(\d+)H')
    min = re.compile(r'(\d+)M')            
    sec = re.compile(r'(\d+)S')
    for i in final:
        if 'plcount' not in final[i]:
                vid = ''
                search_request = yt.search().list(
                    part='snippet',
                    channelId=i,
                    q=final[i]['pltitle']  # modify this later
                )
                search_response = search_request.execute()
                for j in search_response['items']:
                    if(j['snippet']['title'] == final[i]['pltitle']):
                        vid = j['id']['videoId']
                        break

                Vid_request = yt.videos().list(
                            part='statistics,contentDetails',
                            id=vid
                        )
                vid_response = Vid_request.execute()
                likes = int(vid_response['items'][0]['statistics']['likeCount'])
                viewCount = int(vid_response['items'][0]['statistics']['viewCount'])
                duration = vid_response['items'][0]['contentDetails']['duration']
                hours = hour.search(duration)
                minutes = min.search(duration)
                seconds = sec.search(duration)
                if(hours != None):
                    hours = int(hours.group(1))
                else:
                    hours = 0
                if(minutes != None):
                    minutes = int(minutes.group(1))
                else:
                    minutes = 0
                if(seconds != None):
                    seconds = int(seconds.group(1))
                else:
                    seconds = 0
                print('final','\n',final)
                final[i]['plcount']=1
                final[i]['likes']=likes
                final[i]['viewCount']=viewCount
                final[i]['duration']=str(hours)+"H "+str(minutes)+"M "+str(seconds)+"S"
                
    return final


def main():
    # keyword = input("Enter Playlist word to search")
    # input = 'Pandas' + " playlist"
    # searchplaylist=searchPlaylist(input)
    # plDetails = getPLdetails(searchplaylist)
    # videosInPl = getVideosInPL(plDetails)
    # stats = computeStats(videosInPl)
    # durationOfPl = computeDurationofPlaylist(videosInPl)

    # final = searchplaylist
    # for j in plDetails:
    #     final[j]['plcount'] = plDetails[j]['plcount']
    # for j in stats:
    #     final[j]['likes'] = stats[j]['likes']
    #     final[j]['viewCount'] = stats[j]['viewCount']
    # for j in durationOfPl:
    #     final[j]['duration'] = durationOfPl[j]

    # print(final)

    hour = re.compile(r'(\d+)H')
    min = re.compile(r'(\d+)M')
    sec = re.compile(r'(\d+)S')
    vid = ''
    search_request = yt.search().list(
        part='snippet',
        channelId='UCeVMnSShP_Iviwkknt83cww',
        q='Python Pandas Tutorial in Hindi'  # modify this later
    )
    search_response = search_request.execute()
    for i in search_response['items']:
        if(i['snippet']['title'] == 'Python Pandas Tutorial in Hindi'):
            print(i['snippet']['title'])
            print(i['id']['videoId'])
            vid = i['id']['videoId']
            break

    Vid_request = yt.videos().list(
                part='statistics,contentDetails',
                id=vid
            )
    vid_response = Vid_request.execute()
    likes = int(vid_response['items'][0]['statistics']['likeCount'])
    viewCount = int(vid_response['items'][0]['statistics']['viewCount'])
    duration = vid_response['items'][0]['contentDetails']['duration']
    hours = hour.search(duration)
    minutes = min.search(duration)
    seconds = sec.search(duration)
    if(hours != None):
        hours = int(hours.group(1))
    else:
        hours = 0
    if(minutes != None):
        minutes = int(minutes.group(1))
    else:
        minutes = 0
    if(seconds != None):
        seconds = int(seconds.group(1))
    else:
        seconds = 0
    print(hours,minutes,seconds,likes,viewCount)
        # if('Python Pandas Tutorial in Hindi' == i[snippe])
    # print(search_response['items'][0]['id']['videoId'])

    

   

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
 