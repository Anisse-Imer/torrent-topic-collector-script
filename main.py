import time
import threading
import libtorrent as lt

import requests
from bs4 import BeautifulSoup

import concurrent.futures

class singletonTorrent:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(singletonTorrent, cls).__new__(cls)
        return cls._instance

    def download(self, save_path: str, magnet_url: str) -> threading.Thread:
        def _download_task():
            try:
                ses = lt.session()
                ses.listen_on(6881, 6891)
                params:dict = {
                    'save_path': save_path,
                    'storage_mode': lt.storage_mode_t(2),
                }
                handle = lt.add_magnet_uri(ses, magnet_url, params)
                ses.start_dht()
                
                while not handle.has_metadata():
                    time.sleep(1)
                
                while handle.status().state != lt.torrent_status.seeding:
                    s = handle.status()
                    time.sleep(5)
            except Exception as e:
                raise e
        
        thread = threading.Thread(target=_download_task)
        thread.start()
        return thread

    def search(self, query:str):
        url:str = f"https://apibay.org/q.php?q={query.replace(' ', '+')}"
        response:requests.Response = requests.get(url).json()
        magnets:list[str] = [f"magnet:?xt=urn:btih:{item['info_hash']}" for item in response]
        return magnets

def main():
    path:str = "./downloads"
    _instance:singletonTorrent = singletonTorrent()
    topic_magnets:list[str] = _instance.search(query="American Psycho")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for magnet in topic_magnets:
            executor.submit(_instance.download(save_path=path, magnet_url=magnet))

if __name__ == "__main__":
    main()
