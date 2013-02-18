"""
Color and gradient management routines.
"""

import re
import operator
import numpy
import colorsys
import warnings

"""
This module uses some pre-defined gradients.

- `RYG` = Red-Yellow-Green. Red = 0, Green = 1.
- `RWG` = Red-White-Green. Red = 0. Green = 1.

By default, the scale is (0, 0.5, 1). For a (-1, 0, +1) scale,
use `RYG_1`, `RWG_1`, etc.

A number of other gradients from [ColorBrewer](http://colorbrewer2.org/)
are also available for use. These are preferred.
"""

RYG   = (( 0.0, '#ff0000'), (0.5, '#ffff00'), (1.0, '#00ff00'))
RYG_1 = ((-1.0, '#ff0000'), (0.0, '#ffff00'), (1.0, '#00ff00'))

# Alternate palette colours
#     RYG   = (( 0.0, '#FF4142'), (0.5, '#FFD026'), (1.0, '#AAE817'))
#     RYG_1 = ((-1.0, '#FF4142'), (0.0, '#FFD026'), (1.0, '#AAE817'))

RWG   = (( 0.0, '#ff0000'), (0.5, '#ffffff'), (1.0, '#00ff00'))
RWG_1 = ((-1.0, '#ff0000'), (0.0, '#ffffff'), (1.0, '#00ff00'))

# Color schemes from <http://colorbrewer2.org/>
# under [Apache license](http://www.personal.psu.edu/cab38/ColorBrewer/ColorBrewer_updates.html)

# Sequential 9-point multihue color schemes
BuGn    = (( 0.0, '#F7FCFD'), (0.5, '#66C2A4'), (1.0, '#00441B'))
BuPu    = (( 0.0, '#F7FCFD'), (0.5, '#8C96C6'), (1.0, '#4D004B'))
GnBu    = (( 0.0, '#F7FCF0'), (0.5, '#7BCCC4'), (1.0, '#084081'))
OrRd    = (( 0.0, '#FFF7EC'), (0.5, '#FC8D59'), (1.0, '#7F0000'))
PuBu    = (( 0.0, '#FFF7FB'), (0.5, '#74A9CF'), (1.0, '#023858'))
PuBuGn  = (( 0.0, '#FFF7FB'), (0.5, '#67A9CF'), (1.0, '#014636'))
PuRd    = (( 0.0, '#F7F4F9'), (0.5, '#DF65B0'), (1.0, '#67001F'))
RdPu    = (( 0.0, '#FFF7F3'), (0.5, '#F768A1'), (1.0, '#49006A'))
YlGn    = (( 0.0, '#FFFFE5'), (0.5, '#78C679'), (1.0, '#004529'))
YlGnBu  = (( 0.0, '#FFFFD9'), (0.5, '#41B6C4'), (1.0, '#081D58'))
YlOrBr  = (( 0.0, '#FFFFE5'), (0.5, '#FE9929'), (1.0, '#662506'))
YlOrRd  = (( 0.0, '#FFFFCC'), (0.5, '#FD8D3C'), (1.0, '#800026'))

# Sequential 9-point single hue color schemes
Blues   = (( 0.0, '#F7FBFF'), (0.5, '#6BAED6'), (1.0, '#08306B'))
Greens  = (( 0.0, '#F7FCF5'), (0.5, '#74C476'), (1.0, '#00441B'))
Greys   = (( 0.0, '#FFFFFF'), (0.5, '#969696'), (1.0, '#000000'))
Oranges = (( 0.0, '#FFF5EB'), (0.5, '#FD8D3C'), (1.0, '#7F2704'))
Purples = (( 0.0, '#FCFBFD'), (0.5, '#9E9AC8'), (1.0, '#3F007D'))
Reds    = (( 0.0, '#FFF5F0'), (0.5, '#FB6A4A'), (1.0, '#67000D'))

# Sequential 9-point single hue color schemes: added by Gramener
# This is the MS Office Tan color (_light2) scheme
Browns  = (( 0.0, '#EEECE1'), (0.5, '#948A54'), (1.0, '#4A452A'))
Yellows = (( 0.0, '#FFFFE1'), (0.5, '#FFFF00'), (1.0, '#C0AE00'))

# Diverging 9-point multihue color schemes

