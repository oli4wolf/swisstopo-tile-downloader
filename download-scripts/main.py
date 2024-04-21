from multiprocessing import Process
import sys
import thermikPoint
import obstaclesPoint
import tileDownloader
import hikeDownloader

def main(path, download):
    print("Starting download of thermik hotspots.")
    thermikProc = Process(target=thermikPoint.main, args=(path, download))
    thermikProc.start()
    print("Starting download of obstacles.")
    obstaclesProc = Process(target=obstaclesPoint.main, args=(path, download))
    obstaclesProc.start()
    print("Starting download of tiles.")
    tileProc = Process(target=tileDownloader.main, args=(path, download))
    tileProc.start()
    print("Starting download of hikes.")
    hikeProc = Process(target=hikeDownloader.main, args=(path, download))
    hikeProc.start()
    thermikProc.join()
    obstaclesProc.join()
    tileProc.join()
    hikeProc.join()
    print("Download finished.")

# Example python main.py d:/ True
if __name__ == "__main__":
    if len(sys.argv) > 2:
        main(sys.argv[1], sys.argv[2])
    else:
        # Default path if none is given.
        main("./", True)
