# pp4sparta后处理脚本简介

## 语法

### 基本语法

```bash
pp4sparta.py infile headfile outfile keyword args ...
```

前三个参数`infile headfile outfile`为必须的，`keyword args`是非必须的，可以根据需要添加，当前支持以下功能：

>1. `frac` 按照一定比例压缩输出文件。例如`frac 0.5`，即压缩文件为原始文件的一半大小。（原理，随机删除一定比例的网格）
>2. `cut` 裁剪掉box中不在流场中的部分。由于sparta导出的grid信息是包含流场box的所有部分，有时为了减小计算量，会在来流出添加一个合适的入口边界surf，从而使得输出文件中有部分区域不在流场，但仍会被输出，各项流动信息都是0，属于无效的数据，可以将网格内的粒子数密度作为判据，网格内粒子数密度小于1e-6，则删除这一网格信息。`cut num`即裁剪掉这部分区域，且指明粒子数密度n为第`num`列，默认不进行此操作

### 举例

```bash
pp4sparta.py grid24000 head.txt grid_resaved.plt cut 3 frac 0.3
```

表示处理grid24000文件，输出文件中各列的含义在head.txt的文件的第一行提供，将计算box中没有粒子分布的区域裁剪掉，表示粒子数密度的列是第三列。随机删除70%的网格的信息，使文件大小压缩到原来的30%。将处理后的文件另存为grid_resaved.plt

### headfile

headfile主要提供tecplot文件的头信息，后处理程序只读取第一行，其余行的内容可以留着备用。

```text
VARIABLES= x y n den u v Trot Tvib Ttra p MFP Kncell
___ the rest lines will not been read ___
VARIABLES= id x y z n den u v w Ttra p
......
```
