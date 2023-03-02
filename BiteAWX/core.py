# -*- coding: utf-8 -*-
"""

@author: modabao
@Time: 2023/2/20 08:51
"""

import numpy as np
import xarray as xr
from PIL import Image

from .containers import Head1, Head3, Head2, Head_loc
from .tools import make_coords_dims_attrs, unpack_head, open_seek_read


class AWX(object):
    def __init__(self, path_awx=None):
        self.path = path_awx
        self._byte_order = '<'
        self._head1 = None
        self._head2 = None
        self._head3 = None
        self._values = None
        self._coords = None
        self._product_name = None
        self._palette = None
        self._calibration = None
        self._head_loc = None
        self._positioning = None

    @property
    def head1(self):
        if self._head1 is None:
            buffer = open_seek_read(self.path, 0, 40)
            str_items = (0, 10)
            head1 = unpack_head('<12s9h8sh', buffer, str_items=str_items)
            if head1[1]:
                head1 = unpack_head('>12s9h8sh', buffer, str_items=str_items)
                self._byte_order = '>'
            self._head1 = Head1(*head1)
        return self._head1

    @property
    def head2(self):
        if self._head2 is None:
            head1 = self.head1
            category = head1.category
            try:
                info = Head2[category]
            except KeyError:
                raise KeyError(f'Unkown product category: head1.category={category}')
            buffer = open_seek_read(self.path, 40, head1.head2_length)
            size, format, dataclass, str_items, scale_items = info[1:]
            head2 = unpack_head(
                format, buffer[:size], str_items=str_items, scale_items=scale_items
            )
            self._head2 = dataclass(*head2)
            self._unpack_tables(buffer[size:])
        return self._head2

    @property
    def head3(self):
        if self._head3 is None:
            head1 = self.head1
            head_length = head1.record_length * head1.head_records
            head12_length = head1.head1_length + head1.head2_length + head1.pad_length
            if head_length > head12_length:
                buffer = open_seek_read(self.path, head12_length, 128)
                head3 = unpack_head('64s8s8s8s8s8s8s8s8s', buffer, str_items=range(9))
            else:
                head3 = ()
            self._head3 = Head3(*head3)
        return self._head3

    @property
    def values(self):
        head1 = self.head1
        if head1.compress:
            NotImplementedError('Can\'t process compressed data for now')
        if head1.category == 4:
            NotImplementedError('Can\'t process Points data (head1.category=4) for now')
        if self._values is None:
            head2 = self.head2
            dtype = f'u{head2.word_bytes}'
            shape = (head2.height, head2.width)
            buffer = open_seek_read(self.path, head1.record_length * head1.head_records, None)
            self._values = np.frombuffer(buffer, dtype=dtype).reshape(shape)
        return self._values

    def _unpack_tables(self, buffer):
        if not buffer:
            return
        head2 = self.head2
        col_length = head2.palette_length
        cal_length = head2.calibration_length
        geo_length = head2.positioning_length
        if p := col_length:
            self._palette = np.frombuffer(buffer[:p], 'u1').reshape((3, -1)).T
        if cal_length:
            self._calibration = np.frombuffer(buffer[p : (p := p + cal_length)], 'u2').astype(np.float32) / 100
        if geo_length:
            head_loc = unpack_head('8h', buffer[p : (p := p + 16)], scale_items=range(2, 5))
            self._head_loc = head_loc = Head_loc(*head_loc)
            self._positioning = np.frombuffer(buffer[p:], 'i2')\
                .reshape((head_loc.ny, head_loc.nx, 2))

    @property
    def product_name(self):
        if self._product_name is None:
            if self.head3:
                self._product_name = self.head3.sat2004.split('_')[-5]
            else:
                self._product_name = 'Unknown'
        return self._product_name

    @property
    def calibration(self):
        return self._calibration

    @calibration.setter
    def calibration(self, cali: np.ndarray):
        self._calibration = cali

    def DataArray(self, calibrate=False):
        head2 = self.head2
        coords, dims, attrs = make_coords_dims_attrs(head2)
        add_offset = attrs.get('add_offset', None)
        scale_factor = attrs.get('scale_factor', None)
        data = self.values
        if calibrate and (self._calibration is not None):
            data = self._calibration[data]
        elif calibrate and scale_factor:
            data = data * scale_factor + add_offset
            del attrs['add_offset'], attrs['scale_factor']
        da = xr.DataArray(
            data, coords=coords, dims=dims, name=self.product_name, attrs=attrs
        )
        return da

    def to_netcdf(self, path_nc=None, calibrate=False, complevel=0):
        path_nc = path_nc or self.path + '.nc'
        da = self.DataArray(calibrate)
        if complevel:
            da.encoding['zlib'] = 'True'
            da.encoding['complevel'] = complevel
        ds = da.to_dataset()
        if (not calibrate) and (self._calibration is not None):
            ds = ds.assign_coords(calibration=self._calibration)
        if (positioning := self._positioning) is not None:
            ds = ds.assign_coords(positioning=(da.dims, positioning))
        ds.attrs = {
            'ConvertedBy': 'BiteAWX(modabao)',
            **self.head1.to_attr(),
            **self.head3.to_attr()
        }
        ds.to_netcdf(path_nc)

    def to_pic(self, path_pic=None):
        """保存为图片
        """
        path_pic = path_pic or self.path + '.jpg'
        if getattr(self.head2, 'palette', None):
            im = self._palette[self.values]
        else:
            im = self.values
        Image.fromarray(im).save(path_pic)

