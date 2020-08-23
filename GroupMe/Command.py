from datetime import datetime
from groupy.client import Client
from Token import groupyToken, groupy_id, bot_id
import LastFm
from GroupMe import Users
client = Client.from_token(groupyToken)
group = client.groups.get(groupy_id)
Users = Users.Users


class Command:
    def __init__(self):
        self.commands = {
            "!stop": self.stop,
            "!commands": self.commandList,
            "!musiclastyear": self.musicLastYear,
            "!musicrecents": self.musicRecents,
            "!toptracks": self.TopTracks,
            "!playcount": self.playCount,
            #"!rankscrobbles": self.rankScrobbles

        }

        self.commandDescriptions = {
            "!stop": "terminates bot",
            "!commands": "Lists all commands",
            "!musiclastyear": "Tracks 1 year ago",
            "!musicrecents": "Recent Tracks (24hrs)",
            "!toptracks": "Overall Top Tracks",
            "!playcount": "Total plays",
            #"!rankscrobbles": "Scrobble Ranks"
        }


    ### Function handles each command and creates the correct response ###
    def handle_command(self, command, user):
        response= ""
        if command in self.commands:
            if command == "!stop":
                return "!stop"
            else:
                response += str(self.commands[command](user))
                print(str(datetime.now().hour) + ":" + str(datetime.now().minute) + " " + user + ": " + command)
                client.bots.post(bot_id=bot_id, text=str(response))
                return response


    ### Command stops the bot ###
    def stop(self, user):
        stop = "!stop"
        return stop


    ### Command lists all of the available commands ###
    def commandList(self, user):
        response = "Commands:\r\n"

        for command in self.commandDescriptions:
            response += "-" + command + ": " + self.commandDescriptions[command] + "\r\n"

        return response


    ### Command lists music that was listened to one year ago ###
    def musicLastYear(self, user):
        response = "One Year Ago Tracks: \r\n"
        trackList = LastFm.oneYearAgoTracks(str(Users.usersLastFM[user]))
        if not trackList:
            response+= "None"
        else:
            for item in trackList:
                if len(response) < 950: ### Checking if response is under the 1000 character limit ###
                    try:
                        response += str(item.playback_date)[13:] + ": " + str(item.track.artist) + " - " + str(item.track.title) + "\r\n"
                    except UnicodeEncodeError: ### If the track or artist title has non ascii characters ###
                        response += str(item.playback_date)[13:] + ": " + str(item.playback_date) + "Unreadable Track"
        return response


    ### Command lists music from the past 24 hours ###
    def musicRecents(self, user):
        response = "Recently Played Tracks: \r\n"
        trackList = LastFm.lastDayTracks(str(Users.usersLastFM[user]))
        if not trackList:
            response+= "None"
        else:
            for item in trackList:
                if len(response) < 950:      ### Checking if response is under the 1000 character limit ###
                    try:
                        response += str(item.playback_date)[13:] + ": " + str(item.track.artist) + " - " + str(item.track.title) + "\r\n"
                    except UnicodeEncodeError:   ### If the track or artist title has non ascii characters ###
                        response += str(item.playback_date)[13:] + ": " + str(item.playback_date) + "Unreadable Track"
                else:
                    return response
        return response


    ### Command lists top tracks of all time ###
    ### TODO odify to allow user to select interval  ###
    def TopTracks(self, user):
        response = "Top Tracks: \r\n"
        trackList = LastFm.topTracks(str(Users.usersLastFM[user]))
        if not trackList:
            response+= "None"
        else:
            counter = 1
            for item in trackList:
                if len(response) < 950: ### Checking if response is under the 1000 character limit ###
                    try:
                            response += str(counter) + ". " + str(item.item.artist) + " - " + str(item.item.title) + "\r\n"
                            counter+=1
                    except UnicodeEncodeError:  ### If the track or artist title has non ascii characters ###
                            response += str(counter) + ". " + "Unreadable Track"
                            counter+=1
                else:
                    return response

        return response


    def playCount(self, user):
        response = "Total Scrobbles: " + str(LastFm.playCount(str(Users.usersLastFM[user])))
        return response

    ### TODO ranking scrobbles of users ###
    #def rankScrobbles(self):








