# -*- coding: utf-8 -*-
"""

@Author: modabao
@Time: 2023/2/23 10:27
"""

from datetime import datetime
from struct import unpack
from typing import Union

import numpy as np
import xarray as xr
from pyproj import CRS, Proj

from .containers import Head2GSS, Head2Grd, Head2POS, Head2Pts, reso_units, lat_attrs, lon_attrs, x_attrs, y_attrs


def unpack_head(format, buffer, str_items=(), scale_items=()) -> list:
    head = list(unpack(format, buffer))
    for n in str_items:
        head[n] = head[n].strip(b'\x00').decode()
    for n in scale_items:
        head[n] /= 100
    return head


def open_seek_read(path, offset=0, size=None):
    with open(path, 'rb') as f:
        f.seek(offset)
        return f.read(size)


def make_coords_dims_attrs(head2: Union[Head2GSS, Head2POS, Head2Grd, Head2Pts], values: np.ndarray):
    time = datetime(*[getattr(head2, _) for _ in ['year', 'month', 'day', 'hour', 'minute']])
    if isinstance(head2, Head2Pts):
        coords = dict(
            lat=('index', values[:, 0] / 100, lat_attrs),
            lon=('index', values[:, 1] / 100, lon_attrs),
            p=('index', values[:, 2], {'units': 'hPa', 'standard_name': 'pressure'}),
            time=time
        )
        dims=('index',)
        attrs = head2.to_attr()
    else:
        projection, height, width = [getattr(head2, k) for k in ('projection', 'height', 'width')]
        lat_n, lat_s, lon_w, lon_e = [
            getattr(head2, _) for _ in ['lat_n', 'lat_s', 'lon_w', 'lon_e']
        ]
        if projection == 4:
            projparams = 'WGS84'
            coords = dict(
                lat=('lat', np.linspace(lat_n, lat_s, height), lat_attrs),
                lon=('lon', np.linspace(lon_w, lon_e, width), lon_attrs),
                time=time
            )
            dims=('lat', 'lon')
        else:
            lat_0, lon_0, std_1, std_2 = [
                getattr(head2, k) for k in ('lat_c', 'lon_c', 'prj_std1', 'prj_std2')
            ]
            reso_unit = reso_units[getattr(head2, 'reso_unit', 1)]  # default resolution 1000m
            reso_v, reso_h = [getattr(head2, _) * reso_unit for _ in ['reso_v', 'reso_h']]
            dims = ('y', 'x')
            if projection == 1:
                projparams = f'+proj=lcc +lon_0={lon_0} +lat_0={lat_0} +lat_1={std_1} +lat_2={std_2}'
            elif projection == 2:
                projparams = f'+proj=merc +lon_0={lon_0} +lat_ts={std_1}'
            elif projection == 3:
                projparams = f'+proj=stere +lon_0={lon_0} +lat_0={lat_0}'
                print('Warning: Stereographic projection hasn\'t been test!')
            else:
                NotImplementedError(f'Unsupported head2.projection: {projection}')
            x0, y0 = Proj(projparams, preserve_units=False)(lon_0, lat_0)
            x_half, y_half = reso_h * (width - 1) / 2, reso_v * (height - 1) / 2
            l, r = x0 - x_half, x0 + x_half
            s, n = y0 - y_half, y0 + y_half
            coords = dict(
                y=('y', np.linspace(n, s, height), y_attrs),
                x=('x', np.linspace(l, r, width), x_attrs),
                time=time
            )
        projparams = CRS(projparams).to_json_dict()
        projparams['name'] = 'AWX custom projection'
        crs = CRS(projparams)
        coords['crs'] = xr.DataArray(attrs=crs.to_cf())
        attrs = head2.to_attr()
        if isinstance(head2, Head2Grd):
            # make `add_offset`, `scale_factor` CF-convention style
            add_offset, scale_factor = attrs['Head2Grd.add_offset'], attrs['Head2Grd.scale_factor']
            add_offset, scale_factor = add_offset / scale_factor, 1 / scale_factor
            attrs['add_offset'], attrs['scale_factor'] = add_offset, scale_factor
        attrs = {
            'grid_mapping': 'crs',
            'coordinates': ' '.join(dims),
            **attrs
        }
    return coords, dims, attrs


