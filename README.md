# BiteAWX

国家卫星气象中心AWX格式文件读取库。

## 安装

```
pip install BiteAWX
```

第三方包依赖包括

`numpy; xarray; pyproj; pillow; netCDF4`

## 功能

- 查看各级头信息
- 读取原始数据块为numpy数组
- 读取为定标/未定标xarray数组
- 修改定标表
- 另存为netCDF4文件，可选是否定标、压缩
- 另存为图片

## 使用方式

```python
from BiteAWX import AWX

path_awx = './test_data/ANI_IR2_R01_20230217_0800_FY2G.AWX'
awx = AWX(path_awx)

# 读取原始数据为np.ndarray
array = awx.values

# 读取原始数据为xarray.DataArray
da = awx.DataArray()

# 读取定标后为xarray.DataArray
da = awx.DataArray(calibrate=True)

# 查看定标表
calibration = awx.calibration

# 修改定标表
import numpy as np
calibration = np.arange(len(calibration)) * calibration[1]
awx.calibration = calibration

# 读取新定标后为xarray.DataArray
da = awx.DataArray(calibrate=True)

# 查看各级头信息
print(awx.head1, '\n')
print(awx.head2, '\n')
print(awx.head3)

# 另存为nerCDF4文件
# Windows下路径中不得有中文
awx.to_netcdf()  # 在原AWX文件绝对路径后加`.nc`保存定标后数据
awx.to_netcdf(path='where/what.nc')  # 指定路径和文件名
awx.to_netcdf(calibrate=False)  # 不定标，定标表将存为`calibration`维度变量
awx.to_netcdf(complevel=1)  # 压缩，complevel取值范围0-9，默认为0不压缩

# 另存为图片
awx.to_pic()  # 在原AWX文件绝对路径后加`.jpg`保存
awx.to_pic(path='where/what.jpg')  # 指定路径和文件名
```

## 注意

- 已测试数据有限，可能存在Bug，欢迎提issue
- 不要过于信任MICAPS4的显示范围，它的投影参数可能有问题
- 投影信息存储遵循CF-Conventions，所以暂时没有强制提供经纬度网格
- 暂不支持离散场产品数据的提取，但应当可以读取各级头信息
- 要素名称从三级头信息的sat2004文件名提取，否则默认为`Unknown`

## TODO

- 详细文档
- 增加强制提供经纬度网格的选项
- 增加作为xarray的backend
- 支持离散场产品数据
- 支持手动定义要素名
