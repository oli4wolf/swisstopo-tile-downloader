# Raster Tiles
Raster Tiles for switzerland can be obtained from swisstopo in different resolution.
https://www.swisstopo.admin.ch/de/geodata/maps/smr.html
To start we take the biggest tiles with enough resolution.
Either 50 or 100.
https://www.swisstopo.admin.ch/de/geodata/maps/smr/smr100.html
Condition is to declare the origin.
Way too big and needs to be split up.

Next try with the https://api3.geo.admin.ch/services/sdiservices.html
GetTile
<Scheme>://<ServerName>/<ProtocoleVersion>/<LayerName>/<Stylename>/<Time>/<TileMatrixSet>/<TileSetId>/<TileRow>/<TileCol>.<FormatExtension>

https://wmts3.geo.admin.ch/1.0.0/ch.swisstopo.swisstlm3d-wanderwege/ch.default/current/21781_26/22/236/284.png

https://wmts3.geo.admin.ch/1.0.0/ch.swisstopo.pixelkarte-farbe/default/current/21781/20/58/70.jpeg

# Tried but useless -> Transform the jpeg to binary.
* Download the .jpeg of the map from swisstopo with the tilesDownloader.py.
* Transform with to bin RGB565 truecolor. https://lvgl.io/tools/imageconverter