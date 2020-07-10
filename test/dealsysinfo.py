#!/usr/bin/env python3 
from collections import Counter, defaultdict
import json
import xml.etree.ElementTree

sysinfo = '''<sysinfo type='smbios'>
  <bios>
    <entry name='vendor'>Dell Inc.</entry>
    <entry name='version'>2.4.2</entry>
    <entry name='date'>01/29/2015</entry>
    <entry name='release'>2.4</entry>
  </bios>
  <system>
    <entry name='manufacturer'>Dell Inc.</entry>
    <entry name='product'>PowerEdge R420</entry>
    <entry name='version'>Not Specified</entry>
    <entry name='serial'>JC3CC52</entry>
    <entry name='uuid'>4c4c4544-0043-3310-8043-cac04f433532</entry>
    <entry name='sku'>SKU=NotProvided;ModelName=PowerEdge R420</entry>
    <entry name='family'>Not Specified</entry>
  </system>
  <baseBoard>
    <entry name='manufacturer'>Dell Inc.</entry>
    <entry name='product'>0K7WRR</entry>
    <entry name='version'>A02</entry>
    <entry name='serial'>..CN77921536001W.</entry>
    <entry name='asset'>Not Specified</entry>
  </baseBoard>
  <chassis>
    <entry name='manufacturer'>Dell Inc.</entry>
    <entry name='version'>Not Specified</entry>
    <entry name='serial'>JC3CC52</entry>
    <entry name='asset'>Not Specified</entry>
    <entry name='sku'>Not Specified</entry>
  </chassis>
  <processor>
    <entry name='socket_destination'>CPU1</entry>
    <entry name='type'>Central Processor</entry>
    <entry name='family'>Xeon</entry>
    <entry name='manufacturer'>Intel</entry>
    <entry name='signature'>Type 0, Family 6, Model 45, Stepping 7</entry>
    <entry name='version'>       Intel(R) Xeon(R) CPU E5-2420 0 @ 1.90GHz</entry>
    <entry name='external_clock'>7200 MHz</entry>
    <entry name='max_speed'>3600 MHz</entry>
    <entry name='status'>Populated, Enabled</entry>
    <entry name='serial_number'>Not Specified</entry>
    <entry name='part_number'>Not Specified</entry>
  </processor>
  <processor>
    <entry name='socket_destination'>CPU2</entry>
    <entry name='type'>Central Processor</entry>
    <entry name='family'>Xeon</entry>
    <entry name='manufacturer'>Intel</entry>
    <entry name='signature'>Type 0, Family 6, Model 45, Stepping 7</entry>
    <entry name='version'>       Intel(R) Xeon(R) CPU E5-2420 0 @ 1.90GHz</entry>
    <entry name='external_clock'>7200 MHz</entry>
    <entry name='max_speed'>3600 MHz</entry>
    <entry name='status'>Populated, Idle</entry>
    <entry name='serial_number'>Not Specified</entry>
    <entry name='part_number'>Not Specified</entry>
  </processor>
  <memory_device>
    <entry name='size'>16384 MB</entry>
    <entry name='form_factor'>DIMM</entry>
    <entry name='locator'>DIMM_A1</entry>
    <entry name='bank_locator'>Not Specified</entry>
    <entry name='type'>DDR3</entry>
    <entry name='type_detail'>Synchronous Registered (Buffered)</entry>
    <entry name='speed'>1600 MT/s</entry>
    <entry name='manufacturer'>00CE00B300CE</entry>
    <entry name='serial_number'>19CDC07F</entry>
    <entry name='part_number'>M393B2G70DB0-YK0</entry>
  </memory_device>
  <memory_device>
    <entry name='size'>16384 MB</entry>
    <entry name='form_factor'>DIMM</entry>
    <entry name='locator'>DIMM_A2</entry>
    <entry name='bank_locator'>Not Specified</entry>
    <entry name='type'>DDR3</entry>
    <entry name='type_detail'>Synchronous Registered (Buffered)</entry>
    <entry name='speed'>1600 MT/s</entry>
    <entry name='manufacturer'>00CE00B300CE</entry>
    <entry name='serial_number'>19CDC07E</entry>
    <entry name='part_number'>M393B2G70DB0-YK0</entry>
  </memory_device>
  <memory_device>
    <entry name='size'>16384 MB</entry>
    <entry name='form_factor'>DIMM</entry>
    <entry name='locator'>DIMM_B1</entry>
    <entry name='bank_locator'>Not Specified</entry>
    <entry name='type'>DDR3</entry>
    <entry name='type_detail'>Synchronous Registered (Buffered)</entry>
    <entry name='speed'>1600 MT/s</entry>
    <entry name='manufacturer'>00CE00B300CE</entry>
    <entry name='serial_number'>19CDC58D</entry>
    <entry name='part_number'>M393B2G70DB0-YK0</entry>
  </memory_device>
  <memory_device>
    <entry name='size'>16384 MB</entry>
    <entry name='form_factor'>DIMM</entry>
    <entry name='locator'>DIMM_B2</entry>
    <entry name='bank_locator'>Not Specified</entry>
    <entry name='type'>DDR3</entry>
    <entry name='type_detail'>Synchronous Registered (Buffered)</entry>
    <entry name='speed'>1600 MT/s</entry>
    <entry name='manufacturer'>00CE00B300CE</entry>
    <entry name='serial_number'>19CDA2B5</entry>
    <entry name='part_number'>M393B2G70DB0-YK0</entry>
  </memory_device>
</sysinfo>'''

sysinfo2 = '''<sysinfo type='smbios'>
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
'''

doc = xml.etree.ElementTree.fromstring(sysinfo2)

infojson = {}

for k,num in Counter(map(lambda x: x.tag, doc)).items():
    if num == 1:
        ele = doc.find(k)
        d = {}
        for entry in ele:
            name = entry.attrib.get('name')
            value = entry.text.strip()
            d[name] = None if value == 'Not Applicable' else value
        infojson[k] = d
    else:
        infojson[k] = []
        eles = doc.findall(k)
        for ele in eles:
            d = {}
            for entry in ele:
                name = entry.attrib.get('name')
                value = entry.text.strip()
                d[name] = value
            infojson[k].append(d)

print(json.dumps(infojson,indent=2))
