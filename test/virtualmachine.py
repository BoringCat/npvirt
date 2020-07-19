# raise Exception('Reject Import!')

import os
import utils
import docs
from collections import defaultdict
import xml.etree.ElementTree as ET
import copy

LANG = os.environ.get('LANG', 'en_US.UTF-8').split('.')[0]

__all__ = ['VirtualMachine']

@utils.addDoc(docs.VirtualMachine)
class VirtualMachine():
# counts
    _count_features_hyperv = ET.fromstring(
        '<hyperv><relaxed state="on"/><vapic state="on"/><spinlocks state="on" retries="8191"/></hyperv>'
    )
    _count_clock = ET.fromstring(
        '''<clock offset="utc"><timer name="rtc" tickpolicy="catchup"/><timer name="pit" tickpolicy="delay"/>
        <timer name="hpet" present="no"/></clock>'''
    )
    _count_clock_hyperv = ET.Element('timer',name="hypervclock",present="yes")
# classes
    class _RAW():
        '''存储原始的第一级XML对象

        用 for + setattr 生成的，里面有什么我也不知道'''
    class OS():
        _count_bootmenu = ET.Element('bootmenu',enable="yes")
        def __init__(self, os):
            self._xmlobj_ = os
            self._load_dkb()
        def _load_dkb(self):
            k = self._xmlobj_.find('kernel')
            i = self._xmlobj_.find('initrd')
            m = self._xmlobj_.find('mdline')
            if k != None or i != None or m != None:
                self._dkb = True
                if k == None: self._xmlobj_.append(ET.Element('kernel'))
                if i == None: self._xmlobj_.append(ET.Element('initrd'))
                if m == None: self._xmlobj_.append(ET.Element('mdline'))
        @property
        def direct_kernel_boot(self): return self._dkb
        @direct_kernel_boot.setter
        def direct_kernel_boot(self, value):
            if type(value) != bool:
                raise TypeError('direct_kernel_boot need "bool" but not "%s"'% utils.getClassName(value))
            self._dkb = value
            if value:
                self._xmlobj_.append(ET.Element('kernel'))
                self._xmlobj_.append(ET.Element('initrd'))
                self._xmlobj_.append(ET.Element('mdline'))
            else:
                self._xmlobj_.remove(self._xmlobj_.find('kernel'))
                self._xmlobj_.remove(self._xmlobj_.find('initrd'))
                self._xmlobj_.remove(self._xmlobj_.find('mdline'))
        @direct_kernel_boot.deleter
        def direct_kernel_boot(self):
            self._dkb = False
            if self._xmlobj_.find('kernel') != None:
                self._xmlobj_.remove(self._xmlobj_.find('kernel'))
            if self._xmlobj_.find('initrd') != None:
                self._xmlobj_.remove(self._xmlobj_.find('initrd'))
            if self._xmlobj_.find('mdline') != None:
                self._xmlobj_.remove(self._xmlobj_.find('mdline'))
        @property
        def arch(self): return self._xmlobj_.find('type').get('arch',None)
        @arch.setter
        def arch(self, value): self._xmlobj_.find('type').set('arch', value)
        @property
        def machine(self): return self._xmlobj_.find('type').get('machine',None)
        @machine.setter
        def machine(self, value): self._xmlobj_.find('type').set('machine', value)
        @property
        def type(self): return self._xmlobj_.find('type').text
        @type.setter
        def type(self, value): self._xmlobj_.find('type').text = value
        @property
        def bootmenu(self): return self._xmlobj_.find('bootmenu') != None
        @bootmenu.setter
        def bootmenu(self, value):
            if self._dkb:
                raise ValueError('BootMenu not supported in direct kernel boot')
            if type(value) != bool:
                raise TypeError('bootmenu need "bool" but not "%s"'% utils.getClassName(value))
            if value:
                if self._xmlobj_.find('bootmenu') == None:
                    return
                self._xmlobj_.append(_count_bootmenu)
            else:
                if self._xmlobj_.find('bootmenu') != None:
                    return
                self._xmlobj_.remove(_count_bootmenu)
        @bootmenu.deleter
        def bootmenu(self):
            if self._xmlobj_.find('bootmenu') != None:
                return
            self._xmlobj_.remove(_count_bootmenu)
        @property
        def kernel(self):
            if not self._dkb:
                raise ValueError('kernel needed direct_kernel_boot = True')
            return self._xmlobj_.find('kernel').text
        @kernel.setter
        def kernel(self, value):
            if not self._dkb:
                raise ValueError('initrd needed direct_kernel_boot = True')
            self._xmlobj_.find('kernel').text = value
        @kernel.deleter
        def kernel(self):
            if not self._dkb:
                raise ValueError('initrd needed direct_kernel_boot = True')
            self._xmlobj_.find('kernel').text = ''
        @property
        def initrd(self):
            if not self._dkb:
                raise ValueError('initrd needed direct_kernel_boot = True')
            return self._xmlobj_.find('initrd').text
        @initrd.setter
        def initrd(self, value):
            if not self._dkb:
                raise ValueError('initrd needed direct_kernel_boot = True')
            self._xmlobj_.find('initrd').text = value
        @initrd.deleter
        def initrd(self):
            if not self._dkb:
                raise ValueError('initrd needed direct_kernel_boot = True')
            self._xmlobj_.find('initrd').text = ''
        @property
        def cmdline(self):
            if not self._dkb:
                raise ValueError('cmdline needed direct_kernel_boot = True')
            return self._xmlobj_.find('cmdline').text
        @cmdline.setter
        def cmdline(self, value):
            if not self._dkb:
                raise ValueError('initrd needed direct_kernel_boot = True')
            self._xmlobj_.find('cmdline').text = value
        @cmdline.deleter
        def mdline(self):
            if not self._dkb:
                raise ValueError('initrd needed direct_kernel_boot = True')
            self._xmlobj_.find('mdline').text = ''
    class Features():
        def __init__(self, features):
            self._xmlobj_ = features
        def __iter__(self):
            self._iter_i_ = 0
            return self
        def __getitem__(self, index):
            return self._xmlobj_[index]
        def __next__(self):
            if self._iter_i_<len(self._xmlobj_):
                res = self._xmlobj_[self._iter_i_]
                self._iter_i_ += 1
                return res
            else:
                del self._iter_i_
                raise StopIteration
        def __contains__(self, feature):
            return self._xmlobj_.find(feature) != None

        def appendET(self, ET):
            obj = self._xmlobj_.find(ET.tag)
            if obj != None:
                return False
            self._xmlobj_.append(ET)
            return True
            
        def append(self, feature, **attrib):
            obj = self._xmlobj_.find(feature)
            if obj != None:
                return False
            self._xmlobj_.append(ET.Element(feature,attrib))
            return True

        def get(self, feature):
            return self._xmlobj_.find(feature)

        def pop(self, index):
            obj = self._xmlobj_[index]
            self._xmlobj_.remove(obj)
            return obj

        def index(self, feature):
            obj = self._xmlobj_.find(feature)
            if obj == None:
                return -1
            return tuple(self._xmlobj_).index(obj)

        def listTags(self):
            return list(map(lambda x:x.tag, self._xmlobj_))

        def listWithAttrib(self):
            l = {}
            for feature in self._xmlobj_:
                if len(feature.attrib):
                    l[feature.tag] = feature.attrib.copy()
                    if feature.text != None:
                        l[feature.tag]['text'] = feature.text
                else:
                    l[feature.tag] = feature.text
            return l
    class CPU():
        class Features():
            def __init__(self, cpu):
                self._xmlobj_ = cpu
            def __iter__(self):
                self._iter_i_ = 0
                self._iter_list_ = self._xmlobj_.findall('feature')
                self._iter_max_ = len(self._iter_list_)
                return self
            def __getitem__(self, name):
                return self._xmlobj_.find('./feature[@name="%s"]' % name)
            def __next__(self):
                if self._iter_i_ < self._iter_max_:
                    res = self._iter_list_[self._iter_i_]
                    self._iter_i_ += 1
                    return res
                else:
                    del self._iter_i_
                    del self._iter_list_
                    del self._iter_max_
                    raise StopIteration
            def __contains__(self, name):
                return self._xmlobj_.find('./feature[@name="%s"]' % name) != None

            def append(self, name, policy):
                if policy not in ['force','require','optional','disable','forbid']:
                    raise ValueError('policy only support [force,require,optional,disable,forbid] but not "%s"' % value)
                obj = self._xmlobj_.find('./feature[@name="%s"]' % name)
                if obj != None:
                    return False
                self._xmlobj_.append(ET.Element('feature',policy=policy,name=name))
                return True

            def motify(self, name, policy):
                if policy not in ['force','require','optional','disable','forbid']:
                    raise ValueError('policy only support [force,require,optional,disable,forbid] but not "%s"' % value)
                obj = self._xmlobj_.find('./feature[@name="%s"]' % name)
                if obj == None:
                    return False
                obj.set('policy',policy)
                return True

            def get(self, feature):
                return self._xmlobj_.find('./feature[@name="%s"]' % name)

            def popitem(self, name):
                obj = self._xmlobj_.find('./feature[@name="%s"]' % name)
                self._xmlobj_.remove(obj)
                return obj

            def listNamePolicy(self):
                return dict(map(lambda x:(x.get('name'), x.get('policy')), self._xmlobj_.findall('feature')))

        def __init__(self, cpu):
            self._xmlobj_ = cpu
            self.features = self.Features(cpu)
        @property
        def mode(self): return self._xmlobj_.get('mode',None)
        @mode.setter
        def mode(self, value):
            if value not in ['custom','host-model','host-passthrough']:
                raise ValueError('mode only support [custom,host-model,host-passthrough] but not "%s"' % value)
            self._xmlobj_.set('mode', str(value))
        @property
        def check(self): return self._xmlobj_.get('check',None)
        @check.setter
        def check(self, value):
            if value not in ['none','partial','full']:
                raise ValueError('check only support [none,partial,full] but not "%s"' % value)
            self._xmlobj_.set('check', str(value))
        @property
        def sockets(self):
            if self._xmlobj_.find('topology') != None:
                return int(self._xmlobj_.find('topology').get('sockets','0'))
        @sockets.setter
        def sockets(self, value):
            if type(value) != int:
                raise TypeError('sockets need "int" but not "%s"' % utils.getClassName(value))
            if self._xmlobj_.find('topology') != None:
                self._xmlobj_.find('topology').set('sockets', str(value))
            else:
                self._xmlobj_.append(ET.Element('togology',sockets=str(value)))
        @sockets.deleter
        def sockets(self):
            obj = self._xmlobj_.find('topology')
            if obj != None:
                obj.attrib.pop('sockets',None)
            if len(obj.attrib) == 0:
                self._xmlobj_.remove(obj)
        @property
        def cores(self):
            if self._xmlobj_.find('topology') != None:
                return int(self._xmlobj_.find('topology').get('cores','0'))
        @cores.setter
        def cores(self, value):
            if type(value) != int:
                raise TypeError('cores need "int" but not "%s"' % utils.getClassName(value))
            if self._xmlobj_.find('topology') != None:
                self._xmlobj_.find('topology').set('cores', str(value))
            else:
                self._xmlobj_.append(ET.Element('togology',cores=str(value)))
        @cores.deleter
        def cores(self):
            obj = self._xmlobj_.find('topology')
            if obj != None:
                obj.attrib.pop('cores',None)
            if len(obj.attrib) == 0:
                self._xmlobj_.remove(obj)
        @property
        def threads(self):
            if self._xmlobj_.find('topology') != None:
                return int(self._xmlobj_.find('topology').get('threads','0'))
        @threads.setter
        def threads(self, value):
            if type(value) != int:
                raise TypeError('threads need "int" but not "%s"' % utils.getClassName(value))
            if self._xmlobj_.find('topology') != None:
                self._xmlobj_.find('topology').set('threads', str(value))
            else:
                self._xmlobj_.append(ET.Element('togology',threads=str(value)))
        @threads.deleter
        def threads(self):
            obj = self._xmlobj_.find('topology')
            if obj != None:
                obj.attrib.pop('threads',None)
            if len(obj.attrib) == 0:
                self._xmlobj_.remove(obj)
    class PM():
        def __init__(self, pm):
            self._xmlobj_ = pm
        @property
        def suspend_to_mem(self): return self._xmlobj_.find('suspend-to-mem').get('enable') == 'yes'
        @suspend_to_mem.setter
        def suspend_to_mem(self, value):
            if type(value) != bool:
                raise ValueError('suspend-to-mem need "bool" but not "%s"' % utils.getClassName(value))
            self._xmlobj_.find('suspend-to-mem').set('enable', "yes" if value else "no")
        @suspend_to_mem.deleter
        def suspend_to_mem(self): self._xmlobj_.find('suspend-to-mem').set('enable', "no")
        @property
        def suspend_to_disk(self): return self._xmlobj_.find('suspend-to-disk').get('enable') == 'yes'
        @suspend_to_disk.setter
        def suspend_to_disk(self, value):
            if type(value) != bool:
                raise ValueError('suspend-to-disk need "bool" but not "%s"' % utils.getClassName(value))
            self._xmlobj_.find('suspend-to-disk').set('enable', "yes" if value else "no")
        @suspend_to_disk.deleter
        def suspend_to_disk(self): self._xmlobj_.find('suspend-to-disk').set('enable', "no")
    class Devices():
        pass
