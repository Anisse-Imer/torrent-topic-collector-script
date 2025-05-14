import time

import threading
import libtorrent as lt
import concurrent.futures

import requests
import certifi
from fp.fp import FreeProxy

class singletonTorrent:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(singletonTorrent, cls).__new__(cls)
        return cls._instance

    def get_random_proxy(self):
        proxy = FreeProxy(rand=True, timeout=1).get()
        return proxy

    def download(self, save_path: str, magnet_url: str) -> threading.Thread:
        def _download_task():
            try:
                ses = lt.session()
                ses.listen_on(6881, 6891)
                params = {
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
                print(f"Download error: {e}")

        thread = threading.Thread(target=_download_task)
        thread.start()
        return thread

    def search(self, query: str, retries=3):
        for attempt in range(retries):
            proxy = self.get_random_proxy()
            proxies = {
                'http': proxy,
                'https': proxy,
            }
            url = f"https://apibay.org/q.php?q={query.replace(' ', '+')}"
            try:
                response = requests.get(url, proxies=proxies, timeout=30)
                response.raise_for_status()
                data = response.json()
                magnets = [f"magnet:?xt=urn:btih:{item['info_hash']}" for item in data]
                return magnets
            except requests.exceptions.RequestException as e:
                print(f"Attempt {attempt + 1}: Search error with proxy {proxy}: {e}")
                time.sleep(2)  # Wait before retrying
        return []


def main():
    path = "./downloads"
    _instance = singletonTorrent()
    topic_magnets = _instance.search(query="American Psycho", retries=15)
    print(topic_magnets)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for magnet in topic_magnets:
            executor.submit(_instance.download, save_path=path, magnet_url=magnet)

if __name__ == "__main__":
    main()
