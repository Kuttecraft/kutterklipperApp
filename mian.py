import sys
from app import KutterKlipperInterface

if __name__ == "__main__":
    printer_1_data = sys.argv[1] if len(sys.argv) > 1 else None
    app = KutterKlipperInterface(printer_1_data=printer_1_data)
    app.run()