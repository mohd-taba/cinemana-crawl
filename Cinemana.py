import requests

seasonAPI = "https://cinemana.shabakaty.com/api/android/videoSeason/id/{season_id}"
filesAPI = "https://cinemana.shabakaty.com/api/android/transcoddedFiles/id/{episode_id}"
videoInfoAPI = "https://cinemana.shabakaty.com/api/android/allVideoInfo/id/{episode_id}"
import pdb

class Episode:
    def __init__(self, ID, episodeNumber, seasonNumber, showID, showName):
        self.ID = ID
        self.episodeNumber = episodeNumber
        self.seasonNumber = seasonNumber
        self.showID = showID
        self.url_dict = {}
        self.subs = {}
        r = requests.get(filesAPI.format(episode_id=self.ID))
        rr = requests.get(videoInfoAPI.format(episode_id=self.ID))
        jj = rr.json()
        j = r.json()
        for url in j:
            self.url_dict[url['resolution']] = url['videoUrl']
        try:
            for url in jj['translations']:
                if url['extention'] == 'srt':
                    self.subs[url['name']] = url['file']
        except:
            pass
            

class Show:
    def __init__(self, url):
        self.url = url
        self.ID = self.getID(self.formatString(url))
        self.episodes = []
        self.title = ""
        r = requests.get(seasonAPI.format(season_id=self.ID))
        for episode in r.json():
            self.title = episode["en_title"]
            self.episodes.append(Episode(episode["nb"], episode["episodeNummer"], episode["season"], episode["rootSeries"], episode["en_title"]))
        
    def formatString(self, string):
        return string.split("/")[-1] if string.split("/")[-1] != "" else string.split("/")[-2]

    def getID(self, string):
        if string.find("?"):
            return string.split("?")[0]
        else:
            return string

    def WriteToCrawlJob(self):
        """Function to create a jDownloader CrawlJob file, filename being the season followed by episode number."""
        path = r"C:\Users\NameTBA\Documents\FolderWatch\{filename}.crawljob"
        f = open(path.format(filename=self.ID),'w')
        for episode in self.episodes:
            for definition, url in episode.url_dict.items():
                f.write('->NEW ENTRY<-\n    text={link}\n    filename=[{defi}] - {pkgn} - S{seasonn}E{epsn}.mp4\n    packageName={pkgn}\n'.format(link = url, defi = definition, epsn = episode.episodeNumber.zfill(2),seasonn = episode.seasonNumber.zfill(2) , pkgn = self.title))
        f.close()

def main():
    while True:
        s = Show(input("Cinemana URL?\n"))
        s.WriteToCrawlJob()

if __name__ == "__main__":
    main()

