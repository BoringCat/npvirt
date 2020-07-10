#!/usr/bin/env python3

import libvirt
from uuid import uuid4

uuidgen = lambda : str(uuid4())

conn = libvirt.open('qemu+ssh://172.17.0.1/system')

conn.createXML('''<domain type='kvm'>
  <name>demo</name>
  <uuid>{uuid}<uuid>
  <memory>{memory}</memory>
  <vcpu>{cpus}</vcpu>
  <clock offset='utc'/>
  <on_poweroff>destroy</on_poweroff>
  <on_reboot>restart</on_reboot>
  <on_crash>destroy</on_crash>
  <devices>
    <input type='mouse' bus='ps2'/>
    <graphics type='vnc' port='-1' listen='127.0.0.1'/>
  </devices>
</domain>
'''.format(
    uuid=uuidgen(),
    memory=2*1024*1024,
    cpus=2
))

""