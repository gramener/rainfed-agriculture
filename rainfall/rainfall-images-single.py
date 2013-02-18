"""
Converts 0.5 deg daily rainfall data into daily images.

Usage:
    python rainfall-video.py
"""

import csv
import color as _color      # Gramener visualisation server
import Image                # Python Image Library
import itertools

reader = csv.DictReader(open('daily-rainfall-data.csv'), delimiter='\t')
fields = reader.fieldnames[3:]
W = len(fields)

HI = 5.7    # 99% = 49.1, 95% = 14.3, 90% = 5.7, 80% = 0.6
STARTYEAR = 1971
ENDYEAR = 2005
YEARS = ENDYEAR - STARTYEAR + 1     # Number of years
ROWS = 65                           # Number of latitude grids each day

im = Image.new('RGBA', (W * 366, YEARS * ROWS))
for key, rows in itertools.groupby(reader, lambda v: (v['Year'], v['Day'])):
    print key
    rows = list(rows)
    X0 = W * (int(key[1]) - 1)
    Y0 = ROWS * (int(key[0]) - STARTYEAR)
    for y, row in enumerate(rows):
        for x, field in enumerate(fields):
            try:
                cell = float(row[field])
            except:
                cell = -999
            if cell < 0:
                color = (0, 0, 0, 0)
            else:
                color = tuple(int(255 * v) for v in _color.rgba(
                    _color.gradient(cell / HI, _color.Greens)))
            im.putpixel((x + X0, y + Y0), color)

im.save('rainfall.png')
