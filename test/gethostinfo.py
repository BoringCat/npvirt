#!/usr/bin/env python3

import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
import json

class xmlIf():
    @staticmethod
    def TextStrip(xml, key, _dict):
        if xml.find(key) != None:
            _dict[key] = xml.find(key).text.strip()

    @staticmethod
    def TextStripList(xml, key):
        if xml.findall(key):
            return [n.text.strip() for n in xml.findall(key)]

    @staticmethod
    def Attrib(xml, key, _dict):
        '''向字典内添加 xml.attrib
        '''
        if xml.find(key) != None:
            _dict[key] = xml.find(key).attrib.copy()

    @staticmethod
    def AttribKey(xml, key, attrkey, _dict):
        '''向字典内添加 xml.attrib['attrkey']
        '''
        if xml.find(key) != None:
            _dict[key] = xml.find(key).attrib.get(attrkey,None)

    @staticmethod
    def AttribList(xml, key, _dict):
        '''向字典内添加 [xml.attrib]
        '''
        if xml.findall(key):
            _dict[key] = [ n.attrib.copy() for n in xml.findall(key) ]

    @staticmethod
    def AttribListKey(xml, key, attrkey, _dict):
        '''向字典内添加 [xml.attrib['attrkey']]
        '''
        if xml.findall(key):
            _dict[key] = [ n.attrib.get(attrkey) for n in xml.findall(key) ]

    @staticmethod
    def AttribSubText(xml, key, subkey, _dict):
        t = xml.find(key)
        if t != None:
            _dict[key] = t.attrib.copy()
            _dict[key][subkey] = t.text

    @staticmethod
    def AttribListSubText(xml, key, subkey, _dict):
        if xml.findall(key):
            _dict[key] = []
            for n in xml.findall(key):
                td = n.attrib.copy()
                td[subkey] = n.text.strip()
                _dict[key].append(td)

    @staticmethod
    def AttribList_KeyText2Dict(xml, key, key_attr, _dict):
        if xml.findall(key):
            # _dict[key] = {}
            for n in xml.findall(key):
                t = n.attrib.get(key_attr)
                _dict[t] = n.text.strip()

