<div align=center><img src=images/logo.png width=30% ></div>

# Mars

Mars(战神),对之前的[WDScanner](https://github.com/TideSec/WDScanner)的全新重写，结合Tide潮汐资产探测和指纹识别方面的技术积累，可以为客户提供更高效智能的安全检测和安全监测服务。

之所以取名为Mars(战神)，因为设计初衷是想做个专门挖SRC的平台，能自动化的比较全面的搜集资产信息并能监测资产的变化情况，及时发现新应用或新服务，并能自动化匹配POC进行检测，进而提高SRC漏洞挖掘效率，所以在资产发现、指纹探测、变更监测方面做的稍微细致一些。

平台适用人群：

- 1、**白帽子**。Mars可对SRC进行资产搜集、资产变更监测。
- 2、**乙方安服团队**。可对客户资产进行监测管理，出现新漏洞第一时间感知。
- 3、**甲方安运团队**。可对内网资产和互联网资产进行周期性探测，发现新端口、内容变更等。
- 4、**红蓝对抗**。可用于前期资产搜集、信息搜集，动作比较小。

由于个人不大会做前端，所以平台框架直接使用了jeffzh3ng大佬的[fuxi](https://github.com/jeffzh3ng/fuxi)项目，在此致敬大佬的开源精神。Mars平台使用了flask+vali-admin做为前端，python作为后台扫描脚本，可使用分布式的节点扫描模式，可以对资产探测、POC检测、弱口令检测、漏洞扫描等任务分多个节点来完成。

项目Github地址：[https://github.com/TideSec/Mars](https://github.com/TideSec/Mars)

# 声明

**本平台只是对目标系统进行信息搜集和端口开放性探测，漏洞扫描调用了wvs的扫描Api。对互联网任何目标的检测均需在取得授权后方可进行，如需测试本平台可用性请自行搭建靶机环境。若使用者因此做出危害网络安全的行为后果自负，与作者无关，特此声明。**

# Change Log

- [2020-05-11] 更新了几个Bug~
- [2020-05-10] 一期开源~
- [2019-05-07] 团队内部搭建测试使用
- [2019-04-02] POC检测、弱口令检测完成
- [2019-03-18] 资产探测完成
- [2019-02-22] 完成部分核心功能
- [2019-01-15] 规划整体架构
 
**tips：** 2020年5月11日，代码略有更新，主要修复几个bug，可在docker中的中进行代码更新。
```
cd /root/Mars && git pull
```
# Abstract

主要功能：客户管理、资产发现、子域名枚举、C段扫描、资产变更监测、端口变更监测、域名解析变更监测、Awvs扫描、POC检测、web指纹探测、端口指纹探测、CDN探测、操作系统指纹探测、泛解析探测、WAF探测、敏感信息检测、分布式多节点扫描等等。目前被动扫描准备对接xray+wascan，准备二期开源该功能及其他若干功能。

# Install

## Demo演示

在阿里云上搭建了一个演示站点，可以先浏览下大体功能，看是不是你想要的。

Mars(战神)：[http://mars.tidesec.com](http://mars.tidesec.com)

因为是演示站点，我使用一个只读权限的账号，所以只能查看，没法增删改的。另外，demo站关闭了wvs，所以漏洞扫描模块没法查看。想体验完整版的需要自己本地搭建了~~

## docker安装

我把mongodb、awvs、hydra、扫描任务等都集成到docker里面了，可直接使用，镜像略大。

自己安装docker后，从docker仓库拉取镜像
```
docker pull registry.cn-hangzhou.aliyuncs.com/secplus/mars:1.0
```
![pic](images/pic20.png)

创建docker
```
docker run --name tide-mars  -p 5000:5000 -p 27017:27017  -p 13443:13443 -h tide-mars -d registry.cn-hangzhou.aliyuncs.com/secplus/mars:1.0  /usr/sbin/sshd -D
```

启动Mars平台（如果主机配置低的话建议不启动Awvs，不然会卡死的，不想启动Awvs注释start.sh文件中第三行就可以）
```
docker exec tide-mars  /bin/bash -c '/bin/bash /root/Mars/start.sh'
```

之后就可以使用浏览器访问`http://ip:5000`(这个ip是你的docker母机的地址)来访问mars了，登录密码默认为`tidesec`。

同时浏览器可访问`https://ip:13443`，账号`tide@tidesec.com/Tide@2020`，查看awvs状态。

![pic](images/pic12.png)

在创建容器以后，如果docker停止了，再次运行(不需要重新创建容器)只需要执行下面命令
```
dk start tide-mars && docker exec tide-mars  /bin/bash -c '/bin/bash /root/Mars/start.sh'
```
### 错误排查

如果无法打开5000端口或13443端口、或者添加任务后无法扫描，可以进入docker进行人工排查。
```
docker exec -it tide-mars /bin/bash
```
启动数据库
```
nohup mongod --dbpath=/data/db --bind_ip 0.0.0.0 --auth &
```
启动mars控制台
```
cd /root/Mars && python mars.py
```
启动扫描任务
```
cd /root/Mars/taskpython/ && python asset_task_scan_v1.0.py
```
启动awvs(可选，不启动时无法使用漏洞扫描功能)
```
su -l acunetix -c /home/acunetix/.acunetix_trial/start.sh
```

使用`ps -aux`可看到mar.py、数据库和wvs均已启动。

![pic](images/pic21.png)

## 分布式部署

Mars支持分布式部署，可以多节点同时扫描，空闲节点会优先执行任务，节点任务相互没有干扰。

- 在web控制台添加多个任务；
- 每个节点接收任务后会把该任务进行标记，这样其他节点不会重复扫描；
- 如果某节点因为出错而导致没有完成扫描，下次该节点再次启动时会继续执行该任务；
- 节点的标识是靠`taskpython/asset_task_scan_v1.0.py`文件中的`scan_node`参数，默认是主机名，可自行修改。

**多节点的部署方式：**
- 1、把`taskpython`目录拷贝到其他服务器上。
- 2、安装依赖包`pip install -r requirements.txt`
- 3、修改`asset_task_scan_v1.0.py`文件中的`MONGODB_CONFIG`的mongo数据库地址。
- 4、运行`python asset_task_scan_v1.0.py`即可。


## 手工安装

非常不建议手工从头安装，如果是想二次开发，可以自行摸索安装。

# Function

## 登录界面
直接使用的vali-admin内置的一个lockscreen页面，改了个比较灰主流的背景，原谅我的审美。
登录密码默认为`tidesec`，在配置文件`Mars/instance/config.py`中设置，可以自行修改，修改后需要重启下`python mars.py`脚本，先kill掉`python mars.py`进程，再执行一下`python mars.py`就行。

![pic](images/pic1.jpg)

## 用户管理
添加用户和管理用户：设置用户联系人、手机、邮箱等，可以进行漏洞预警，设置服务周期和服务类型，比如定期的漏洞扫描、POC检测、弱口令检测、敏感字检测等。

![pic](images/pic2.jpg)

## 资产管理
资产管理是整个平台最基础也算最核心的功能，对资产进行POC检测或者弱口令检测，首先依赖于资产能被发现、指纹能被识别。

比如通过资产探测发现某服务器使用了iis，那么系统会自动调用IIS短文件名检测POC、IIS PUT检测POC进行自动检测，如果发现使用了weblogic会把weblogic的所有反序列化漏洞POC都检测一遍，如果发现系统使用了Mysql，会自动调用mysql弱口令检测程序进行弱口令测试，等等。这些能自动检测的前提就是能发现资产指纹信息，目前我们也搭建了自己的潮汐指纹识别平台，目前已经开源[http://finger.tidesec.com](http://finger.tidesec.com)。

![pic](images/pic15.png)

添加资产时，平台会根据资产类型进行智能分类，比如你添加了test.gauzi.com和app.gauzi.com和www.maodou.com作为资产，平台会把该任务分为两个具体任务，一个是guazi.com，里面包括两个资产test.gauzi.com和app.gauzi.com，另一个是maodou.com，里面包括www.maodou.com作为资产。

之后后台会自动进行子域名枚举，子域名枚举共使用了四种方式以保证子域名枚举的全面，并把这些子域名都作为该资产任务下的具体资产。

子域名枚举的四种方式：
- 1、`https://github.com/aboul3la/Sublist3r`，对接了N多接口。
- 2、`https://github.com/lijiejie/subDomainsBrute`，主要是字典枚举。
- 3、使用baidu进行子域名检索。
- 4、对主域名进行三层页面爬取，提取子域名。

之后会对这些子域名进行探测信息，可以根据策略配置“web端口快速探测”扫描全端口还是部分端口，而且在分析过程中如果发现子域名对应的ip集中在某个C段（启用“探测C段”选项时），那么平台会自动把该C段IP也作为资产任务进行扫描探测，并写入数据库进行呈现。

![pic](images/pic3.jpg)

![pic](images/pic4.jpg)

![pic](images/pic5.jpg)

![pic](images/pic14.png)

## 指纹识别

可识别的指纹包括：web应用指纹、操作系统指纹、中间件指纹、waf指纹、CDN信息、前端指纹信息、IP归属地、IP所在GPS信息、标题状态等。

![pic](images/pic6.png)

## 变更监测

当设置了周期扫描时，若该资产在扫描时发现开放了新端口，那么该资产会被标识为资产存在变更。除了监测端口变更外，还会对标题、网站状态、IP解析进行监测，如果出现了变更，也会被标识出来。

![pic](images/pic16.png)
![pic](images/pic17.png)

## POC检测

这个模块直接调用了pocsuite进行poc扫描，可对所有资产进行检测。新建任务时可以从资产里直接选择，也可以手工添加。jeffzh3ng大佬设计了一个可以直接把POC文件拖拽的功能，很棒。后续准备根据资产指纹来对资产进行分组，这样POC检测能更智能一些。

poc管理
![pic](images/pic9.png)

新建POC任务
![pic](images/pic10.png)

poc结果
![pic](images/pic11.png)

## 漏洞扫描

漏洞扫描直接调用了AWVS的API接口，我在docker里也配置好了Awvs，是2019年7月的linux版的，想升级的自己可以升级。本来是想做成和WDScanner一样，把所有漏洞存在mongo数据库中，由于精力不准暂时没完成。

![pic](images/pic19.png)

由于该扫描是直接调用的Awvs的API接口，所以在awvs没启动的时候，该功能不可用。

![pic](images/pic18.png)

不过在使用docker环境执行awvs扫描时，发现占用资源很多wvs很容易报错，同时会导致web应用打开都比较费劲。自己部署的时候可以把wvs使用单独的服务器部署，然后在配置文件`Mars/instance/config.py`中修改awvs地址和api的key就可以。

![pic](images/pic13.png)

##  认证检测

认证检测主要是对弱口令进行检测，调用了hydra来完成该任务。

新建弱口令任务
![pic](images/pic7.png)

弱口令检测结果
![pic](images/pic8.png)

# ToDo

- 资产按指纹智能分类，直接匹配POC
- 融合被动扫描Xray+WASCAN
- AWVS结果本地存储后控制台直接查看
- 导出结果和报告

# Thanks

jeffzh3ng大佬：https://github.com/jeffzh3ng/
Tide安全团队的小伙伴：http://www.tidesec.com

# 关于Tide安全团队

Tide安全团队致力于分享高质量原创文章，研究方向覆盖网络攻防、Web安全、移动终端、安全开发、IoT/物联网/工控安全等多个领域，对安全感兴趣的小伙伴可以关注或加入我们。

Tide安全团队自研开源多套安全平台，如Tide(潮汐)网络空间搜索平台、潮启移动端安全管控平台、分布式web扫描平台WDScanner、Mars网络威胁监测平台、潮汐指纹识别系统、潮巡自动化漏洞挖掘平台、工业互联网安全监测平台、漏洞知识库、代理资源池、字典权重库、内部培训系统等等。

Tide安全团队自建立之初持续向CNCERT、CNVD、漏洞盒子、补天、各大SRC等漏洞提交平台提交漏洞，在漏洞盒子先后组建的两支漏洞挖掘团队在全国300多个安全团队中均拥有排名前十的成绩。团队成员在FreeBuf、安全客、安全脉搏、t00ls、简书、CSDN、51CTO、CnBlogs等网站开设专栏或博客，研究安全技术、分享经验技能。

对安全感兴趣的小伙伴可以关注Tide安全团队Wiki：[http://paper.TideSec.com](http://paper.TideSec.com) 或团队公众号。

<div align=center><img src=images/ewm.png width=30% ></div> 

