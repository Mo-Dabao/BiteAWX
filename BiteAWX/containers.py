# -*- coding: utf-8 -*-
"""

@Author: modabao
@Time: 2023/2/21 15:51
"""

from typing import Sequence
from typing import NamedTuple
from dataclasses import dataclass, asdict


def _repr(self):
    return (
        f'* {type(self).__name__} *\n' +
        '\n'.join([f'{k}:\t{v}' for k, v in asdict(self).items()])
    )

def _to_attr(self, keys=None, drop=None):
    name = type(self).__name__
    if keys:
        attr = {f'{name}.{k}': getattr(self, k) for k in keys}
    else:
        attr = {f'{name}.{k}': v for k, v in asdict(self).items() if k not in drop}
    return attr


@dataclass(repr=False, eq=False, order=False)
class Head1:
    sat96: str  # Sat96文件名
    byte_order: int  # 整型数的字节顺序
    head1_length: int  # 第一级文件头长度
    head2_length: int  # 第二级文件头长度
    pad_length: int  # 填充段数据长度
    record_length: int  # 记录长度
    head_records: int  # 文件头占用记录数
    data_records: int  # 产品数据占用记录数
    category: int  # 产品类别
    compress: int  # 压缩方式
    version: str  # 格式说明字串
    quality: int  # 产品数据质量标记

    def __repr__(self) -> str:
        return _repr(self)
    
    def to_attr(self):
        return _to_attr(self, keys=('sat96', 'category', 'version', 'quality'))


@dataclass(repr=False, eq=False, order=False)
class Head2GSS:
    satellite: str  # 卫星名
    year: int  # 时间（年）
    month: int  # 时间（月）
    day: int  # 时间（日）
    hour: int  # 时间（时）
    minute: int  # 时间（分）
    channel: int  # 通道号
    projection: int  # 投影方式
    width: int  # 图像宽度
    height: int  # 图像高度
    line_tl: int  # 图像左上角扫描线号
    pixel_tl: int  # 图像左上角象元号
    sampling_rate: int  # 抽样率
    lat_n: int  # 地理范围（北纬）
    lat_s: int  # 地理范围（南纬）
    lon_w: int  # 地理范围（西经）
    lon_e: int  # 地理范围（东经）
    lat_c: int  # 投影中心纬度
    lon_c: int  # 投影中心经度
    prj_std1: int  # 投影标准纬度1（或标准经度）
    prj_std2: int  # 标准投影纬度2
    reso_h: int  # 投影水平分辨率
    reso_v: int  # 投影垂直分辨率
    gridline_flag: int  # 地理网格叠加标志
    gridline_value: int  # 地理网格叠加值
    palette_length: int  # 调色表数据块长度
    calibration_length: int  # 定标数据块长度
    positioning_length: int  # 定位数据块长度
    reserved: int  # 保留
    word_bytes: int = 1  # 默认字长为1字节

    def __repr__(self) -> str:
        return _repr(self)
    
    def to_attr(self):
        return _to_attr(
            self, drop=(
                'palette_length', 'calibration_length', 'positioning_length',
                'reserved', 'word_bytes'
            )
        )


@dataclass(repr=False, eq=False, order=False)
class Head2POS:
    satellite: str  # 卫星名
    year: int  # 开始时间（年）
    month: int  # 开始时间（月）
    day: int  # 开始时间（日）
    hour: int  # 开始时间（时）
    minute: int  # 开始时间（分）
    year_end: int  # 结束时间（年）
    month_end: int  # 结束时间（月）
    day_end: int  # 结束时间（日）
    hour_end: int  # 结束时间（时）
    minute_end: int  # 结束时间（分）
    channel: int  # 通道号
    channel_r: int  # R通道号
    channel_g: int  # G通道号
    channel_b: int  # B通道号
    ascending: int  # 升降轨标志
    orbit: int  # 轨道号
    word_bytes: int  # 一个像元占字节数
    projection: int  # 投影方式
    product: int  # 产品类型
    width: int  # 图像宽度
    height: int  # 图像高度
    line_tl: int  # 图像左上角扫描线号
    pixel_tl: int  # 图像左上角像元号
    sampling_rate: int  # 抽样率
    lat_n: int  # 地理范围（北纬）
    lat_s: int  # 地理范围（南纬）
    lon_w: int  # 地理范围（西经）
    lon_e: int  # 地理范围（东经）
    lat_c: int  # 投影中心纬度
    lon_c: int  # 投影中心经度
    prj_std1: int  # 投影标准纬度1（或标准经度）
    prj_std2: int  # 标准投影纬度2
    reso_h: int  # 投影水平分辨率
    reso_v: int  # 投影垂直分辨率
    gridline_flag: int  # 地理网格叠加标志
    gridline_value: int  # 地理网格叠加值
    palette_length: int  # 调色表数据块长度
    calibration_length: int  # 定标数据块长度
    positioning_length: int  # 定位数据块长度
    reserved: int  # 保留

    def __repr__(self) -> str:
        return _repr(self)

    def to_attr(self):
        return _to_attr(
            self, drop=(
                'palette_length', 'calibration_length', 'positioning_length',
                'reserved', 'word_bytes'
            )
        )


