<div align="center">
<p align="center">
  <a href=""><img src="https://github.com/Kaguya233qwq/nonebot_plugin_alicdk_get/blob/main/.README_images/d1527335.png?raw=true" width="200" height="200" alt="拿来吧你"></a>
</p>

## nonebot_plugin_alicdk_get

** _✨ ~~一款对阿里云盘说“**拿来吧你！**”的插件~~ ✨_**

</div>

基于nonebot2与aligo的阿里云盘兑换码自动获取和兑换插件。√

通过使用定时任务以秒为计数单位多次向阿里盘盘酱的分享记录发送请求，检测最新的记录是否包含兑换码，若是便会执行自动兑换的逻辑，并通通过bot发送通知给用户。

***阿里盘盘酱每次分享的兑换码都是图片形式，故使用了在线图像识别接口来提取图片内容。（OCR接口失效本项目也会失效。需按时维护）***

### **环境要求：**

aligo：[项目地址](https://github.com/foyoux/aligo)

apscheduler:[项目地址](https://github.com/nonebot/plugin-apscheduler)

### **快速上手**

1.安装本插件。

使用pip包管理器：

`pip install nonebot-plugin-alicdk-get`

或使用nb-cli：

`nb plugin install nonebot-plugin-alicdk-get`

2.第一次启动会弹出二维码，请使用阿里云盘app授权登录。

3.(**必需**)在`.env`文件中修改接收bot消息的群号，兑换成功将会通知您

*(str)*`RECV_GROUP_ID = ""`

4.在任意一个bot所在群内发送启动命令：`[命令前缀符] + sc启动`，即可开始执行监听任务

###### **默认请求频率是每 10秒 一次**

5.守株待兔。

### **进阶 命令列表**

当需要使用监听服务时，您可能需要用到以下命令（需要命令前缀符）：


| 命令      | 作用                                                                 |
| ----------- | ---------------------------------------------------------------------- |
| `sc启动`  | 启动定时器并开启监听服务。                                           |
| `sc关闭`  | 关闭定时器与监听服务。                                               |
| `sc暂停`  | 暂停运行中的监听服务。                                               |
| `sc继续`  | 继续运行监听服务。                                                   |
| `sc间隔x` | x为大于零的数字，表示设置<br />请求间隔为x秒。此过程会开启监听服务。 |
| `sc状态`  | 查询监听服务当前状态。0：停止 1：运行 2：暂停                       |

您也可以不使用监听服务。当您发现有兑换码被发布时，可以直接在有bot的群内发送：

`[命令前缀符] + getcode`或`[命令前缀符] + 福利码`

来手动执行兑换。

### 注意👀️ ：当兑换成功时定时任务将会暂停。如需继续监控请发送继续命令来继续进行监听。

---

#### 有bug请及时反馈，使用过程中有任何问题可以issue或者加我**QQ：1453608435**

<p align="center">
  <a href="https://github.com/"><img src="https://github.com/Kaguya233qwq/nonebot_plugin_alicdk_get/blob/main/.README_images/17623ac4.png?raw=true" width="300" height="350" alt="QRCode"></a>
</p>

---

## 更新日志

2022.9.29-v1.1.1

增加监听状态查询命令

2022.9.29-v1.1

1.优化定时任务逻辑

2.增加命令控制监听服务的运行

3.增加其他错误日志捕获

2022.9.18-v1.0

初始版本
