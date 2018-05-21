import requests, urllib2, re
from bs4 import BeautifulSoup as bs
def ripVids(url):
    """Finds the url of the video of the supplied link of the episode, url = episode url, returns a dict with keys as resolution and values as links"""

    print "Ripping " + url
    try:
        r = requests.get(url)
    except requests.ConnectionError:
        print("Please check internet connection.")
        
    soup = bs(r.text, 'lxml')
    vids = soup.find('video')
    vids = vids.findAll('source')
    dic = {}
    for i in vids:
        dic[i['data-res']] = i['src']
    return dic

def obtainURLs(url):
    """Finds all episodes of certain series of supplied episode link, return a dict with number of eps and link of eps"""
    try:
        r = requests.get(url)
    except requests.ConnectionError:
        print("Please check internet connection.")
    soup = bs(r.text, 'lxml')
    title = soup.find('title')
    titleText = title.get_text()
    linkstag = soup.find('div', {'id':'myTabContent'})
    linksList = linkstag.findAll('a')
    ld = {}
    for i in linksList:
        ld[i.get_text()] = i['href']
        print i.get_text(), "Just got added"
    return ld, titleText.strip()
   
def DownloadFile(url, name):
    """Download specific video requires video url, and name of file"""

    print "Downloading " + name
    try:
        r = requests.get(url)
    except requests.ConnectionError:
        print "Please check internet connection."
    f = open(name.replace('|',''), 'wb')
    for chunk in r.iter_content(chunk_size=512 * 1024): 
        if chunk: # filter out keep-alive new chunks
            f.write(chunk)
    f.close()
    return

def WriteToCrawlJob(pkgname, nesteddicts):
    """Function to create a jDownloader CrawlJob file, filename being the season followed by episode number."""

    f = open(pkgname+'.crawljob','wb')
    for i in nesteddicts:
        for n in nesteddicts[i]:
            f.write('->NEW ENTRY<-\n    text={link}\n    filename=[{defi}]{pkgn} {epsname}.mp4\n    packageName={pkgn}\n'.format(link = nesteddicts[i][n], defi = n, epsname = i.replace('|',""), pkgn = pkgname))
    f.close()
def main():
    """Compile everything together, insert only URL"""

    url = raw_input("Input URL:\n")
    df = {}
    d1, text = obtainURLs(url)
    for i in d1:
        df[i] = ripVids(d1[i])
    WriteToCrawlJob(re.sub(r'[^\w]', ' ', text), df)

if __name__ == "__main__":
    main()
