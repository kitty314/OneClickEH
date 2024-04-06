import json
import os
import py3createtorrent

from flask import Flask, request
from flask_cors import CORS

from qb_io import QBIO
from eh_io import EHIO
from downloader import Downloader


def get_config():
    with open('configs.json') as f:
        data = json.load(f)
        eh_config = data['eh']
        qb_config = data['qb']
        server_config = data['server']
        path = data['path']
        qb_api = data['qb_api']
    return eh_config, qb_config, server_config, path, qb_api


def create_torrent_file(gid, root, archive_path):
    # Create a new torrent file
    torrent_path = os.path.join(root, gid + ".torrent")
    py3createtorrent.create_torrent(path=archive_path, trackers=[
                                    "http://ehtracker.org/{}/announce".format(gid)], output=torrent_path, force=True, comment='Created by OneClickEH: https://github.com/Tofudry233/OneClickEH')
    return torrent_path


app = Flask(__name__)
CORS(app)


@app.route('/server', methods=['POST'])
def handle_task():
    data = request.json
    if 'passwd' in data.keys() and data['passwd'] == server_config['passwd']:
        if 'url' in data.keys() and ("e-hentai" in data['url'] or "exhentai" in data['url']):

            print("Received a valid request. Processing...")

            eh_io = EHIO(**eh_config)

            gallery_url = data['url']
            gid = gallery_url[23:].split('/')[0]
            t = gallery_url[23:].split('/')[1].strip('/')

            downloader = Downloader(**path)

            # 1. Get the download link of the archive from EH
            print("Getting the download link of the archive from EH...")
            archive_url = eh_io.get_original_archive_url(gallery_url)
            print("Archive URL: ", archive_url)

            # 2. Download the archive from EH
            print("Downloading the archive from EH...")
            archive_path = downloader.download_file(archive_url)
            print("Archive downloaded to: ", archive_path)

            # 3. Create a new torrent file
            print("Creating a new torrent file...")
            torrent_path = create_torrent_file(gid, path['temp_path'], archive_path)
            print("Torrent file created at: ", torrent_path)

            # 4. Upload the torrent file to EH, and receive the download link of the new torrent file
            print("Uploading the torrent file to EH...")
            personal_torrent_url = eh_io.upload_torrent_file(
                gid, t, torrent_path)
            print("Personal torrent URL: ", personal_torrent_url)

            # 5. Download the new torrent file from EH
            print("Downloading the new torrent file from EH...")
            personal_torrent_path = downloader.download_torrent(
                personal_torrent_url)
            print("Personal torrent downloaded to: ", personal_torrent_path)

            # 6. Seed the new torrent file
            qb_io = QBIO(**qb_config)
            qb_io.upload_and_seed(personal_torrent_path,
                                  path['archive_path'], **qb_api)

            return "Task is running.", 200
        else:
            print("Invalid information. Ignoring.")
            return "Invalid information provided.", 400


if __name__ == '__main__':
    # 0. Read in the configs.json file
    eh_config, qb_config, server_config, path, qb_api = get_config()
    app.run(server_config["host"],server_config["port"], debug=False)
