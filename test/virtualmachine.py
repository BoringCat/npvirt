raise Exception('Reject Import!')

class VM_os():
    type_ = ''
    arch = ''
    machine = ''
    bootlist = []
    bootmenu = {'enable': False, 'timeout': 5000}
    direct_kernel_boot = False
    kernel = ''
    initrd = ''
    cmdline = ''

class VM_vcpu():
    placement = 'static'
    current = 0
    value = 0

class VM_cpu():
    mode = 'static'
    check = "none"
    sockets = None
    cores = None
    threads = None

class VM_Features_Hyperv():
    relaxed = True
    vapic = True
    spinlocks = {'state': True, 'retries': None}
    vpindex = None
    runtime = None
    synic = None
    stimer = {'state': None, 'direct': None}
    reset = None
    vendor_id = {'state': None, 'value': None}
    frequencies = None
    reenlightenment = None
    tlbflush = None
    ipi = None
    evmcs = None

class VM_Device_Disks():
    pass

class VM_Device_Filesystems():
    pass

class VM_Device_Controllers():
    pass

class VM_Device_Hostdevs():
    pass

class VM_Device_Redirdevs():
    pass

class VM_Device_Smartcards():
    pass

class VM_Device_Interfaces():
    pass

class VM_Device_Inputs():
    pass

class VM_Device_Graphicses():
    pass

class VM_Device_Video():
    pass

class VM_Device_Parallels():
    pass

class VM_Device_Serials():
    pass

class VM_Device_Consoles():
    pass

class VM_Device_Channels():
    pass

class VM_Device_Sounds():
    pass

class VM_Device_Watchdog():
    pass

class VM_Device_Rngs():
    pass

class VM_Device_Tpm():
    pass

class VM_Device_Iommu():
    pass



class VM_Devices():
    emulator = ''
    disks = VM_Device_Disks()
    filesystems = VM_Device_Filesystems()
    controllers = VM_Device_Controllers()
    hostdevs = VM_Device_Hostdevs()
    redirdevs = VM_Device_Redirdevs()
    smartcards = VM_Device_Smartcards()
    interfaces = VM_Device_Interfaces()
    inputs = VM_Device_Inputs()
    graphicses = VM_Device_Graphicses()
    video = VM_Device_Video()
    parallels = VM_Device_Parallels()
    serials = VM_Device_Serials()
    consoles = VM_Device_Consoles()
    channels = VM_Device_Channels()
    sounds = VM_Device_Sounds()
    watchdog = VM_Device_Watchdog()
    rngs = VM_Device_Rngs()
    tpm = VM_Device_Tpm()
    iommu = VM_Device_Iommu()

class VirtualMachine():
    name = ''
    uuid = ''
    title = ''
    description = ''
    os = VM_os()
    vcpu = VM_vcpu()
    memory = 0
    currentMemory = 0
    cpu = VM_cpu()
    features = {'acpi': True, 'apic': True , 'pae': True, 'hyperv': VM_Features_Hyperv()}
    clock = '''  <clock offset='{clock_offset}'>
    <timer name='rtc' tickpolicy='catchup'/>
    <timer name='pit' tickpolicy='delay'/>
    <timer name="hpet" present="no"/>
    <timer name="hypervclock" present="yes"/><!-- Windows Only -->
  </clock>'''
    pm = {'suspend-to-mem': False, 'suspend-to-disk': False}
    on_poweroff = 'destroy'
    on_reboot = 'restart'
    on_crash = 'destroy'
    devices = VM_Devices()