@dataclass(repr=False, eq=False, order=False)
class Head2Grd:
    satellite: str  # 卫星名
    product: int  # 格点场要素
    word_bytes: int  # 格点数据字节
    add_offset: int  # 格点数据基准值  # 实际数据=（格点数据+基准值）/比例因子  # bad
    scale_factor: int  # 格点数据比例因子  # bad
    time_flag: int  # 时间范围代码
    year: int  # 开始年
    month: int  # 开始月
    day: int  # 开始日
    hour: int  # 开始时
    minute: int  # 开始分
    year_end: int  # 结束年
    month_end: int  # 结束月
    day_end: int  # 结束日
    hour_end: int  # 结束时
    minute_end: int  # 结束分
    lat_n: int  # 网格左上角纬度
    lon_w: int  # 网格左上角经度
    lat_s: int  # 网格右下角纬度
    lon_e: int  # 网格右下角经度
    reso_unit: int  # 格距单位
    reso_h: int  # 横向格距
    reso_v: int  # 纵向格距
    width: int  # 横向格点数
    height: int  # 纵向格点数
    land_flag: int  # 有无陆地判释值
    land_value: int  # 陆地具体判释值
    cloud_flag: int  # 有无云判释值
    cloud_value: int  # 云具体判释值
    water_flag: int  # 有无水体判释值
    water_value: int  # 水体具体判释值
    ice_flag: int  # 有无冰体判释值
    ice_value: int  # 冰体具体判释值
    qc_flag: int  # 是否有质量控制值
    qc_upper: int  # 质量控制值上限
    qc_lower: int  # 质量控制值下限
    reserved: int  # 备用
    projection: int = 4  # 默认等经纬度投影

    def __repr__(self) -> str:
        return _repr(self)

    def to_attr(self):
        return _to_attr(self, drop=('reserved', 'word_bytes'))


@dataclass(repr=False, eq=False, order=False)
class Head2Pts:
    satellite: str  # 卫星名
    product: int  # 要素
    words: int  # 每个记录多少个字
    points: int  # 探测点总数
    year: int  # 开始年
    month: int  # 开始月
    day: int  # 开始日
    hour: int  # 开始时
    minute: int  # 开始分
    year_end: int  # 结束年
    month_end: int  # 结束月
    day_end: int  # 结束日
    hour_end: int  # 结束时
    minute_end: int  # 结束分
    inversion: int  # 反演方法类型
    first_guess: int  # 初估场类型
    missing_value: int  # 缺省值
    word_bytes: int = 2  # 默认字长为2字节

    def __repr__(self) -> str:
        return _repr(self)

    def to_attr(self):
        return _to_attr(self, drop=('word_bytes',))


@dataclass(repr=False, eq=False, order=False)
class Head3:
    sat2004: str = ''  # Sat2004文件名
    format_version: str = ''  # 格式版本号
    manufacturer: str = ''  # 生产商
    satellite: str = ''  # 卫星名
    instrument: str = ''  # 仪器名
    program_version: str = ''  # 处理程序的版本号
    reserved: str = ''  # 保留
    copy_right: str = ''  # 版权
    pad_length: str = ''  # 扩展段的填充段长度

    def __repr__(self) -> str:
        return _repr(self) if self.sat2004 else '* No Head3 found *'

    def __bool__(self):
        return bool(self.sat2004)
    
    def to_attr(self):
        return _to_attr(self, drop=('reserved', 'pad_length')) if self.sat2004 else {}


class Head2info(NamedTuple):
    category: int
    size: int
    format: str
    dataclass: type
    str_items: Sequence
    scale_items: Sequence


Head2 = {
    1: Head2info(1, 64, '8s28h', Head2GSS, (0,), range(13, 23)),
    2: Head2info(2, 88, '8s40h', Head2POS, (0,), range(29, 35)),
    3: Head2info(3, 80, '8s36h', Head2Grd, (0,), range(16, 20)),
    4: Head2info(4, 40, '8s16h', Head2Pts, (0,), ())
}


@dataclass(repr=False, eq=False, order=False)
class Head_loc:
    coord_type: int  # 网格点坐标定义
    src: int  # 网格数据来源
    reso: int  # 网格度数
    lat_n: int  # 左上角网格点纬度
    lon_w: int  # 左上角网格点经度
    nx: int  # 横向网格点数
    ny: int  # 纵向网格点数
    reserved: int  # 保留

reso_units = {
    0: 0.01,  # °
    1: 1000,  # m
    2: 1,  # m
    9: 0.5625  # °
}

lat_attrs = {
    'units': 'degrees_north',
    'long_name': 'latitude coordinate',
    'standard_name': 'latitude'
}

lon_attrs = {
    'units': 'degrees_east',
    'long_name': 'longitude coordinate',
    'standard_name': 'longitude'
}

x_attrs, y_attrs = [
    {
        'units': 'm',
        'long_name': f'{_} coordinate of projection',
        'standard_name': f'projection_{_}_coordinate'
    } for _ in 'xy'
]
