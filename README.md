# BestCF

一个具有自动定时更新阿里云DNS解析为CloudFlare优选IP的Python脚本。

## 支持平台

支持Windows、Linux、macOS

## 使用

首先安装Python依赖

``` shell
pip install -r requirements.txt
```

下载对应系统版本的 [CloudflareSpeedTest](https://github.com/XIU2/CloudflareSpeedTest/releases) 并将文件解压至脚本同一目录。

然后编辑脚本内的需要修改的变量

配置完成后运行脚本即可

```shell
python main.py
```