# Photocopyable, print friendly, colorblind safe
PuOr    = ((-1.0, '#B35806'), (0.0, '#F7F7F7'), (1.0, '#542788'))
# Print friendly, colorblind safe
BrBG    = ((-1.0, '#8C510A'), (0.0, '#F5F5F5'), (1.0, '#01665E'))
PiYG    = ((-1.0, '#C51B7D'), (0.0, '#F7F7F7'), (1.0, '#4D9221'))
PRGn    = ((-1.0, '#762A83'), (0.0, '#F7F7F7'), (1.0, '#1B7837'))
RdBu    = ((-1.0, '#B2182B'), (0.0, '#F7F7F7'), (1.0, '#2166AC'))
RdYlBu  = ((-1.0, '#D73027'), (0.0, '#FFFFBF'), (1.0, '#4575B4'))
# Others
RdGy    = ((-1.0, '#B2182B'), (0.0, '#FFFFFF'), (1.0, '#4D4D4D'))
RdYlGn  = ((-1.0, '#D73027'), (0.0, '#FFFFBF'), (1.0, '#1A9850'))
Spectral= ((-1.0, '#FC8D59'), (0.0, '#FFFFBF'), (1.0, '#91CF60'))

_colornames = {
    'black'     : [ 0   , 0   , 0   ],
    'silver'    : [ 192 , 192 , 192 ],
    'gray'      : [ 128 , 128 , 128 ],
    'white'     : [ 255 , 255 , 255 ],
    'maroon'    : [ 128 , 0   , 0   ],
    'red'       : [ 255 , 0   , 0   ],
    'purple'    : [ 128 , 0   , 128 ],
    'fuchsia'   : [ 255 , 0   , 255 ],
    'green'     : [ 0   , 128 , 0   ],
    'lime'      : [ 0   , 255 , 0   ],
    'olive'     : [ 128 , 128 , 0   ],
    'yellow'    : [ 255 , 255 , 0   ],
    'navy'      : [ 0   , 0   , 128 ],
    'blue'      : [ 0   , 0   , 255 ],
    'teal'      : [ 0   , 128 , 128 ],
    'aqua'      : [ 0   , 255 , 255 ],
}

# Microsoft Office Themes
class _MSO(object):
    """
    Refer to colours in any of these ways:

        color['accent_1']
        color[0]
        color.accent_1
        color[:1]
    """
    _lookup = {
        'accent_1'  : 0,
        'accent_2'  : 1,
        'accent_3'  : 2,
        'accent_4'  : 3,
        'accent_5'  : 4,
        'accent_6'  : 5,
        'light_2'   : 6,
        'dark_2'    : 7,
        'light_1'   : 8,
        'dark_1'    : 9,
    }

    def __init__(self, *values):
        self.values = values

    def __getitem__(self, key):
        if isinstance(key, slice) or type(key) is int:
            return self.values.__getitem__(key)
        elif key in self._lookup:
            return self.values[self._lookup[key]]

    def __getattr__(self, key):
        if key in self._lookup:
            return self.values[self._lookup[key]]

    def __len__(self):
        return len(self.values)

    def __str__(self):
        return ' '.join(self.values)

    def __repr__(self):
        return '_MSO' + repr(self.values)