# variable
    raw = _RAW()
# private function
    def __init__(self, xml = None):
        if xml == None:
            self.__init_toxml__()
        else:
            self.__init_fromxml__(xml)
        self._register_values()
        self._register_raws()

    def __init_toxml__(self):
        self._xmlobj_ = ET.Element('domain')
        for l1id in [
            'name','uuid','memory','currentMemory','vcpu','os','features',
            'cpu','on_poweroff','on_reboot','on_crash','pm','devices'
        ]:
            self._xmlobj_.append(
                ET.Element(l1id),
            )
        self._xmlobj_.find('uuid').text = utils.uuidgen()
        self._xmlobj_.find('memory').text = '0'
        self._xmlobj_.find('memory').set('unit','KiB')
        self._xmlobj_.find('currentMemory').text = '0'
        self._xmlobj_.find('currentMemory').set('unit','KiB')
        self._xmlobj_.find('vcpu').set('placement','static')
        self._xmlobj_.find('cpu').set('mode','')
        self._xmlobj_.find('cpu').set('check','')
        self._xmlobj_.find('on_poweroff').text = 'destroy'
        self._xmlobj_.find('on_reboot').text = 'restart'
        self._xmlobj_.find('on_crash').text = 'destroy'
        self._xmlobj_.find('pm').append(ET.Element('suspend-to-mem',enable='no'))
        self._xmlobj_.find('pm').append(ET.Element('suspend-to-disk',enable='no'))
        self._xmlobj_.find('os').append(ET.Element('type',arch='',machine=''))
        self._xmlobj_.find('features').append(ET.Element('acpi'))
        self._xmlobj_.find('features').append(ET.Element('apic'))
        self._xmlobj_.find('features').append(ET.Element('pae'))
        self._xmlobj_.find('features').append(ET.Element('vmport',state='off'))
        self._xmlobj_.append(self._count_clock)

    def __init_fromxml__(self, xml):
        self._xmlobj_ = ET.fromstring(''.join(map(str.strip,xml.splitlines())))
        f_hyperv = self._xmlobj_.find('./features/hyperv')
        c_hyperv = self._xmlobj_.find('./clock/timer[@name="hypervclock"]')
        if f_hyperv:
            self._count_features_hyperv = f_hyperv
        if c_hyperv:
            self._count_clock_hyperv = c_hyperv

    def _register_raws(self):
        for n in self._xmlobj_:
            setattr(self.raw,n.tag,n)

    def _register_values(self):
        self.pm = self.PM(self._xmlobj_.find('pm'))
        self.features = self.Features(self._xmlobj_.find('features'))
        self.devices = self._xmlobj_.find('devices')
        self.os = self.OS(self._xmlobj_.find('os'))
        self.cpu = self.CPU(self._xmlobj_.find('cpu'))

    def _value_check(self):
        if self._xmlobj_.find('currentMemory').text in [None, '', "0"]:
            self._xmlobj_.find('currentMemory').text = self._xmlobj_.find('memory').text
        if self._xmlobj_.find('uuid').text in [None, '']:
            self._xmlobj_.find('uuid').text = utils.uuidgen()
        if self._xmlobj_.find('vcpu').text in [None, '']:
            self._xmlobj_.find('vcpu').text = '1'
        vcpu_current =  self._xmlobj_.find('vcpu').get('current', None)
        if vcpu_current != None:
            if not vcpu_current:
                self._xmlobj_.find('vcpu').attrib.pop('current')
            if int(vcpu_current) > int(self._xmlobj_.find('vcpu').text):
                self._xmlobj_.find('vcpu').attrib.pop('current')

    def __str__(self):
        self._value_check()
        return utils.prettyXML(copy.copy(self._xmlobj_))
