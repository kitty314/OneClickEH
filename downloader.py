import requests
from multiprocessing import Pool, cpu_count
import os
from tqdm import tqdm
from urllib.parse import unquote
import re

class Downloader():
    def __init__(self, archive_path, temp_path, torrent_path) -> None:
        self.archive_path = archive_path
        self.temp_path = temp_path
        self.torrent_path = torrent_path

    def _download_chunk(self, args):
        url, filename, start, end, part_num, total_size = args
        headers = {'Range': f'bytes={start}-{end}'}
        r = requests.get(url, headers=headers, stream=True)
        # Calculate chunk size for progress update
        chunk_size = max(int((end - start) / 100), 8192)  # Adjust the chunk size dynamically
        # Open temporary file for writing the downloaded chunk
        with open(os.path.join(self.temp_path, f'{filename}_part{part_num}'), 'wb') as f, tqdm(
            total=total_size, position=part_num, desc=f'{filename}_part{part_num}', unit='B', unit_scale=True, unit_divisor=1024
        ) as progress:
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)
                progress.update(len(chunk))

    def _merge_files(self, total_parts, prefix, output_filename):
        print("\nMerging parts into the final file...")
        with open(output_filename, 'wb') as outfile, tqdm(total=total_parts, desc="Merging", unit='part') as progress:
            for i in range(total_parts):
                part_file_name = os.path.join(self.temp_path, f'{prefix}_part{i}')
                # Verify part file exists before attempting to open
                if not os.path.exists(part_file_name):
                    raise FileNotFoundError(f"Missing part: {part_file_name}. Download might be incomplete.")
                with open(part_file_name, 'rb') as infile:
                    outfile.write(infile.read())
                os.remove(part_file_name)
                progress.update(1)

    def download_file(self, url):
        proc_num = min(cpu_count(), 5)
        r = requests.head(url)

        filename = r.headers['Content-Disposition'].split("=")[-1].strip('"')
        bytes_string = re.sub(
            r'\\x([0-9a-fA-F]{2})',
            lambda match: bytes.fromhex(match.group(1)).decode('latin1'),
            filename
        )
        filename = bytes_string.encode('latin1').decode('utf-8')

        if not os.path.exists(self.archive_path):
            os.makedirs(self.archive_path)

        output_filepath = os.path.join(self.archive_path, filename)

        total_size = int(r.headers.get('content-length', 0))
        part_size = total_size // proc_num
        
        parts = [(url, filename, i * part_size, (i + 1) * part_size - 1, i, part_size) for i in range(proc_num)]
        # Adjust the last part to cover the remainder
        if total_size % proc_num > 0:
            last_size = total_size - parts[-1][2]
            parts[-1] = (url, filename, parts[-1][2], total_size - 1, proc_num - 1, last_size)
        
        with Pool(proc_num) as p:
            p.map(self._download_chunk, parts)
        
        self._merge_files(proc_num, filename, output_filepath)

        return output_filepath

    def download_torrent(self, url):
        r = requests.get(url)
        if r.status_code == 200:
            filename = r.headers['Content-Disposition'].split("=")[-1].strip('"')
            output_filename = os.path.join(self.torrent_path, filename)
            with open(output_filename, 'wb') as f:
                f.write(r.content)
            return output_filename
        else:
            print(f"Failed to download the file. Status code: {r.status_code}")
            return None