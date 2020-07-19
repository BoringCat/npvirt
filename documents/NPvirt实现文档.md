# npvirt 实现文档 <!-- omit in toc --> 

- [功能实现](#功能实现)
  - [连接](#连接)
    - [TCP连接](#tcp连接)
    - [SSH + qemu连接](#ssh--qemu连接)
    - [tls连接](#tls连接)
    - [Socket连接](#socket连接)
  - [后端状态检测](#后端状态检测)
  - [获取主机信息](#获取主机信息)
    - [主机](#主机)
  - [获取虚拟机信息](#获取虚拟机信息)
  - [获取开启的虚拟机的vnc端口](#获取开启的虚拟机的vnc端口)
  - [存储池管理](#存储池管理)
    - [存储池状态](#存储池状态)
  - [网络列表](#网络列表)
- [官方文档翻译理解](#官方文档翻译理解)
  - [getMaxVcpus()](#getmaxvcpus)
  - [getInfo()](#getinfo)
  - [getVersion()](#getversion)
  - [getLibVersion()](#getlibversion)
  - [getMemoryStats(libvirt.VIR_NODE_MEMORY_STATS_ALL_CELLS)](#getmemorystatslibvirtvir_node_memory_stats_all_cells)
  - [getSysinfo()](#getsysinfo)
  - [getCPUMap()](#getcpumap)
  - [寻找虚拟机](#寻找虚拟机)
  - [虚拟机状态过滤](#虚拟机状态过滤)
  - [虚拟机操作](#虚拟机操作)
    - [hostname()](#hostname)
    - [info()](#info)
    - [isActive()](#isactive)
    - [状态](#状态)
    - [配置XML文档](#配置xml文档)

## 功能实现
### 连接
#### TCP连接
参数:
- IP
- 端口（如果不是默认）  
对应 Python 后端
```python
libvirt.open('qemu+tcp://IP+PORT/system')
```
#### SSH + qemu连接
参数:
- 用户名
- 地址+端口（默认22）（IP:port）（尽可能IPv6）  
对应 Python 后端
```python
libvirt.open('qemu+ssh://IP+PORT/system')
```
#### tls连接
参数:
- Hostname
- 端口（如果不是默认）  
对应 Python 后端
```python
libvirt.open('qemu+tls://Hostname+PORT/system')
```
#### Socket连接
参数:
- socket位置  
  （如果不是 `/run/libvirt/libvirt-sock`）  
  （格式`?socket=/path/to/socket`)  
对应 Python 后端
```python
libvirt.open('qemu:///system')
```
### 后端状态检测
isAlive() 正常返回1，不正常0  
只有在触发错误时，isAlive才会变成0（有个鬼用）
### 获取主机信息
| 信息 | 获取py |
| :-- | :---- |
| 连接 | `conn.getURI()` |
| 主机名 | `conn.getHostname()` |
| 虚拟化层 | `conn.getType()` |
| 内存 | `conn.getInfo()[1]`<br>需要四舍五入 |
| 逻辑CPU | `conn.getInfo()[2]` |
| 处理器 | dealsysinfo获取 |
| 架构 | `conn.getInfo()[0]` |

#### 主机
### 获取虚拟机信息
listAllDomains() 返回虚拟机对象

### 获取开启的虚拟机的vnc端口
```py
import xml.etree.ElementTree as ET
import libvirt
conn = libvirt.open()
dom = conn.lookupByName()
domxml = ET.fromstring(dom.XMLDesc())
[n.attrib.get('port',None) for n in domxml.find('devices').findall('graphics') if n.attrib.get('type','') == 'vnc']
```

### 存储池管理
| 功能 | 函数 |
| :-: | :-: |
| 获取AutoStart | autostart() |
| 连接 | create() |
| 断开连接 | destroy() |
| 状态 | info()<br>状态<br>总大小<br>已用大小<br>可用大小 |
| 返回卷列表 | listVolumes() |
| 返回卷对象 | listAllVolumes() |

#### 存储池状态
| 常量 | 状态 | 对应int |
| :-- | :-: | :-: |
| VIR_STORAGE_POOL_INACTIVE | 未连接 | 0 |
| VIR_STORAGE_POOL_BUILDING | 创建中 | 1 |
| VIR_STORAGE_POOL_RUNNING | 已连接 | 2 |
| VIR_STORAGE_POOL_DEGRADED | 性能下降 | 3 |
| VIR_STORAGE_POOL_INACCESSIBLE | 无法访问 | 4 |

### 网络列表
- listAllNetworks() 获取 Libvirt 的网络
- listAllInterfaces() 减去 Libvirt 的网络

## 官方文档翻译理解
### getMaxVcpus()
你系统能最大超售的CPU个数
(i7-6700HQ 4核8线程得到值 16)

### getInfo()
| Member | Description | 翻译 |
| :----- | :---------- | :-- |
| list[0] | string indicating the CPU model | CPU架构 |
| list[1] | memory size in megabytes | 系统内存大小 (Mib) |
| list[2] | the number of active CPUs | 活动CPU数 |
| list[3] | expected CPU frequency (mhz) | CPU最大频率 |
| list[4] | the number of NUMA nodes, 1 for uniform memory access | NUMA节点 |
| list[5] | number of CPU sockets per node | CPU插槽数 |
| list[6] | number of cores per socket | 每个插槽的CPU核心数 |
| list[7] | number of threads per core | 每个核心的线程数 |

### getVersion()
Qemu的版本
`1000000*major + 1000*minor + release`
```python
ver = conn.getVersion()
major = ver // 1000000
minor = (ver % 1000000) // 1000
release = (ver % 1000000 % 1000)
print('Version: %d.%d.%d' % (major, minor, release))
```

### getLibVersion()
libvirt的版本
`1000000*major + 1000*minor + release`
```python
ver = conn.getVersion()
major = ver // 1000000
minor = (ver % 1000000) // 1000
release = (ver % 1000000 % 1000)
print('Version: %d.%d.%d' % (major, minor, release))
```

### getMemoryStats(libvirt.VIR_NODE_MEMORY_STATS_ALL_CELLS)
获取内存状态

### getSysinfo()
返回一个XML
```xml
<sysinfo type='smbios'>
  <bios>
    <entry name='vendor'>American Megatrends Inc.</entry>
    <entry name='version'>1.05.09</entry>
    <entry name='date'>12/28/2016</entry>
    <entry name='release'>5.11</entry>
  </bios>
  <system>
    <entry name='manufacturer'>Notebook</entry>
    <entry name='product'>P65xRP</entry>
    <entry name='version'>Not Applicable</entry>
    <entry name='serial'>Not Applicable</entry>
    <entry name='uuid'>3b5bfa80-fad0-0000-0000-000000000000</entry>
    <entry name='sku'>Not Applicable</entry>
    <entry name='family'>Not Applicable</entry>
  </system>
  <baseBoard>
    <entry name='manufacturer'>Notebook</entry>
    <entry name='product'>P65xRP</entry>
    <entry name='version'>Not Applicable</entry>
    <entry name='serial'>Not Applicable</entry>
    <entry name='asset'>Tag 12345</entry>
    <entry name='location'>To Be Filled By O.E.M.</entry>
  </baseBoard>
  <chassis>
    <entry name='manufacturer'>Notebook</entry>
    <entry name='version'>N/A</entry>
    <entry name='serial'>None</entry>
    <entry name='asset'>No Asset Tag</entry>
    <entry name='sku'>To Be Filled By O.E.M.</entry>
  </chassis>
  <processor>
    <entry name='socket_destination'>U3E1</entry>
    <entry name='type'>Central Processor</entry>
    <entry name='family'>Core i7</entry>
    <entry name='manufacturer'>Intel(R) Corporation</entry>
    <entry name='signature'>Type 0, Family 6, Model 94, Stepping 3</entry>
    <entry name='version'>Intel(R) Core(TM) i7-6700HQ CPU @ 2.60GHz</entry>
    <entry name='external_clock'>100 MHz</entry>
    <entry name='max_speed'>8300 MHz</entry>
    <entry name='status'>Populated, Enabled</entry>
    <entry name='serial_number'>To Be Filled By O.E.M.</entry>
    <entry name='part_number'>To Be Filled By O.E.M.</entry>
  </processor>
  <memory_device>
    <entry name='size'>8 GB</entry>
    <entry name='form_factor'>SODIMM</entry>
    <entry name='locator'>ChannelB-DIMM0</entry>
    <entry name='bank_locator'>BANK 2</entry>
    <entry name='type'>DDR4</entry>
    <entry name='type_detail'>Synchronous</entry>
    <entry name='speed'>2400 MT/s</entry>
    <entry name='manufacturer'>Samsung</entry>
    <entry name='serial_number'>36FEC5A7</entry>
    <entry name='part_number'>M471A1K43CB1-CRC</entry>
  </memory_device>
  <memory_device>
    <entry name='size'>8 GB</entry>
    <entry name='form_factor'>SODIMM</entry>
    <entry name='locator'>ChannelB-DIMM1</entry>
    <entry name='bank_locator'>BANK 3</entry>
    <entry name='type'>DDR4</entry>
    <entry name='type_detail'>Synchronous</entry>
    <entry name='speed'>2400 MT/s</entry>
    <entry name='manufacturer'>Samsung</entry>
    <entry name='serial_number'>36FEC7BF</entry>
    <entry name='part_number'>M471A1K43CB1-CRC</entry>
  </memory_device>
</sysinfo>
```
### getCPUMap()
返回CPU地图
0: CPU个数
1: CPU在线状态
2: 在线CPU个数(?)

### 寻找虚拟机
- lookupByID()
  内部ID
- lookupByName()
  虚拟机名
  可能会用这个
- lookupByUUID()
  虚拟机UUID
  次选

### 虚拟机状态过滤
listAllDomains(?)
| 常量 | 目标 |
| :--:| :-- |
| VIR_CONNECT_LIST_DOMAINS_ACTIVE | 已经开机的 |
| VIR_CONNECT_LIST_DOMAINS_INACTIVE | 已经关机的 |
| VIR_CONNECT_LIST_DOMAINS_PERSISTENT | 持久化的(正常都是) |
| VIR_CONNECT_LIST_DOMAINS_TRANSIENT | 非持久化的(还能这样玩?) |
| VIR_CONNECT_LIST_DOMAINS_RUNNING | 正在运行的 |
| VIR_CONNECT_LIST_DOMAINS_PAUSED | 暂停的 |
| VIR_CONNECT_LIST_DOMAINS_SHUTOFF | 关闭电源的 |
| VIR_CONNECT_LIST_DOMAINS_OTHER | 其他状态(?) |
| VIR_CONNECT_LIST_DOMAINS_MANAGEDSAVE | 保存内存状态关机的 |
| VIR_CONNECT_LIST_DOMAINS_NO_MANAGEDSAVE | 没有保存内存的(无论开关) |
| VIR_CONNECT_LIST_DOMAINS_AUTOSTART | 随物理机启动的 |
| VIR_CONNECT_LIST_DOMAINS_NO_AUTOSTART | 不随物理机启动的 |
| VIR_CONNECT_LIST_DOMAINS_HAS_SNAPSHOT | 有快照的 |
| VIR_CONNECT_LIST_DOMAINS_NO_SNAPSHOT | 没有快照的 |

### 虚拟机操作
#### hostname()
获取主机名，需要 QEMU Guest Agent 

#### info()
| index | 说明 |
| :---: | :-: |
| 0 | 状态(1: 运行) (5: 关闭) |
| 1 | 最大内存分配 |
| 2 | 当前内存分配 |
| 3 | CPU个数 |
| 4 | CPU时间(?) |

#### isActive()
是否正在运行

#### 状态
| 常量 | 状态 | 对应int |
| :-: | :-- | :-----: |
| VIR_DOMAIN_NOSTATE | 没有状态 | 0 |
| VIR_DOMAIN_RUNNING | 正在运行 | 1 |
| VIR_DOMAIN_BLOCKED | 阻塞的(?) | 2 |
| VIR_DOMAIN_PAUSED | 暂停的 | 3 |
| VIR_DOMAIN_SHUTDOWN | 正在关闭的 | 4 |
| VIR_DOMAIN_SHUTOFF | 已经关闭的 | 5 |
| VIR_DOMAIN_CRASHED | 崩溃的 | 6 |
| VIR_DOMAIN_PMSUSPENDED | 保存状态的(?) | 6 |

#### 配置XML文档
XMLDesc(libvirt.VIR_DOMAIN_XML_INACTIVE)