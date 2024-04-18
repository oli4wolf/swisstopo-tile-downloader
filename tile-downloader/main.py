import sys
import thermikPoint
import obstaclesPoint

def main(path, download):
    thermikPoint.main(path, download)
    obstaclesPoint.main(path, download)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        main(sys.argv[1], sys.argv[2])
    else:
        # Default path if none is given.
        main("./", True)
