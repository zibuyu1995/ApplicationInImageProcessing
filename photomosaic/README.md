# python openCv 实现蒙太奇马赛克图像(2019-1-31)

### 原理:
* 递归查询预选文件夹下的所有图像动态调整大小
* 建立每个预选图像的hsv索引
* 计算原图像hsv，与预选图像索引做比对


### 运行:
* 安装虚拟环境:
```bash
pip install requirements.txt
```
