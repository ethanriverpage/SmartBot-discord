import LastfmAPIWrapper.LastFmWrapper as pylast
from Database.Database import Database


class Lastfm_Commands:
    """The Lastfm_Command Class

    The Lastfm_Command class contains all the commands their methods for the
    LastFm API Wrapper. It also creates its own dataframe from the Lastfm
    database table.

    """



    def __init__(self):
        self.commands = {
            "!musiclastyear": self.list_playbacks_year_ago,
            "!recentlyplayed": self.list_playbacks_24hours,
            "!toptracks": self.list_top_tracks,
            "!topartists": self.list_top_artists,
            "!playcount": self.get_playback_count,
            "!nowplaying": self.get_currently_playing,
            "!compareme": self.compareMe,
            "!rank": self.rankPlays()
        }

        self.commandDescriptions = {
            "!musiclastyear": "Tracks 1 year ago",
            "!recentlyplayed": "Recent Tracks (24hrs)",
            "!toptracks": "Top Tracks",
            "!topartists": "Top Artists",
            "!playcount": "Total plays",
            "!nowplaying": "Currently playing song",
            "!compareme": "Compare to other user",
            "!rank": "Not Implimented"
        }

        self.database = Database('LastFm')



    def get_username(self, groupme_id):
        """
        Fetches and returns a groupme user's registered lastfm username from the lastfm
        dataframe using their groupme id as the key.

        :param groupme_id: {Integer} the user's groupme id
        :return lastfm_username: {String} the users lastfm username
        """
        lastfm_username = self.database.df.loc[self.database.df['GroupMeID'] == str(groupme_id)]['username'][0]
        return lastfm_username



    def format_by_time(self, listOfTracks):
        """
        Takes in a list of pylast.Track objects and returns a string that lists
        the tracks with their given playback time.

        :param listOfTracks: {list} track objects
        :return botResponse: {String} a list of tracks with given time
        """
        botResponse = ""
        if not listOfTracks:
            botResponse = "None"
        else:
            for track in listOfTracks:
                if len(botResponse) < 900:  ### Checking if response is under the 1000 character limit ###
                    try:
                        botResponse += pylast.playbackTimeUtcToEst(track.playback_date) + "  " + str(
                            track.track.artist) + " - " + str(track.track.title) + "\r\n"
                    except UnicodeEncodeError:  ### If the track or artist title has non ascii characters ###
                        botResponse += pylast.playbackTimeUtcToEst(track.playback_date) + "  " + "Unreadable Track"
            return botResponse



    def format_by_rank(self, listOfTracks):
        """
        Takes in a list of pylast.Track objects and returns a string that lists
        the tracks with their given rank.

        :param listOfTracks: {list} track objects
        :return botResponse: {String} a list of tracks with given rank
        """
        botResponse = ""
        if not listOfTracks:
            botResponse = "None"
        else:
            rank = 1
            for item in listOfTracks:
                if len(botResponse) < 900:  ### Checking if response is under the 1000 character limit ###
                    try:
                        botResponse += str(rank) + ". " + str(item.item.artist) + " - " + str(
                            item.item.title) + " (" + str(item.weight) + " plays)" + "\r\n"
                        rank += 1
                    except UnicodeEncodeError:  ### If the track or artist title has non ascii characters ###
                        botResponse += str(rank) + ". " + "Unreadable Track" " (" + str(
                            item.weight) + " plays)" + "\r\n"
                        rank += 1

            return botResponse



    # TODO create list_playbacks()
    #  list_playbacks(self, user, period)
    #  combines all playback functions

    def list_playbacks_year_ago(self, groupme_id):
        """
        lists a users playbacks from one year ago

        :param groupme_id: {Integer} the user's groupme id
        :return: {String} A formatted list of tracks
        """
        lastfm_username = self.get_username(groupme_id)
        botResponse = "One Year Ago Tracks: @" + str(lastfm_username) + "\r\n"
        trackList = pylast.oneYearAgoTracks(lastfm_username)
        botResponse += str(self.format_by_time(trackList))
        return botResponse



    def list_playbacks_24hours(self, groupme_id):
        """
        lists a users playbacks from past 24 hours

        :param groupme_id: {Integer} the user's groupme id
        :return: {String} A formatted list of tracks
        """
        lastfm_username = self.get_username(groupme_id)
        botResponse = "Recently Played Tracks: @" + str(lastfm_username) + "\r\n"
        trackList = pylast.playbackPastDay(lastfm_username)
        botResponse += str(self.format_by_time(trackList))
        return botResponse



    def list_top_tracks(self, groupme_id, period="overall"):
        """
        lists a users top tracks from a given period

        :param groupme_id: {Integer} the user's groupme id
        :param period: {String} time period to fetch top tracks from
        :return: {String} A formatted list of top tracks
        """
        periodOptions = {
            "overall": "overall",
            "week": "7day",
            "month": "1month",
            "year": "12month"
        }

        lastfm_username = self.get_username(groupme_id)
        botResponse = "Top Tracks: @" + str(lastfm_username) + "\r\n"
        if period in periodOptions:
            topTrackList = pylast.getTopTracks(lastfm_username, periodOptions[period])
            botResponse += self.format_by_rank(topTrackList)
        else:
            botResponse = "Try: \r\n"
            for item in periodOptions:
                botResponse += "!toptracks {" + item + "}\r\n"
        return botResponse



    ### TODO post picture of top artists
    def list_top_artists(self, groupme_id, period="overall"):
        """
        lists a users top tracks from a given period

        :param groupme_id: {Integer} the user's groupme id
        :param period: {String} time period to fetch top tracks from
        :return: {String} A formatted list of top artists
        """
        periodOptions = {
            "overall": "overall",
            "week": "7day",
            "month": "1month",
            "year": "12month"
        }

        lastfm_username = self.get_username(groupme_id)
        botResponse = "Top Artists: @" + str(lastfm_username) + "\r\n"
        if period in periodOptions:
            listOfArtists = pylast.getTopArtist(lastfm_username, periodOptions[period])
            if not listOfArtists:
                botResponse += "None"
            else:
                rank = 1
                for item in listOfArtists:
                    if len(botResponse) < 900:  ### Checking if response is under the 1000 character limit ###
                        try:
                            botResponse += str(rank) + ". " + str(item.item) + " (" + str(
                                item.weight) + " plays)\r\n"
                            rank += 1
                        except UnicodeEncodeError:  ### If the track or artist title has non ascii characters ###
                            botResponse += str(rank) + ". Unreadable Artist (" + str(item.weight) + ")\r\n"
                            rank += 1
                return botResponse
        else:
            botResponse = "Try: \r\n"
            for item in periodOptions:
                botResponse += "!topartists {" + item + "}\r\n"
        return botResponse



    def get_playback_count(self, groupme_id):
        """
        fetches and returns a users total number of playbacks

        :param groupme_id: {Integer} the user's groupme id
        :return: {String} the user's total number of playbacks
        """
        lastfm_username = self.get_username(groupme_id)
        playbackCount = "Total Scrobbles: @" + str(lastfm_username) + "\r\n" + str(
            pylast.playCount(lastfm_username))
        return playbackCount



    def get_currently_playing(self, groupme_id):
        """
        fetches and returns a users currently playing song

        :param groupme_id: {Integer} the user's groupme id
        :return: {String} the user's currently playing song
        """
        lastfm_username = self.get_username(groupme_id)
        botResponse = "Currently Playing: @" + str(lastfm_username) + "\r\n"
        currentlyPlayingTrackList = pylast.getNowPlaying(lastfm_username)
        if None in currentlyPlayingTrackList:
            botResponse += "None"
        else:
            for track in currentlyPlayingTrackList:
                try:
                    botResponse += str(track.artist) + " - " + str(track.title)
                except UnicodeEncodeError:
                    botResponse += "Unreadable Track"
        return botResponse



    ### input format !compareme @Other User
    # TODO document compareme()
    def compareMe(self, groupme_id, otherUserFirstName, otherUserLastName, period="overall"):
        """

        :param groupme_id:
        :param otherUserFirstName:
        :param otherUserLastName:
        :param period:
        :return:
        """
        periodOptions = {
            "overall": "overall",
            "week": "7day",
            "month": "1month",
            "year": "12month"
        }
        if otherUserFirstName[0] == "@":
            otherUser = otherUserFirstName[1:] + " " + otherUserLastName
        else:
            otherUser = otherUserFirstName + " " + otherUserLastName
        botResponse = "Comparing: " + str(self.get_username(groupme_id)) + " & " + str(
            self.get_username(otherUser)) + "\r\n" # TODO throws exception: otherUser needs to be a groupme_id

        similarArtistList = pylast.compareUsersTopArtists(self.get_username(groupme_id),
                                                          self.get_username(otherUser),
                                                          periodInput=periodOptions[period])
        similarTracksList = pylast.compareUsersTopTracks(self.get_username(groupme_id),
                                                         self.get_username(otherUser),
                                                         periodInput=periodOptions[period])
        if len(similarArtistList) > 5:
            similarArtistList = similarArtistList[0:10]
        if len(similarTracksList) > 5:
            similarTracksList = similarTracksList[0:10]

        botResponse += "\r\nSIMILAR ARTISTS: \r\n"
        for artist in similarArtistList:
            botResponse += str(artist) + "\r\n"

        botResponse += "\r\nSIMILAR TRACKS: \r\n"
        for track in similarTracksList:
            botResponse += str(track) + "\r\n"
        return botResponse



    ### TODO rank users scrobbles ###
    def rankPlays(self):
        return "Implement Me"