# property
  # name
    @property
    def name(self): return self._xmlobj_.find('name').text
    @name.setter
    def name(self,name): self._xmlobj_.find('name').text = name
  # uuid
    @property
    def uuid(self): return self._xmlobj_.find('uuid').text
    @uuid.setter
    def uuid(self,uuid): self._xmlobj_.find('uuid').text = uuid
  # Memory
    @property
    def maxMemory(self): return int(self._xmlobj_.find('memory').text)
    @maxMemory.setter
    def maxMemory(self,memory): self._xmlobj_.find('memory').text = str(utils.formatHumanReadMemory(memory,'K'))
    
    @property
    def minMemory(self): return self._xmlobj_.find('currentMemory').text
    @minMemory.setter
    def minMemory(self,memory): self._xmlobj_.find('currentMemory').text = str(utils.formatHumanReadMemory(memory,'K'))
    @minMemory.deleter
    def minMemory(self): self._xmlobj_.find('currentMemory').text = ''
  # Vcpu
    @property
    def maxVCPU(self): return int(self._xmlobj_.find('vcpu').text)
    @maxVCPU.setter
    def maxVCPU(self,cpus): self._xmlobj_.find('vcpu').text = str(cpus)
    
    @property
    def minVCPU(self): return self._xmlobj_.find('vcpu').get('current', None)
    @minVCPU.setter
    def minVCPU(self,cpus): self._xmlobj_.find('vcpu').set('current', str(cpus))
    @minVCPU.deleter
    def minVCPU(self): self._xmlobj_.find('vcpu').attrib.pop('current')
  # Actions
    @property
    def on_poweroff(self): return self._xmlobj_.find('on_poweroff').text
    @on_poweroff.setter
    def on_poweroff(self, value):
        if value not in ['destroy','restart','preserve','rename-restart']:
            raise ValueError('UnSupport action "%s". on_poweroff allow [destroy,restart,preserve,rename-restart]' % value)
        self._xmlobj_.find('on_poweroff').text = value
    @on_poweroff.deleter
    def on_poweroff(self): self._xmlobj_.find('on_poweroff').text = 'destroy'

    @property
    def on_reboot(self): return self._xmlobj_.find('on_reboot').text
    @on_reboot.setter
    def on_reboot(self, value):
        if value not in ['destroy','restart','preserve','rename-restart']:
            raise ValueError('UnSupport action "%s". on_reboot allow [destroy,restart,preserve,rename-restart]' % value)
        self._xmlobj_.find('on_reboot').text = value
    @on_reboot.deleter
    def on_reboot(self): self._xmlobj_.find('on_reboot').text = 'restart'

    @property
    def on_crash(self): return self._xmlobj_.find('on_crash').text
    @on_crash.setter
    def on_crash(self, value):
        if value not in ['destroy','restart','preserve','rename-restart','coredump-destroy','coredump-restart']:
            raise ValueError('UnSupport action "%s". on_crash allow [destroy,restart,preserve,rename-restart,coredump-destroy,coredump-restart]' % value)
        self._xmlobj_.find('on_crash').text = value
    @on_crash.deleter
    def on_crash(self): self._xmlobj_.find('on_crash').text = 'destroy'

    @property
    def on_lockfailure(self):
        obj = self._xmlobj_.find('on_lockfailure')
        return obj.text if obj else None
    @on_lockfailure.setter
    def on_lockfailure(self, value):
        if value not in ['poweroff','restart','pause','ignore']:
            raise ValueError('UnSupport action "%s". on_lockfailure allow [poweroff,restart,pause,ignore]' % value)
        obj = self._xmlobj_.find('on_lockfailure')
        if not obj:
            obj = ET.Element('on_lockfailure')
            self._xmlobj_.append(obj)
        obj.text = value
    @on_lockfailure.deleter
    def on_lockfailure(self): self._xmlobj_.remove(self._xmlobj_.find('on_lockfailure'))

# functions
    @utils.addDoc(docs.VirtualMachine_UseWindows)
    def UseWindows(self, status):
        if type(status) != bool:
            raise TypeError('status need "bool" but not "%s"' % utils.getClassName(enable))
        if status:
            if 'hyperv' not in self.features:
                self.features.appendET(self._count_features_hyperv)
            self._xmlobj_.find('clock').set('offset','localtime')
            c_hyperv = self._xmlobj_.find('./clock/timer[@name="hypervclock"]')
            if c_hyperv == None:
                self._xmlobj_.find('clock').append(self._count_clock_hyperv)
        else:
            if 'hyperv' in self.features:
                self._count_features_hyperv = self.features.get('hyperv')
                self.features.pop(self._count_features_hyperv)
            self._xmlobj_.find('clock').set('offset','utc')
            c_hyperv = self._xmlobj_.find('./clock/timer[@name="hypervclock"]')
            if c_hyperv != None:
                self._count_clock_hyperv = c_hyperv
                self._xmlobj_.find('clock').remove(c_hyperv)