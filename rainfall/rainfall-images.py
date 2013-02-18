"""
Converts 0.5 deg daily rainfall data into daily images.

Usage:
    python rainfall-video.py
"""

import os
import csv
import datetime
import color as _color      # Gramener visualisation server
import Image                # Python Image Library
import itertools

if not os.path.isdir('out'):
    os.makedirs('out')

reader = csv.DictReader(open('daily-rainfall-data.csv'), delimiter='\t')
fields = reader.fieldnames[3:]
W = len(fields)
HI = 5.7    # 99% = 49.1, 95% = 14.3, 90% = 5.7, 80% = 0.6

for key, rows in itertools.groupby(reader, lambda v: (v['Year'], v['Day'])):
    rows = list(rows)
    im = Image.new('RGBA', (W, len(rows)))
    for y, row in enumerate(rows):
        for x, field in enumerate(fields):
            try:
                cell = float(row[field])
            except:
                cell = -999
            if cell < 0:
                color = (0, 0, 0, 0)
            else:
                color = tuple(int(255*v) for v in _color.rgba(
                    _color.gradient(cell / HI, _color.Greens)))
            im.putpixel((x, y), color)

    date = datetime.datetime(int(key[0]), 1, 1) + datetime.timedelta(days=int(key[1]) - 1)
    filename = date.strftime('out/%Y-%m-%d.png')
    im.save(filename)
    print filename
