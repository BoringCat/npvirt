VirtualMachine_UseWindows = '''
VirtualMachine.UseWindows (安装适用于Windows的虚拟机配置)

仅修改 `features.hyperv` 和 `clock`

当设定为True时
- 检测并增加 features.hyperv 配置，来源于默认或输入的xml。
- 修改 clock 的 offset 属性为 'localtime'
- 检测并修改 clock.timer[@name="hypervclock"] 配置，来源于默认或输入的xml。

当设定为False时
- 检测并删除 features.hyperv 配置，并备份配置到常量中
- 修改 clock 的 offset 属性为 'utc'
- 检测并删除 clock.timer[@name="hypervclock"] 配置，并备份配置到常量中
'''

VirtualMachine = '''
VirtualMachine Libvirt VM 类

通过libvirt的dom.xml创建方法:  
- VirtualMachine(xml)

新建方法:  
- VirtualMachine()

Raw属性:  
VirtualMachine.raw

支持libvirt属性:
- name
- uuid
- title
- description
- vcpu
- memory
- currentMemory
- cpu
 - topology
 - feature
- os
 - bootmenu
 - direct kernel boot
- features
- clock (仅可通过raw进行自定义)
- on_poweroff
- on_reboot
- on_crash
- on_lockfailure
- devices
'''