class VirtHostInfo():
    class Capabilities():
        host = None
        guests = None
        def __init__(self, capabilitiesxml):
            root = ET.fromstring(capabilitiesxml)
            self._getHostInfo(root.find('host'))
            self._getGuestsInfo(root.findall('guest'))

        def _getHostInfo(self, hostinfo):
            cpuxml = hostinfo.find('cpu')
            cpuinfo = {}
            xmlIf.TextStrip(cpuxml, 'arch', cpuinfo)
            xmlIf.TextStrip(cpuxml, 'model', cpuinfo)
            xmlIf.TextStrip(cpuxml, 'vendor', cpuinfo)
            xmlIf.Attrib(cpuxml, 'microcode', cpuinfo)
            xmlIf.Attrib(cpuxml, 'counter', cpuinfo)
            xmlIf.Attrib(cpuxml, 'topology', cpuinfo)
            xmlIf.AttribListKey(cpuxml, 'feature', 'name', cpuinfo)
            xmlIf.AttribList(cpuxml, 'pages', cpuinfo)
            topologyxml = hostinfo.find('topology')
            cpu_cells = defaultdict(dict)
            for cell in topologyxml.find('cells'):
                id = cell.attrib.get('id')
                xmlIf.AttribSubText(cell, 'memory', 'value', cpu_cells[id])
                xmlIf.AttribListSubText(cell, 'pages', 'num', cpu_cells[id])
                xmlIf.AttribList(cell.find('cpus'), 'cpu', cpu_cells[id])
            cachexml = hostinfo.find('cache')
            cpu_caches = [ bank.attrib.copy() for bank in cachexml.findall('bank') ] if cachexml != None else None
            self.host = {
                'uuid': hostinfo.find('uuid').text.strip(),
                'cpuinfo': cpuinfo,
                'cpu_cells': cpu_cells,
                'cpu_caches': cpu_caches
            }

        def _getGuestsInfo(self, guests):
            self.guests = {}
            for guest in guests:
                td = {}
                xmlIf.TextStrip(guest, 'os_type', td)
                archxml = guest.find('arch')
                archname = archxml.attrib.get('name')
                xmlIf.TextStrip(archxml,'wordsize',td)
                xmlIf.TextStrip(archxml,'emulator',td)
                xmlIf.AttribListSubText(archxml,'machine','name', td)
                td['domain'] = {}
                for domain in archxml.findall('domain'):
                    if len(domain) != 0:
                        td['domain'][domain.attrib.get('type')] = {}
                        xmlIf.TextStrip(domain, 'emulator', td[domain.attrib.get('type')])
                self.guests[archname] = td

        def getDict(self):
            return {
                'host': self.host,
                'guests': self.guests
            }

        def __str__(self):
            return json.dumps({
                'host': self.host,
                'guests': self.guests
            })

    _capabilities_ = None
    _domainCapabilities_ = None
    _libvirtVersion_ = None
    _sysinfo_ = None
    _url_ = None
    _type_ = None
    _vcpus_ = None
    _totalMemory_ = None
    _qemuVersion_ = None

    @property
    def getCapabilities(self): return self.get('capabilities')
    @property
    def getDomainCapabilities(self): return self.get('domainCapabilities')
    @property
    def getLibvirtVersion(self): return self.get('libvirtVersion')
    @property
    def getSysinfo(self): return self.get('sysinfo')
    @property
    def getUrl(self): return self.get('url')
    @property
    def getType(self): return self.get('type')
    @property
    def getVcpus(self): return self.get('vcpus')
    @property
    def getTotalMemory(self): return self.get('totalMemory')
    @property
    def getQemuVersion(self): return self.get('qemuVersion')

    def __init__(self, virtconn):
        self._conn = virtconn
        self.reflushInfo()

    def _getDomainCapabilities(self, domainCapabilitiesxml):
        self._domainCapabilities_ = {}
        root = ET.fromstring(domainCapabilitiesxml)
        xmlIf.TextStrip(root, 'path', self._domainCapabilities_)
        xmlIf.TextStrip(root, 'domain', self._domainCapabilities_)
        xmlIf.TextStrip(root, 'machine', self._domainCapabilities_)
        xmlIf.TextStrip(root, 'arch', self._domainCapabilities_)
        xmlIf.Attrib(root, 'vcpu', self._domainCapabilities_)
        xmlIf.Attrib(root, 'iothreads', self._domainCapabilities_)
        modexml = root.find('cpu').findall('mode')
        self._domainCapabilities_['cpumode'] = defaultdict(dict)
        for mode in modexml:
            if len(mode) == 0:
                attr = mode.attrib.copy()
                k = attr.pop('name')
                self._domainCapabilities_['cpumode'][k] = attr
            else:
                attr = mode.attrib.copy()
                k = attr.pop('name')
                xmlIf.AttribListSubText(mode, 'model', 'name', self._domainCapabilities_['cpumode'][k])
                if len(self._domainCapabilities_['cpumode'][k]['model']) == 1:
                    tm = self._domainCapabilities_['cpumode'][k]['model'].copy()[0]
                    self._domainCapabilities_['cpumode'][k]['model'] = tm
                if len(self._domainCapabilities_['cpumode'][k]) == 1:
                    addkey = tuple(self._domainCapabilities_['cpumode'][k].keys())[0]
                    self._domainCapabilities_['cpumode'][k+'-'+addkey] = self._domainCapabilities_['cpumode'][k][addkey].copy()
                    self._domainCapabilities_['cpumode'].pop(k)
                xmlIf.TextStrip(mode, 'vendor', self._domainCapabilities_['cpumode'][k])
                xmlIf.AttribList(mode, 'feature', self._domainCapabilities_['cpumode'][k])
        devicesxml = root.find('devices')
        self._domainCapabilities_['devices'] = {}
        for device in devicesxml:
            supported = device.attrib.get('supported','').lower().strip() == 'yes'
            d = {}
            d['supported'] = supported
            d['items'] = {}
            for enum in device:
                k = enum.attrib['name']
                d['items'][k] = xmlIf.TextStripList(enum,'value')
            self._domainCapabilities_['devices'][device.tag] = d
        self._domainCapabilities_['features'] = {}
        for feature in root.find('features'):
            self._domainCapabilities_['features'][feature.tag] = \
                feature.attrib.get('supported', '').lower().strip() == 'yes'

    def _getSysinfo(self, sysinfoxml):
        self._sysinfo_ = {}
        root = ET.fromstring(sysinfoxml)
        if root.attrib.get('type',None):
            self._sysinfo_['type'] = root.attrib['type']
        self._sysinfo_['bios'] = {}
        xmlIf.AttribList_KeyText2Dict(root.find('bios'),'entry','name',self._sysinfo_['bios'])
        self._sysinfo_['baseBoard'] = {}
        xmlIf.AttribList_KeyText2Dict(root.find('baseBoard'),'entry','name',self._sysinfo_['baseBoard'])
        self._sysinfo_['chassis'] = {}
        xmlIf.AttribList_KeyText2Dict(root.find('chassis'),'entry','name',self._sysinfo_['chassis'])
        processorsml = root.findall('processor')
        self._sysinfo_['processor'] = []
        for processor in processorsml:
            d = {}
            xmlIf.AttribList_KeyText2Dict(processor,'entry','name',d)
            self._sysinfo_['processor'].append(d)
        memory_devicesxml = root.findall('memory_device')
        self._sysinfo_['memory_device'] = []
        for memory_device in memory_devicesxml:
            d = {}
            xmlIf.AttribList_KeyText2Dict(memory_device,'entry','name',d)
            self._sysinfo_['memory_device'].append(d)

    def _reflush_capabilities(self):
        self._capabilities_ = self.Capabilities(self._conn.getCapabilities())

    def _reflush_domainCapabilities(self):
        self._getDomainCapabilities(self._conn.getDomainCapabilities())

    def _reflush_libvirtVersion(self):
        tlv = self._conn.getLibVersion()
        self._libvirtVersion_ = "%d.%d.%d" % (
            tlv // 1000000,
            (tlv % 1000000) // 1000,
            tlv % 1000000 % 1000
        )

    def _reflush_sysinfo(self):
        try:
            self._getSysinfo(self._conn.getSysinfo())
        except libvirt.libvirtError as err:
            self._sysinfo_ = err.get_error_message()

    def _reflush_url(self):
        self._url_ = self._conn.getURI()

    def _reflush_type(self):
        self._type_ = self._conn.getType()

    def _reflush_vcpus(self):
        self._vcpus_ = self._conn.getInfo()[2]

    def _reflush_totalMemory(self):
        self._totalMemory_ = self._conn.getMemoryStats(-1).get('total', -1)

    def _reflush_qemuVersion(self):
        tqv = self._conn.getVersion()
        self._qemuVersion_ = "%d.%d.%d" % (
            tqv // 1000000,
            (tqv % 1000000) // 1000,
            tqv % 1000000 % 1000
        )
    
    def reflushInfo(self, key = None):
        if key:
            func = getattr(self, '_reflush_%s' % key, None)
            if not callable(func):
                return False
            func()
            return True
        self._reflush_capabilities()
        self._reflush_domainCapabilities()
        self._reflush_libvirtVersion()
        self._reflush_sysinfo()
        self._reflush_url()
        self._reflush_type()
        self._reflush_vcpus()
        self._reflush_totalMemory()
        self._reflush_qemuVersion()
        return True

    def get(self, key = None):
        if key:
            return getattr(self, '_%s_' % key, None)
        return {
            'capabilities': self._capabilities_,
            'domainCapabilities': self._domainCapabilities_,
            'libvirtVersion': self._libvirtVersion_,
            'sysinfo': self._sysinfo_,
            'url': self._url_,
            'type': self._type_,
            'vcpus': self._vcpus_,
            'totalMemory': self._totalMemory_,
            'qemuVersion': self._qemuVersion_
        }

    def __str__(self):
        return json.dumps({
            'capabilities': self._capabilities_.getDict(),
            'domainCapabilities': self._domainCapabilities_,
            'libvirtVersion': self._libvirtVersion_,
            'sysinfo': self._sysinfo_,
            'url': self._url_,
            'type': self._type_,
            'vcpus': self._vcpus_,
            'totalMemory': self._totalMemory_,
            'qemuVersion': self._qemuVersion_
        })

if __name__ == "__main__":
    import libvirt
    conn = libvirt.open('qemu+ssh://172.17.0.1/system')
    vhio = VirtHostInfo(conn)
    print(json.dumps(vhio.getSysinfo,indent=2))