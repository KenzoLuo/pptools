# ds2v后处理脚本简介

罗健 2020.02.02

## 目的

DS2V程序的输出文件可以被作者提供的桌面程序进行读取以及可视化，但实际使用中，有时需要在Tecplot等可视化工具中对流场进行进一步的分析，为了减少重复劳动编写此后处理脚本。脚本可以在服务器端对计算数据进行处理，方便在计算过程中观察流场的演化与发展，同时，计算结束后也不必将完整的计算数据下载到本地。

目前支持对钝头体流动和Couette流动进行后处理，后续可以按需求添加功能

对于钝头体流动  
>1 流场数据更改为Tecplot格式，并丢弃NaN项。默认保存为“grid_resaved.dat”，可以通过`outfile`关键字自定义输出文件名为“grid_outfile”  
>2 通过关键字`stagl`提取驻点线数据，并自动绘制驻点线上的各个温度变化曲线，并存为“temp_sl.png”  
>3 通过关键字`surf`提取壁面个物理量的分布，默认保存为“surf_resaved.dat”，可以通过`outfile`关键字自定义输出文件名为“surf_outfile”  
>4 通过关键字`prof`提取通过某一点驻点下游垂直于壁面的流场剖面，自动绘制剖面上的速度和温度变化曲线，并保存为“shear_profile.png”，目前不支持自定义剖面位置和角度  
>5 通过算法拟合输出驻点热流

对于Couette流动  
>1 将流场数据沿切向进行平均，将二维流场数据压缩为一维的，数据另存为“resaved.dat”，同样可以通过`outfile`来自定义  
>2 绘制并保存Couette流场速度和温度剖面，方便在计算式观察流场发展情况  
>3 通过关键字`norm`可以对流场进行归一化，当前归一化方式为$u/upu$，$temp/uptemp$，$tvib/uptvib$  
>4 统计平均后输出下壁面的热流

## 语法

基本语法

```bash
pp4ds2v.py blunt/couette keyword args ...
```

对于钝头体流动：

```bash
pp4ds2v.py blunt outfile filename.dat stagl yes/no surf yes/no prof yes/no
```

对于Couette流动

```bash
pp4ds2v.py couette outfile filename.dat norm upu uptemp uptvib
```

各个选项的默认值都是no，`norm`的默认值为$(1,1,1)$，即不进行归一化。
