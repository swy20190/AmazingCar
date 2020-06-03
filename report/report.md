# 基于树莓派的避障小车设计
——嵌入式系统开发课程设计
<https://github.com/swy20190/AmazingCar>
## 作者与分工
### 隋唯一
- 清华大学软件学院
- 学号：2017011430
- <MidnightSun114514@gmail.com>
- 分工：基础算法设计、程序架构、参数调节、文档
### 靳紫荆
- 清华大学软件学院
- 学号：2016011990
- <jinzj16@163.com>
- 分工：参数调节、测试、文档
### 邓坤恬
- 清华大学软件学院
- 学号：2017013655
- 分工：参数调节、测试、文档
## 功能及其实现
### 基础功能
- 前进一米并刹车
- 后退一米并刹车
- 向前行进间左转弯
- 向前行进间右转弯
实现方法：
编写函数init(), forward(...), brake(...), backward(...), turn(...), advanced\_turn(...), 分别用于初始化引脚，前进，刹车，差速转向，指定半径的差速转向。依次执行，即可完成全部任务。
### 直线竞速
编写程序[fullfullahead.py](../code/fullfullahead.py)，测量小车全速前进的速度（感谢王婷助教）。在得到的数据的基础上，编写程序[racing.py](../code/racing.py)。其核心即为一个forward()函数，速度设置为100（即全速前进）。需要注意的是，由于小车本身的误差，在前进的过程中小车会向右跑偏，所以编写了short\_left(...)函数，用于在中途使小车向左转动一个小角度。整体的思路是，先全速前进2.5米，然后向左调整，然后全速前进2.5米，过线之后，首先调用brake(...)刹车，然后调用backward(...)辅助刹车。
值得一提的是，经过测量（再次感谢王婷助教），小车实际运行距离是520厘米，一个美妙的数字。
### 圆周避障
编写程序[circle.py](../code/circle.py)，完成任务。程序中实现了measure(...)函数，以完成超声波测距。由于车轮打滑的原因，所以小车转弯半径远大于我们所计算的一米。这里感激杨松洲助教，他的测量帮助我们将相应参数调整到位。实现的思路是这样的：小车先原地右转90度，然后每次只运动长10厘米的弧，然后停车测量，若距离墙壁大于10厘米，则再移动10厘米，否则原路返回。如是循环。
## 算法说明
前两个功能均为顺序执行，最后一个使用一个while循环，若小车距离障碍不足10厘米，则退出循环，进入倒车环节，否则继续循环，每次移动10厘米。