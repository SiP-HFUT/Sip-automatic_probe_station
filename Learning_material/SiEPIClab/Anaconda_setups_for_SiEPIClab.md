# Anaconda setup for runing SiEPIClab

该目录下的所有程序，源于[SiEPIClab](https://github.com/SiEPIC/SiEPIClab)（原名：PyOptomip）。其使用指引，可见本目录下的 PyOptomip User's Guide.pdf 文件。另外，自动测试中所使用的设备及相关用户手册，也可见本目录的 Instrument Information.pdf 文件。

该程序，可以为搭建我们的自动化测试平台，提供非常宝贵的方法模板。

原程序运行时，可能会出现和visa模块有关的错误。该错误可能和pyvisa的版本更新有关。为了解决该问题，我将程序中，所有`import visa`语句改为`import pyvisa as visa`。

这里总结了个人配置Anaconda的相关步骤，使得我们可以初步运行此程序，并调出起始的GUI。我想这对于进一步学习该程序的实现方法，是有帮助的。



总结的步骤如下：

1. 安装[Anaconda](https://www.anaconda.com/)

2. 现在版本的Anaconda ，其默认环境是基于Python 3。但是目前所使用的稳定的pyOptomip程序软件是基于Python 2. 因此，我们需要在Anaconda 中，创建一个新的基于Python 2语言的环境，其步骤为：

   1. 在Anaconda 的Prompt中，创建新的名为py2的环境，其编译语言基于Python2，具体操作见： [Switching between Python 2 and Python 3 environments](https://docs.anaconda.com/anaconda/user-guide/tasks/switch-environment/)

   2. 继续在Prompt中，利用`activate py2`，转换至创建的新环境。之后在Prompt，为所创建的环境，安装一系列项目程序所需要的模块：

      - 通过命令 ` pip install spyder-kernels==2.2.1`s，安装spyder-kernels模块，其版本号需要满足>=2.2.1且 <2.3.0。待会我们在Spyder上运行python2时，需要该模块。
      - 通过命令` pip install wxpython`，安装wxpython模块（我运行该命令安装此模块时，出现了错误，后来通过在Anaconda Navigator中搜索wxpython，手动安装了该模块）
      - 通过命令`pip install numpy`，安装numpy模块
      - 通过命令`pip install matplotlib`，安装matplotlib模块
      - 通过命令`pip install pyvisa`，安装pyvisa模块
      -  通过命令`pip install comtypes`，安装comtypes模块
      - 通过命令`pip install pyvisa-py`，安装pyvisa-py模块

   3. 在Anaconda Navigator中，打开Spyder（此时不需要切换到新环境） 。在 Tools--Preferences--Python interpreter中, 将Python编译器改为Python2。需要输入Python2中python.exe的路径。该路径在Anaconda安装目录中的envs文件夹。对于我的电脑，路径为：C:/Users/Rui/anaconda3/envs/py2/python.exe

   4. 在Spyder中，打开pyOptomip.pyw并运行，之后可能会出现和visa有关的错误，该错误可能和pyvisa的版本更新有关。我将pyOptomip文件夹中，所有`import visa`改为`import pyvisa as visa`，该问题解决（该目录下的程序，此语句已经改动）。

   5. 顺利运行pyOptomip.pyw后，将出现下面的GUI窗口，表示程序启动成功。

      <img src="../md_files/Initial_GUI.png" style="zoom:60%;" />