Office      = _MSO('#4f81bd', '#c0504d', '#9bbb59', '#8064a2', '#4bacc6', '#f79646', '#eeece1', '#1f497d', '#ffffff', '#000000')
Adjacency   = _MSO('#A9A57C', '#9CBEBD', '#D2CB6C', '#95A39D', '#C89F5D', '#B1A089', '#DFDCB7', '#675E47', '#FFFFFF', '#2F2B20', '#D25814', '#849A0A')
Apex        = _MSO('#ceb966', '#9cb084', '#6bb1c9', '#6585cf', '#7e6bc9', '#a379bb', '#c9c2d1', '#69676d', '#ffffff', '#000000')
Apothecary  = _MSO('#93A299', '#CF543F', '#B5AE53', '#848058', '#E8B54D', '#786C71', '#ECEDD1', '#564B3C', '#FFFFFF', '#000000', '#CCCC00', '#B2B2B2')
Aspect      = _MSO('#f07f09', '#9f2936', '#1b587c', '#4e8542', '#604878', '#c19859', '#e3ded1', '#323232', '#ffffff', '#000000')
Austin      = _MSO('#94C600', '#71685A', '#FF6700', '#909465', '#956B43', '#FEA022', '#CAF278', '#3E3D2D', '#FFFFFF', '#000000', '#E68200', '#FFA94A')
BlackTie    = _MSO('#6F6F74', '#A7B789', '#BEAE98', '#92A9B9', '#9C8265', '#8D6974', '#E3DCCF', '#46464A', '#FFFFFF', '#000000', '#67AABF', '#B1B5AB')
Civic       = _MSO('#d16349', '#ccb400', '#8cadae', '#8c7b70', '#8fb08c', '#d19049', '#c5d1d7', '#646b86', '#ffffff', '#000000')
Clarity     = _MSO('#93A299', '#AD8F67', '#726056', '#4C5A6A', '#808DA0', '#79463D', '#F3F2DC', '#D2533C', '#FFFFFF', '#292934', '#0000FF', '#800080')
Composite   = _MSO('#98C723', '#59B0B9', '#DEAE00', '#B77BB4', '#E0773C', '#A98D63', '#E7ECED', '#5B6973', '#FFFFFF', '#000000', '#26CBEC', '#598C8C')
Concourse   = _MSO('#2da2bf', '#da1f28', '#eb641b', '#39639d', '#474b78', '#7d3c4a', '#def5fa', '#464646', '#ffffff', '#000000')
Couture     = _MSO('#9E8E5C', '#A09781', '#85776D', '#AEAFA9', '#8D878B', '#6B6149', '#D0CCB9', '#37302A', '#FFFFFF', '#000000', '#B6A272', '#8A784F')
Elemental   = _MSO('#629DD1', '#297FD5', '#7F8FA9', '#4A66AC', '#5AA2AE', '#9D90A0', '#ACCBF9', '#242852', '#FFFFFF', '#000000', '#9454C3', '#3EBBF0')
Equity      = _MSO('#d34817', '#9b2d1f', '#a28e6a', '#956251', '#918485', '#855d5d', '#e9e5dc', '#696464', '#ffffff', '#000000')
Essential   = _MSO('#7A7A7A', '#F5C201', '#526DB0', '#989AAC', '#DC5924', '#B4B392', '#C8C8B1', '#D1282E', '#FFFFFF', '#000000', '#CC9900', '#969696')
Executive   = _MSO('#6076B4', '#9C5252', '#E68422', '#846648', '#63891F', '#758085', '#E4E9EF', '#2F5897', '#FFFFFF', '#000000', '#3399FF', '#B2B2B2')
Flow        = _MSO('#0f6fc6', '#009dd9', '#0bd0d9', '#10cf9b', '#7cca62', '#a5c249', '#dbf5f9', '#04617b', '#ffffff', '#000000')
Foundry     = _MSO('#72a376', '#b0ccb0', '#a8cdd7', '#c0beaf', '#cec597', '#e8b7b7', '#eaebde', '#676a55', '#ffffff', '#000000')
Grid        = _MSO('#C66951', '#BF974D', '#928B70', '#87706B', '#94734E', '#6F777D', '#CCD1B9', '#534949', '#FFFFFF', '#000000', '#CC9900', '#C0C0C0')
Hardcover   = _MSO('#873624', '#D6862D', '#D0BE40', '#877F6C', '#972109', '#AEB795', '#ECE9C6', '#895D1D', '#FFFFFF', '#000000', '#CC9900', '#B2B2B2')
Horizon     = _MSO('#7E97AD', '#CC8E60', '#7A6A60', '#B4936D', '#67787B', '#9D936F', '#DC9E1F', '#1F2123', '#FFFFFF', '#000000', '#646464', '#969696')
Median      = _MSO('#94b6d2', '#dd8047', '#a5ab81', '#d8b25c', '#7ba79d', '#968c8c', '#ebddc3', '#775f55', '#ffffff', '#000000')
Metro       = _MSO('#7fd13b', '#ea157a', '#feb80a', '#00addc', '#738ac8', '#1ab39f', '#d6ecff', '#4e5b6f', '#ffffff', '#000000')
Module      = _MSO('#f0ad00', '#60b5cc', '#e66c7d', '#6bb76d', '#e88651', '#c64847', '#d4d4d6', '#5a6378', '#ffffff', '#000000')
Newsprint   = _MSO('#AD0101', '#726056', '#AC956E', '#808DA9', '#424E5B', '#730E00', '#DEDEE0', '#303030', '#FFFFFF', '#000000', '#D26900', '#D89243')
Opulent     = _MSO('#b83d68', '#ac66bb', '#de6c36', '#f9b639', '#cf6da4', '#fa8d3d', '#f4e7ed', '#b13f9a', '#ffffff', '#000000')
Oriel       = _MSO('#fe8637', '#7598d9', '#b32c16', '#f5cd2d', '#aebad5', '#777c84', '#fff39d', '#575f6d', '#ffffff', '#000000')
Origin      = _MSO('#727ca3', '#9fb8cd', '#d2da7a', '#fada7a', '#b88472', '#8e736a', '#dde9ec', '#464653', '#ffffff', '#000000')
Paper       = _MSO('#a5b592', '#f3a447', '#e7bc29', '#d092a7', '#9c85c0', '#809ec2', '#fefac9', '#444d26', '#ffffff', '#000000')
Perspective = _MSO('#838D9B', '#D2610C', '#80716A', '#94147C', '#5D5AD2', '#6F6C7D', '#FF8600', '#283138', '#FFFFFF', '#000000', '#6187E3', '#7B8EB8')
Pushpin     = _MSO('#FDA023', '#AA2B1E', '#71685C', '#64A73B', '#EB5605', '#B9CA1A', '#CCDDEA', '#465E9C', '#FFFFFF', '#000000', '#D83E2C', '#ED7D27')
SlipStream  = _MSO('#4E67C8', '#5ECCF3', '#A7EA52', '#5DCEAF', '#FF8021', '#F14124', '#B4DCFA', '#212745', '#FFFFFF', '#000000', '#56C7AA', '#59A8D1')
Solstice    = _MSO('#4f271c', '#feb80a', '#e7bc29', '#84aa33', '#964305', '#475a8d', '#e7dec9', '#4f271c', '#ffffff', '#000000')
Technic     = _MSO('#6ea0b0', '#6ea0b0', '#8d89a4', '#748560', '#9e9273', '#7e848d', '#d4d2d0', '#3b3b3b', '#ffffff', '#000000')
Thatch      = _MSO('#759AA5', '#CFC60D', '#99987F', '#90AC97', '#FFAD1C', '#B9AB6F', '#DFE6D0', '#1D3641', '#FFFFFF', '#000000', '#66AACD', '#809DB3')
Trek        = _MSO('#f0a22e', '#a5644e', '#b58b80', '#c3986d', '#a19574', '#c17529', '#fbeec9', '#4e3b30', '#ffffff', '#000000')
Urban       = _MSO('#53548a', '#438086', '#a04da3', '#c4652d', '#8b5d3d', '#5c92b5', '#dedede', '#424456', '#ffffff', '#000000')
Verve       = _MSO('#ff388c', '#e40059', '#9c007f', '#68007f', '#005bd3', '#00349e', '#d2d2d2', '#666666', '#ffffff', '#000000')
Waveform    = _MSO('#31B6FD', '#4584D3', '#5BD078', '#A5D028', '#F5C040', '#05E0DB', '#C6E7FC', '#073E87', '#FFFFFF', '#000000', '#0080FF', '#5EAEFF')


