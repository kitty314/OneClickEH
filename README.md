# OneClickEH
A simple yet convenient tools for those who want to earn some GPs by uploading torrents to E-Hentai galleries.

中文版在[这里](README_CN.md)

## Recomend using this tool if you...
- Browse E-Hentai on a PC and **have a linux server** with qbittorrent installed.
- Want to earn some GPs, but you cannot use H@H for some reason.
- Just want to help those lack of less GPs.

## What does this tool do? (Pipeline)
1. Send a signal to the server to download the gallery
2. Create a torrent file, upload it to EH
3. Seed the torrent

## Usage
1. Right click on the gallery, click on "Seed through OneClickEH".
2. Check "Torrent Download (x)". You have add an torrent to the gallery. You will earn GPs from any downloads of your uploaded torrents.

## Installation
You have to install OneClickEH Extension and OneClickEH Server.

### OneClickEH Extension (On your local PC)
1. Install [OneClickEH Extension](https://github.com/Tofudry233/OneClickEH_ext).

### OneClickEH Server (On your remote server)
1. Prerequirments: [Qbittorrent-nox](https://github.com/userdocs/qbittorrent-nox-static), Python, Conda
2. [Download OneClickEH](https://github.com/Tofudry233/OneClickEH_ext/archive/refs/heads/master.zip)
3. Install dependencies: pip install -r requirements.txt
4. Configure configs.json
5. Open the port (assume you set it to 9999): sudo ufw allow 9999
6. Run the server: python main.py 
7. Recommend running in the background by using screen (Take Ubuntu for example): 
   1. Install screen: sudo apt-get install screen
   2. Create a new session: screen -S OneClickEH
   3. cd to the directory: cd /path/to/OneClickEH
   4. python main.py
   5. Detach the screen so it will keep running even turn off terminal: Ctrl+A+D
   6. Resume the screen: screen -r OneClickEH

## Configs.json
- "eh": The cookies of e-hentai and ex-hentai. Get these from your browser, and input them here.
- "qb": The settings of your qbittorrent's WebUI.
  - "host": Your VPS's ip address
  - "port": Your qbittorrent WebUI's port.
  - "username" and "password": Your login information to qbittorrent WebUI
- "server": The settings of this OneClickEH's connections
  - "host": Keep it "0.0.0.0".
  - "port": The port where server will listening to. This should be set to be the same as in OneClickEH Extension
  - "passwd": The password for verifying inbound connections. This should be set to be the same as in OneClickEH Extension
- "path": The path ofr saving files.
  - "archive": Where downloaded archive would be stored.
  - "temp": Where some temporary files would be stored, including created torrent files.
  - "torrent": Where the downloaded torrent files would be stored.
- "qb_api": Some advanced settings for qbittorrent.
  - "ratio_limit": The torrent will stop uploading when reach this ratio. This is for saving your bandwidth. Set to 0 if you do not want to limit uploading ratio.
  - "is_paused": Set to 1 if you want to start the torrents manually. Otherwise keep it to be 0, so that the seeding will start automatically.