import qbittorrentapi

class QBIO:
    def __init__(self, host, port, username, password):
        self.conn_info = dict(
            host=host,
            port=port,
            username=username,
            password=password,
        )
    
    def upload_and_seed(self, torrent_path, save_path, ratio_limit=None, is_paused=False):
        if ratio_limit == 0:
            ratio_limit = None
        with qbittorrentapi.Client(**self.conn_info) as qbt_client:
            qbt_client.torrents_add(torrent_files=torrent_path, save_path=save_path, is_skip_checking=False, is_paused=is_paused, ratio_limit=ratio_limit)
            print(f"Torrent file {torrent_path} has been uploaded.")
            print(f"Seeding {torrent_path}...")
            return True