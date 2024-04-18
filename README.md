# swisstopo-tile-downloader
Simple python script (map/dowloaderTiles.py) to download tiles from the Swiss Federal Office of Topography, to store them on an SD-Card for another project (flight-helper).</br>
Additionaly a second script (obstacles/downloaderObstacles.py) downloads the flight obstacles and generates the point in the dimension of the downloaded tiles.</br>
Please consider to use Linux or other OS which handles many small files better. Windows does not handle the load well.</br>
Thermik Hotspot is the CSV of bounding box switzerland from KK7.

# Elements of the downloader.
The main.py launches the 3 downloader (Map, Obstacles, Thermik).</br>
main.py takes a path (not validated) in for example: ../ or ../../ depending on where you want to launch the scripts. The rest of the path is at the root for flight-helper.</br>
Single Downloads can be launched by thermikPoint.py, obstaclesPoint.py and tileDownloader.py.</br>
