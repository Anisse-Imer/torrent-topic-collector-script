import time
import threading
import libtorrent as lt

class singletonTorrent:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(singletonTorrent, cls).__new__(cls)
        return cls._instance

    import threading

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
                
                print("Download completed!")
            except Exception as e:
                print(f"Download failed: {e}")
        
        thread = threading.Thread(target=_download_task)
        thread.start()
        return thread

def main():
    _instance:singletonTorrent = singletonTorrent()
    path:str = "./downloads"
    m_url_1:str = "magnet:?xt=urn:btih:8148C169C4B84048FCF8D44AAF275F82BC33829E&dn=Spider-Man+No+Way+Home+%282021%29+%5B1080p%5D+%5BBluRay%5D&tr=http%3A%2F%2Fp4p.arenabg.com%3A1337%2Fannounce&tr=udp%3A%2F%2F47.ip-51-68-199.eu%3A6969%2Fannounce&tr=udp%3A%2F%2F9.rarbg.me%3A2780%2Fannounce&tr=udp%3A%2F%2F9.rarbg.to%3A2710%2Fannounce&tr=udp%3A%2F%2F9.rarbg.to%3A2730%2Fannounce&tr=udp%3A%2F%2F9.rarbg.to%3A2920%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&tr=udp%3A%2F%2Fopentracker.i2p.rocks%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.cyberia.is%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.dler.org%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.internetwarriors.net%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337&tr=udp%3A%2F%2Ftracker.pirateparty.gr%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.tiny-vps.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce"
    m_url_2:str = ""
    
    _instance.download(save_path=path, magnet_url=m_url)

    download_thread = download("/path/to/save", "magnet:?xt=urn:...")
    download_thread.join()

if __name__ == "__main__":
    main()
