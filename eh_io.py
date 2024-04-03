import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse, parse_qs
import json

def get_config():
    with open('configs.json') as f:
        data = json.load(f)
        cookies = data['cookies']
        headers = data['headers']
        root = data['root']
    return cookies, headers, root

class EHIO():
    def __init__(self, cookies, headers):
        self.cookies = cookies
        self.headers = headers

    def get_archive(self, url) -> tuple[bytes, str]:
        try:
            # Send a GET request to the URL
            response = requests.get(url, headers=self.headers, cookies=self.cookies)
            
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                respo_header = response.headers['Content-Disposition']
                filename = respo_header.split("=")[-1].strip('"')
                return response.content, filename
            else:
                print(f"Failed to download the file. Status code: {response.status_code}")
        except Exception as e:
            print(f"An error occurred: {e}")
            return None, None

    def find_torrent_link(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Define the base part of the URL you are looking for
        base_url = "https://ehtracker.org/get"
        
        # Find all 'a' tags with 'href' containing the base URL
        links = soup.find_all('a', href=re.compile(r'^' + re.escape(base_url)))
        
        # If at least one link is found, return the href attribute of the first link
        if links:
            return links[0].get('href')
        else:
            return "No matching link found."

    def find_archive_download_url(self, html):

        link_text = "Archive Download"
        # Parse the HTML content
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find all <a> tags in the HTML
        links = soup.find_all('a')
        
        # Iterate over all found <a> tags
        for link in links:
            # Check if the link text or the title attribute contains the specified link text
            if link.text == link_text or link.get('title', '') == link_text:
                # Return the URL found
                regex = r"popUp\('([^']+)'"
                match = re.search(regex, link['onclick'])
                url = match.group(1).replace('amp;', '') # https://e-hentai.org/archiver.php?gid=xxx&token=xx&or=xx
                return url
        
        # If the loop completes without finding a match, return None
        return None
    
    def get_original_archive_url(self, url):

        url = self._get_archive_url(url)
        payload = {
            'dltype': 'org',
            'dlcheck': 'Download Original Archive'
        }
        response = requests.post(url, data=payload, headers=self.headers, cookies=self.cookies)
        url_pattern = r"https?://[^\s\"'>]+\.hath\.network[^\s\"'>]*"
        return re.findall(url_pattern, response.text)[0]+'?start=1'
    
    def _get_archive_url(self, url):
        # Send a GET request to the specified URL
        response = requests.get(url, headers=self.headers, cookies=self.cookies)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Extract the download URL from the HTML content
            archive_url = self.find_archive_download_url(response.text)
            return archive_url
        else:
            print(f"Failed to get the archive URL. Status code: {response.status_code}")
            return None
    
    def upload_torrent_file(self, gid, t, torrent_path):
        url = 'https://repo.e-hentai.org/torrent_post.php?gid={}&t={}'.format(gid, t)
        files = {
            'torrentfile': (open(torrent_path, 'rb'))
        }
        
        # Make the POST request to the server with the file, headers, and cookies
        response = requests.post(url, files=files, headers=self.headers, cookies=self.cookies)

        # response.url: 'https://e-hentai.org/gallerytorrents.php?gid=2876854&t=3bc1ac8012&act=uploaded&gtid=1474125'
        # response.text: save3.html
        
        try:
            finished_url = response.url
            return self._get_personal_torrent_url(response.text)
        except:
            print("Error: ", response.status_code, response.text)
    
    def _get_personal_torrent_url(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        links = soup.find_all('a')
        
        for link in links:
            if 'Click' in link.text:
                return link['href']
        return None