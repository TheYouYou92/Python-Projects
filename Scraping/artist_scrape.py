from seleniumbase import *
from bs4 import BeautifulSoup
import re
from selenium.webdriver.common.keys import Keys
import sys
import csv

def to_csv(res):
    with open("lyrics.csv", "a",newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["Name","URL","songName","lyrics","About","Tags","Image","Album", "Year","FAQ","Produced","Written","Label","Copyright","Phonographic","Songs","Covers"], delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(res)
   

def artist_scrape(artist):
    with SB() as sb:
        try:
            sb.open("https://genius.com/artists/" + artist.replace(" ", "-") + "/songs")
            sb.assert_title(artist + " Songs")
            if sb.is_element_visible('button:contains("I Accept")'):
                sb.click('button:contains("I Accept")')
            else:
                pass
            sb.send_keys("body", Keys.END)
            for i in range(20):
                sb.send_keys("body", Keys.END)
                sb.sleep(3)
            html = sb.get_page_source()
            soup = BeautifulSoup(html,'html.parser')
            songlinks = soup.findAll('a',href=re.compile(artist.replace(' ', '-') + r'.+lyrics', re.IGNORECASE))
            songurls = []
            for songlink in songlinks:
                if songlink['href'] not in songurls:
                    songurls.append(songlink['href'])
            for songlink in songurls:
                songdetails = {}
                sb.open(songlink)
                sb.scroll_to_bottom()
                if sb.is_element_visible("button:contains('Expand')"):
                    sb.click('button:contains("Expand")')
                else:
                    pass
                #sb.assert_element("h1")
                html = sb.get_page_source()
                soup = BeautifulSoup(html,'html.parser')
                try:
                    songdetails['Name'] = artist
                except NameError:
                    pass
                try:
                    songdetails['URL'] = songlink
                except NameError: 
                    pass
                try:
                    songdetails['songName'] = soup.find('h1').text
                except AttributeError: 
                    songdetails['songName'] = 'To Be Added'
                try:
                    
                    lyrhtml = soup.find('div', {'class':'Lyrics__Container-sc-1ynbvzw-1'}).prettify(encoding='utf-8')
                    songdetails['lyrics'] = BeautifulSoup(lyrhtml, 'html.parser').get_text()
                except: 
                    songdetails['lyrics'] = 'To Be Added'
                try:
                    
                    abouthtml = soup.find('div', {'class':'RichText__Container-oz284w-0'}).prettify(encoding='utf-8')
                    songdetails['About'] = BeautifulSoup(abouthtml, 'html.parser').get_text()
                    
                except:
                    songdetails['About'] = 'To Be Added'
                try:
                    songdetails['Tags'] = soup.find('div', {'class':'SongTags__Container-xixwg3-1'}).get_text(separator=' ,')
                except: 
                    songdetails['Tags'] = 'To Be Added'
                try:
                    songdetails['Image'] = soup.find('div', {'class':'SongHeaderdesktop__CoverArt-sc-1effuo1-7'}).img['src']
                except:
                    songdetails['Image'] = 'To Be Added'
                try:
                    songdetails['Album'] = soup.find('a', {'class':'PrimaryAlbum__Title-cuci8p-4'}).text
                except: 
                    songdetails['Album'] = 'To Be Added'
                try:
                    songdetails['Year'] = soup.find('span',{'class':'LabelWithIcon__Label-hjli77-1 hgsvkF'}).text
                except: 
                    songdetails['Year'] = 'To Be Added'
                try:
                    
                    faqhtml = soup.find('div', {'class':'QuestionList__Table-sc-1a58vti-5 geLHRn'}).prettify(encoding='utf-8')
                    songdetails['FAQ'] = BeautifulSoup(faqhtml, 'html.parser').get_text()
                except: 
                    songdetails['FAQ'] = 'To Be Added'
                try:
                    Credits = soup.findAll('div',{'class':'SongInfo__Credit-nekw6x-3'})
                    for c in Credits:
                        if 'Produced' in c.get_text():
                            songdetails['Produced'] = c.get_text().replace('Produced By', '')
                        elif 'Written' in c.get_text():
                            songdetails['Written'] = c.get_text().replace('Written By','')
                        elif 'Label' in c.get_text():
                            songdetails['Label'] = c.get_text().replace('Label','')
                        elif 'Copyright  ©' in c.get_text():
                            songdetails['Copyright'] = c.get_text().replace('Copyright ©','')
                        elif 'Phonographic' in c.get_text():
                            songdetails['Phonographic'] = c.get_text().replace('Phonographic Copyright ℗','')
                        elif 'Songs' in c.get_text():
                            songdetails['Songs'] = c.get_text(separator=' \n').replace(',','').replace('&','')
                        elif 'Covers' in c.get_text():
                            songdetails['Covers'] = c.get_text(separator=' \n').replace(',','').replace('&','')
                except:
                    pass
                
                to_csv(songdetails)
        finally:
                print('Done')
                        

    
if __name__ == "__main__":
    for i in range(1, len(sys.argv)):
        artist = sys.argv[i] 
        try:
            artist_scrape(artist)
        except Exception as e:
            print(f"An error occurred with artist {artist}: {str(e)}")



