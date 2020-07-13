# libvirt 的 XML 文档

## 头尾
type = VirtHostInfo.domainCapabilities.domain
```xml
<domain type='kvm'>
  ...
</domain>
```

## 概况
```xml
  <name>{name}</name><!-- 名称 -->
  <uuid>{uuid}</uuid><!-- UUID -->
  <title>{title}</title><!-- 标题 -->
  <description>{description}</description><!-- 描述 -->
```

## 性能
```xml
  <vcpu placement="static" current="{minvcpus}">{maxvcpus}</vcpu>
  <memory unit="KiB">{maxmemory}</memory>
  <currentMemory unit="KiB">{minmemory}</currentMemory>
```
### CPU拓扑
```xml
  <cpu mode="{cpu_mode}" check="none">
    <topology sockets="{cpu_sockets}" cores="{cpu_cores}" threads="{cpu_threads}"/>
  </cpu>
```
### CPU默认
```xml
  <cpu mode="{cpumode}" check="none"/>
```

## 系统
arch -> `VirtHostInfo.capabilities.guests.keys()`  
machine -> `VirtHostInfo.capabilities.guests[arch].machine[?].canonical`  
type -> `VirtHostInfo.capabilities.guests[arch].os_type`  
`<boot/>`: 引导项  
`<bootmenu enable/>`: 是否启用引导菜单  
```xml
  <os>
    <type arch="{os_arch}" machine="{os_machine}">{os_type}</type>
    <boot dev="fd"/>
    <boot dev="hd"/>
    <boot dev="cdrom"/>
    <boot dev="network"/>
    <bootmenu enable="yes"/>
  </os>
```
### 直接内核引导
```xml
  <os>
    <type>hvm</type>
    <kernel>{os_kernel}</kernel>
    <initrd>{os_initrd}</initrd>
    <cmdline>{os_cmdline}</cmdline>
  </os>
```

## 功能
### 默认
```xml
  <features>
    <acpi/>
    <apic/>
    <pae/>
  </features>
```

### hyperv
windows用  
（改善Windows系统的性能）
| 选项 | 描述 | 支持的值<br>默认state | 版本要求 |
| :------ | :---------- | :---- | :---- |
| relaxed | 放宽对计时器的限制 | on, off | 1.0.0 (QEMU 2.0) |
| vapic | 启用虚拟APIC | on, off | 1.1.0 (QEMU 2.0) |
| spinlocks | 启用CPU自旋锁 | on, off<br>retries(重试次数?) >= 4095 | 1.1.0 (QEMU 2.0) |
| vpindex | 虚拟处理器索引?<br>Virtual processor index | on, off | 1.3.3 (QEMU 2.5) |
| runtime | CPU运行时?<br>Processor time spent on running guest code and on behalf of guest code | on, off | 1.3.3 (QEMU 2.5) |
| synic | 启用综合中断控制器?<br>Enable Synthetic Interrupt Controller (SynIC) | on, off | 1.3.3 (QEMU 2.6) |
| stimer | 启用SynIC计数器，支持直通模式?<br>Enable SynIC timers, optionally with Direct Mode support | on, off<br>direct - on,off | 1.3.3 (QEMU 2.6)<br>direct mode 5.7.0 (QEMU 4.1) |
| reset | Enable hypervisor reset | on, off | 1.3.3 (QEMU 2.5) |
| vendor_id | 设置虚拟化供应商ID?<br>Set hypervisor vendor id | on, off<br>value - 字符串, 最大12字符 | 1.3.3 (QEMU 2.5) |
| frequencies | 暴露MSR频率 | on, off | 4.7.0 (QEMU 2.12) |
| reenlightenment | Enable re-enlightenment notification on migration | on, off | 4.7.0 (QEMU 3.0) |
| tlbflush | 启用PV TLB刷新支持?<br>Enable PV TLB flush support | on, off | 4.7.0 (QEMU 3.0) |
| ipi | 启用PV IPI支持 | on, off | 4.10.0 (QEMU 3.1) |
| evmcs | Enable Enlightened VMCS | on, off | 4.10.0 (QEMU 3.1) |

## 时钟
`offset`: `utc` 或 `localtime` ()
```xml
  <clock offset='{clock_offset}'>
    <timer name='rtc' tickpolicy='catchup'/>
    <timer name='pit' tickpolicy='delay'/>
    <timer name="hpet" present="no"/>
    <timer name="hypervclock" present="yes"/><!-- Windows Only -->
  </clock>
```

## 设备
### 可执行文件路径
```xml
    <emulator>{VirtHostInfo.capabilities.guests[arch].emulator}</emulator>
```

