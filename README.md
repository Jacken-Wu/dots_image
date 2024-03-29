# dots_image

将图片转换为字符图片（基于盲文字符的字符图片）

## 原理

本脚本使用 Unicode 的 braille pattern dots 字符进行字符串图像的绘制。  
braille pattern dots由 0 ~ 8 个点构成，共 256 个字符，从 \u2800 开始，到 \u28FF 结束，字符的编码方式如下：  
首先对 8 个点位进行编号：  
&emsp;&emsp;&emsp;&emsp; 1 &emsp; 4  
&emsp;&emsp;&emsp;&emsp; 2 &emsp; 5  
&emsp;&emsp;&emsp;&emsp; 3 &emsp; 6  
&emsp;&emsp;&emsp;&emsp; 7 &emsp; 8  
从 \u2800 开始，编号为 n 的点位，有连续 2^(n-1) 个字符为空，紧接着连续 2^(n-1) 个字符为填充，如此循环。  
例如：对于 3 号点位，\u2800 ~ \u2803 均为空白，\u2804 ~ \u2807 有黑点填充，\u2808 ~ \u280B 又是空白……  
根据这个编码规律，可以找到需要的字符。  

## 使用

直接运行 dots_img.py 脚本即可，更改 generate() 中的参数即可改变生成的字符图片的宽度。
