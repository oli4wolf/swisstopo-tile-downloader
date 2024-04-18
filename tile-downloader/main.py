import sys
import thermikPoint
import obstaclesPoint
import tileDownloader

def main(path, download):
    print("Starting download of thermik hotspots.")
    thermikPoint.main(path, download)
    print("Starting download of obstacles.")
    obstaclesPoint.main(path, download)
    print("Starting download of tiles.")
    tileDownloader.main(path, download)
    print("Download finished.")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        main(sys.argv[1], sys.argv[2])
    else:
        # Default path if none is given.
        main("./", True)