### 信道
#### qemu-qa
```xml
    <channel type="unix">
      <target type="virtio" name="org.qemu.guest_agent.0"/>
      <address type="virtio-serial" controller="0" bus="0" port="2"/>
    </channel>
```

### 磁盘
`type`:
- `file`: 文件
- `block` 块设备
- `dir`: 文件夹?
  - Version >= 0.7.5
- `network`: 来源于网络的文件
  - Version >= 0.8.7
- `volume`: LVM卷
  - Version >= 1.0.5
- `nvme`: 本机的nvme设备
  - Version >= 6.0.0

`device`: 
- `floppy`: 软盘
- `disk`: 磁盘
- `cdrom`: CD
- `lun`
```xml
    <disk type="{disk_type}" device="{disk_dev}">
    </disk>
```
#### backingStore  后备存储 / 基础磁盘
type: 与[磁盘](#磁盘)的Type一样
```xml
      <backingStore type='file'>
        <format type='qcow2'/>
        <source file='/var/lib/libvirt/images/base.qcow2'/>
      </backingStore>
```
可以无限套娃

#### driver 驱动
- `name`: QEMU 只支持 qemu
- `type`: 文件类型
  - `raw`
  - `qcow2`
- `cache`: 缓存模式
  - `default`: 默认
  - `none`: 无
  - `writethrough`: 直写 直接写入磁盘（会触发主机缓存）
  - `writeback`: 回写 缓存数据，在磁盘空闲或缓存满时写入
  - `directsync`: 垂 直 同 步  直接写入磁盘（不触发主机缓存）
  - `unsafe`: 由主机规则决定
- `error_policy`: 错误控制
  - `stop`: 停止（虚拟机? 还是 磁盘?）
  - `report`: 报错
  - ``: 忽略
  - ``: 
```xml
      <driver
        name="qemu"
        type="raw"
        cache="default"
      />
```

#### iotune IO限制
- `total_bytes_sec`  
  总吞吐量限制  
  与 `read_bytes_sec` 和 `write_bytes_sec` 互斥
- `read_bytes_sec`  
  读取吞吐量限制  
  与 `total_bytes_sec` 互斥
- `write_bytes_sec`  
  写入吞吐量限制  
  与 `total_bytes_sec` 互斥
- `total_iops_sec`  
  总IO次数限制  
  与 `read_iops_sec` 和 `write_iops_sec` 互斥
- `read_iops_sec`  
  读取IO次数限制  
  与 `total_iops_sec` 互斥
- `write_iops_sec`  
  写入IO次数限制  
  与 `total_iops_sec` 互斥
```xml
      <iotune>
        <example>...</example>
      </iotune>
```

#### 本地文件实例
`target`:
- `bus`: ide, scsi, virtio, xen, usb, sata, sd
- `dev`: IDE -> hd, virtio -> vd, other -> sd
```xml
    <disk type="file" device="disk">
      <driver name="qemu" type="qcow2"/>
      <source file="/var/lib/libvirt/images/test.qcow2"/>
      <target dev="vda" bus="virtio" />
      <serial>WDNMD</serial>
      <boot order="1"/>
    </disk>
```
ISO文件
```xml
    <disk type="file" device="cdrom">
      <driver name="qemu" type="raw"/>
      <target dev="sda" bus="sata" >
      <source file="/var/lib/libvirt/isos/archlinux-2020.07.01-x86_64.iso"/>
      <readonly/>
      <boot order="2"/>
    </disk>
```
LVM直通  
（也可用于设备直通）
```xml
    <disk type="block" device="disk">
      <driver name="qemu" type="raw" cache="none"/>
      <source dev="/dev/FedoraSlowData/VmDownload"/>
      <target dev="vdb" bus="virtio"/>
    </disk>
```

#### 远程文件实例
iscsi
```xml
    <disk type='network' device='disk'>
      <driver name='qemu' type='raw'/>
      <source protocol='iscsi' name='iqn.2013-07.com.example:iscsi-nopool/1'>
        <host name='example.com' port='3260'/>
        <auth username='myuser'>
          <secret type='iscsi' usage='libvirtiscsi'/>
        </auth>
        <initiator>
          <iqn name='iqn.2013-07.com.example:client'/>
        </initiator>
      </source>
      <target dev='sdb' bus='scsi'/>
    </disk>
```
远程ISO镜像（还有这操作？？？）
```xml
    <disk type='network' device='cdrom'>
      <driver name='qemu' type='raw'/>
      <source protocol="https" name="url_path">
        <host name="hostname" port="443"/>
      </source>
      <target dev='sda' bus='sata' tray='open'/>
      <readonly/>
    </disk>
```
