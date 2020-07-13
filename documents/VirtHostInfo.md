# VirtHostInfo

## 内置类
### Capabilities
#### 变量
- `host`: 主机信息字典
  - `uuid`: 主机的UUID
  - `cpuinfo`: CPU信息
    - `arch`: 架构
    - `model`: CPU型号
    - `vendor`: 厂商?
    - `microcode`: 微码信息
    - `counter`: 频率
    - `topology`: 技术信息
      - `sockets`: 插槽数?
      - `dies`?
      - `cores`: 核心数
      - `threads`: 每个核心的线程数
    - `feature`: 支持的功能列表
    - `pages`: 支持的页大小列表
  - `cpu_cells`: 单个CPU信息（key = CPUID）
    - `memory`: CPU连接的内存大小
    - `pages`: 内存页的分配信息
    - `cpu`: CPU逻辑核心列表
      - `id`: CPU逻辑核心ID
      - `socket_id`: 核心的插槽ID
      - `core_id`: 对应物理核心的ID
      - `siblings`: 同物理核心的逻辑核心ID列表（逗号分割）
  - `cpu_caches`: CPU缓存列表
    - `id`: 核心ID?
    - `level`: 缓存等级
    - `type`
    - `size`: 缓存大小
    - `unit`: 大小单位
    - `cpus`: 对应的CPU逻辑核心
- `guests`: 虚拟机架构信息字典
  - _`archtype`_
    - `os_type`
    - `wordsize`: 位数 （32 / 64）
    - `emulator`: 虚拟化可执行文件路径
    - `machine`: 机器列表(?)
      - { "maxCpus", "name" } (带有 canonical 的是指明默认值)
    - `domain`: 不同虚拟机的可执行文件路径  
      (区分qemu/kvm/.....)  
      （空代表不区分）  
#### 方法
- `_getHostInfo`: 内部XML2Dict函数
- `_getGuestsInfo`: 内部XML2Dict函数
- `getDict`: 返回字典格式的对象
- `__str__`: 返回json字符串

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
- `getCapabilities`: 返回主机技术支持信息  
  参见 [内置类 - Capabilities](#capabilities)
- `getDomainCapabilities`: 返回虚拟机技术支持信息
  - `path`: 默认的虚拟化可执行文件路径
  - `domain`: 默认的虚拟化技术
  - `machine`: 默认的虚拟化主机
  - `arch`: 默认的虚拟化CPU架构
  - `vcpu`: 虚拟化CPU总数限制
    - `max`: 最大值
  - `iothreads`: IO线程
    - `supported`: 是否支持
  - `cpumode`: CPU型号信息
    - `host-passthrough`: 主机直通
      - `supported`: 是否支持
    - `host-model`: 主机CPU信息/默认CPU型号
      - `model`: 技术规格?
      - `vendor`: 厂商
      - `feature` 功能列表
        - `policy`?
        - `name`: 功能名?
    - `custom-model`: 非默认CPU型号支持列表
      - `usable`: 是否能用
      - `name`: 型号名字
  - `devices`: 支持的设备信息
    - _`device_type`_: 设备类型（例：disk、video......）
      - `supported`: 是否支持
      - `items`: 设备分类列表
        - _`device_name`_: 支持的设备分类列表（例：diskDevice......）
  - `features`: 列举功能?
    - _`feature_name`_: 功能是否支持
- `getLibvirtVersion`: 返回libvirt的版本
- `getSysinfo`: 返回系统消息  
  出错时返回 String 类型的错误信息
  - `type`: 信息类型/来源?
  - `bios`: BIOS信息
    - `vendor`: 厂商
    - `version`: 版本号
    - `date`: 发布时间
    - `release`: 内部版本号?
  - `baseBoard`: 设备信息
    - `manufacturer`: 制造商
    - `product`: 型号
    - `version`: 版本号
    - `serial`: 系列号
    - `asset`: 资产信息?
    - `location`: 位置信息?
  - `chassis`: 机箱信息?
    - `manufacturer`: 制造商
    - `version`: 版本号
    - `serial`: 系列号
    - `asset`: 资产信息?
    - `sku`
  - `processor`: 处理器信息列表
    - `socket_destination`: 插槽信息
    - `type`: 类型
    - `family`: 品牌
    - `manufacturer`: 制造商
    - `signature`: 签名?
    - `version`: 版本
    - `external_clock`: 外部时钟速度
    - `max_speed`: 最大速度
    - `status`: 状态
    - `serial_number`: 序列号
    - `part_number`: 零件号
  - `memory_device`: 内存信息列表
    - `size`: 大小（Human readable）
    - `form_factor`: 外形规格
    - `locator`: 逻辑位置
    - `bank_locator`: 物理位置
    - `type`: 规格
    - `type_detail`: 详细规格
    - `speed`: 速度
    - `manufacturer`: 制造商
    - `serial_number`: 序列号
    - `part_number`: 零件号
- `getUrl`: 返回当前连接的Url
- `getType`: 返回当前的虚拟化技术
- `getVcpus`: 返回CPU个数
- `getTotalMemory`: 返回总内存数（KiB）
- `getQemuVersion`: 返回虚拟化技术的版本


## 方法
- `_getDomainCapabilities`: 内部获取虚拟机技术支持信息方法
- `_getSysinfo`: 内部获取系统消息方法
- `_reflush_capabilities`: 内部刷新方法
- `_reflush_domainCapabilities`: 内部刷新方法
- `_reflush_libvirtVersion`: 内部刷新方法
- `_reflush_sysinfo`: 内部刷新方法
- `_reflush_url`: 内部刷新方法
- `_reflush_type`: 内部刷新方法
- `_reflush_vcpus`: 内部刷新方法
- `_reflush_totalMemory`: 内部刷新方法
- `_reflush_qemuVersion`: 内部刷新方法
- `reflushInfo`: 刷新信息方法
  - `key`: 刷新指定的信息（对应变量）（默认None，刷新所有）
- `get`: 获取信息方法
  - `key`: 获取指定的信息（对应变量）（默认None，返回字典）
- `__str__`: 返回Json字符串
