import sys
from scrapper.scrapper import scrapping

if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print("Usage: python main.py <arg1>")
        sys.exit(1)

    script = sys.argv[1]

    if script == "scrapping":   
        scrapping()