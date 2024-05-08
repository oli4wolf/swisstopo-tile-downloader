from multiprocessing import Process
import asyncio
import sys
import thermikDownloader
import obstacleDownloader
import bikeDownloader
import tileDownloader
import hikeDownloader
import satDownloader

import tracemalloc

tracemalloc.start()

async def fileDownload(path, download):
    await asyncio.gather(
        tileDownloader.main(path, download),
        hikeDownloader.main(path, download), 
        bikeDownloader.main(path, download),
        satDownloader.main(path, download)
    )

def main(path, download):
    print("Starting download of thermik hotspots.")
    thermikProc = Process(target=thermikDownloader.main, args=(path, download))
    thermikProc.start()
    print("Starting download of obstacles.")
    obstaclesProc = Process(target=obstacleDownloader.main, args=(path, download))
    obstaclesProc.start()

    asyncio.run(fileDownload(path, download))

    thermikProc.join()
    obstaclesProc.join()
    print("Download finished.")

# Example python main.py d:/ True
if __name__ == "__main__":
    if len(sys.argv) > 2:
        main(sys.argv[1], sys.argv[2])
    else:
        # Default path if none is given.
        main("./", True)
