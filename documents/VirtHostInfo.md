# VirtHostInfo

## 内置类
### Capabilities
#### 变量
- host: 主机信息字典
  - uuid: 主机的UUID
  - cpuinfo: CPU信息
    - arch: 架构
    - model: CPU型号
    - vendor: 厂商?
    - microcode: 微码信息
    - counter: 频率
    - topology: 技术信息
      - sockets: 插槽数?
      - dies?
      - cores: 核心数
      - threads: 每个核心的线程数
    - feature: 支持的功能列表
    - pages: 支持的页大小列表
  - cpu_cells: 单个CPU信息（key = CPUID）
    - memory: CPU连接的内存大小
    - pages: 内存页的分配信息
    - cpu: CPU逻辑核心列表
      - id: CPU逻辑核心ID
      - socket_id: 核心的插槽ID
      - core_id: 对应物理核心的ID
      - siblings: 同物理核心的逻辑核心ID列表（逗号分割）
  - cpu_caches: CPU缓存列表
    - id: 核心ID?
    - level: 缓存等级
    - type
    - size: 缓存大小
    - unit: 大小单位
    - cpus: 对应的CPU逻辑核心
- guests: 虚拟机架构信息字典
  - _archtype_
    - os_type
    - wordsize: 位数 （32 / 64）
    - emulator: qemu文件路径
    - machine: 机器列表(?)
      - { "maxCpus", "name" } (带有 canonical 的是指明默认值)
    - domain: 不同虚拟机的可执行文件路径 (区分qemu/kvm/.....)（空代表不区分）
#### 方法
- _getHostInfo: 内部XML2Dict函数
- _getGuestsInfo: 内部XML2Dict函数
- getDict: 返回字典格式的对象
- \_\_str\_\_: 返回json字符串

## 变量
- `_capabilities_`: 内部存储变量
- `_domainCapabilities_`: 内部存储变量
- `_libvirtVersion_`: 内部存储变量
- `_sysinfo_`: 内部存储变量
- `_url_`: 内部存储变量
- `_type_`: 内部存储变量
- `_vcpus_`: 内部存储变量
- `_totalMemory_`: 内部存储变量
- `_qemuVersion_`: 内部存储变量


### @property 函数
- getCapabilities: 返回主机技术支持信息
- getDomainCapabilities: 返回虚拟机技术支持信息
- getLibvirtVersion: 返回libvirt的版本
- getSysinfo: 返回系统消息
- getUrl: 返回当前连接的Url
- getType: 返回当前的虚拟化技术
- getVcpus: 返回CPU个数
- getTotalMemory: 返回总内存数（KiB）
- getQemuVersion: 返回虚拟化技术的版本


## 方法
- _getDomainCapabilities: 内部获取虚拟机技术支持信息方法
- _getSysinfo: 内部获取系统消息方法
- _reflush_capabilities: 内部刷新方法
- _reflush_domainCapabilities: 内部刷新方法
- _reflush_libvirtVersion: 内部刷新方法
- _reflush_sysinfo: 内部刷新方法
- _reflush_url: 内部刷新方法
- _reflush_type: 内部刷新方法
- _reflush_vcpus: 内部刷新方法
- _reflush_totalMemory: 内部刷新方法
- _reflush_qemuVersion: 内部刷新方法
- reflushInfo: 刷新信息方法
  - key: 刷新指定的信息（对应变量）（默认None，刷新所有）
- get: 获取信息方法
  - key: 获取指定的信息（对应变量）（默认None，返回字典）
- \_\_str\_\_: 返回Json字符串