def _rgb(color):
    """
    Internal color conversion
    Converts `#ffffff` to `(255, 255, 255)`
    """
    warnings.warn('Use color.rgba instead of color._rgb', FutureWarning, stacklevel=2)
    return (int(color[-6:-4], 16), int(color[-4:-2], 16), int(color[-2:], 16))


def rgba(color):
    """Follows <http://dev.w3.org/csswg/css3-color/> and returns a [0-1] float for rgba"""
    result = []
    if color.startswith('#'):
        if len(color) == 7:
            result = [int(color[1:3], 16)/255., int(color[3:5], 16)/255., int(color[5:7], 16)/255.]
        elif len(color) == 4:
            result = [int(color[1:2], 16)/15., int(color[2:3], 16)/15., int(color[3:4], 16)/15.]
        else:
            result = []

    elif color.startswith('rgb(') or color.startswith('rgba('):
        for i, v in enumerate(re.findall(r'[0-9\.%]+', color.split('(')[1])):
            if v.endswith('%'):
                result.append(float(v[:-1]) / 100)
            elif i < 3:
                result.append(float(v) / 255.)
            else:
                result.append(float(v))

    elif color.startswith('hsl(') or color.startswith('hsla('):
        for i, v in enumerate(re.findall(r'[0-9\.%]+', color.split('(')[1])):
            if v.endswith('%'):
                result.append(float(v[:-1]) / 100)
            elif i == 0:
                result.append(float(v) / 360 % 1)
            else:
                result.append(float(v))
        result[0], result[1], result[2] = colorsys.hsv_to_rgb(result[0], result[1], result[2])

    elif color in _colornames:
        result = _colornames[color]

    if len(result) == 3:
        result.append(1.)

    if len(result) != 4:
        raise ValueError('%s: invalid color' % color)

    return tuple(0 if v < 0 else 1 if v > 1 else v for v in result)


def hsla(color):
    """Follows <http://dev.w3.org/csswg/css3-color/> and returns a [0-1] float for hsla"""
    result = rgba(color)
    return colorsys.rgb_to_hsv(result[0], result[1], result[2]) + (result[3], )


def name(r, g, b, a=1):
    """Returns a short color string"""
    r = 0 if r < 0 else 1 if r > 1 else r
    g = 0 if g < 0 else 1 if g > 1 else g
    b = 0 if b < 0 else 1 if b > 1 else b
    a = 0 if a < 0 else 1 if a > 1 else a
    if a >= 1:
        s = '#%02x%02x%02x' % (255*r, 255*g, 255*b)
        return re.sub(r'#(\w)\1(\w)\2(\w)\3', r'#\1\2\3', s)
    else:
        return 'rgba(%d,%d,%d,%0.2f)' % (255*r, 255*g, 255*b, a)


def gradient(x, ranges):
    """
    Sample usage:

        gradient(0.4, ((-1, '#ff0000'), (0, '#ffffff'), (1, '#00ff00')))

    interpolates 0.4 between -1 - 0 - +1 and returns an in-between color
    as #RRGGBB

    The value `x` can also be an array (or any other iterable).
    """

    # If x is an array, apply gradient to each value (potentially recursively)
    if numpy.ndim(x) > 0:
        return [gradient(v, ranges) for v in x]

    x = float(x) if not numpy.isnan(x) else 0
    ranges = sorted(ranges, key=operator.itemgetter(0))
    if x <= ranges[0][0]:
        return ranges[0][1]
    if x >= ranges[-1][0]:
        return ranges[-1][1]
    for i, (start, color) in enumerate(ranges):
        if x <= start:
            break
    p = (x - ranges[i - 1][0]) / (ranges[i][0] - ranges[i - 1][0])
    q = 1. - p
    a = rgba(ranges[i - 1][1])
    b = rgba(ranges[i][1])
    return name(a[0]*q + b[0]*p,
                a[1]*q + b[1]*p,
                a[2]*q + b[2]*p)


def contrast(color):
    """
    Returns a contrasting colour. White, for dark backgrounds,
    and black, for white backgrounds.
    """

    R, G, B, A = rgba(color)

    # See http://www.johndcook.com/blog/2009/08/24/algorithms-convert-color-grayscale/
    luminosity = 0.21 * R + 0.71 * G + 0.07 * B

    return '#000' if luminosity > .5 else '#fff'


def brighten(color, by):
    """
    Brightens a color (e.g. '#ccff00') by `by` percent.
    If `by` is negative, darkens the colour.
    """

    R, G, B, A = rgba(color)
    h, s, v = colorsys.rgb_to_hsv(R, G, B)
    v = max(0, min(1, v * (1 + by)))
    return name(*colorsys.hsv_to_rgb(h, s, v))


_distincts = [
  "#1f77b4", "#aec7e8",
  "#ff7f0e", "#ffbb78",
  "#2ca02c", "#98df8a",
  "#d62728", "#ff9896",
  "#9467bd", "#c5b0d5",
  "#8c564b", "#c49c94",
  "#e377c2", "#f7b6d2",
  "#7f7f7f", "#c7c7c7",
  "#bcbd22", "#dbdb8d",
  "#17becf", "#9edae5"
]

def distinct(n):
    """
    Returns a list of `n` distinct colours
    """
    if n <= 10:
        return [_distincts[2*i] for i in range(0, n)]
    elif n <= 20:
        return _distincts[:n]
    else:
        return _distincts[:]


if __name__ == '__main__':
    assert(rgba('#fff') == (1., 1., 1., 1.))
    assert(rgba('#000000') == (0., 0., 0., 1.))
    assert(rgba('rgb(255, 0% , 100% )') == (1., 0., 1., 1.))
    assert(rgba('rgba( 255  , 0% , 100%,.4)') == (1., 0., 1., .4))
    assert(rgba('hsl(0, 100%, 50%)') == (.5, 0., 0., 1.))
    assert(rgba('hsla(0, 100%, 100%, .9)') == (1., 0., 0., .9))
    assert(rgba('hsla(360, 100%, 100%, 1.9)') == (1., 0., 0., 1.))
    assert(rgba('hsla(360, 0%, 50%, .5)') == (.5, .5, .5, .5))
    assert(hsla('hsla(0, 0%, 50%, .5)') == (0, 0, .5, .5))
    assert(rgba('red') == (1., 0, 0., 1.))
    assert(rgba('white') == (1., 1., 1., 1.))
    assert(name(1, 1, 0) == '#ff0')
    assert(name(-1, 1, 0) == '#0f0')
