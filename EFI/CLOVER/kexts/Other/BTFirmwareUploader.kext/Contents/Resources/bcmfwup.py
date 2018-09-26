# Working version for Mac OSX
# Just we don't need to use attach and deatch drivers methods
#Steps:

#1. Install pyusb : sudo easy_install pyusb
#2. Install libusb pkg
#3. Edit the line "hex = intelhex('BCM.hex')" with the file name of BCM firmware in the current directory
#4. Initialize the bluetooth hardware using BTFirmwareLoader kext(use only Initialize method)
#5. Run script in terminal: python bcmfwup.py
#6. Load Broadcom kext for making bluetooth working

#!/usr/bin/python2
# -*- coding: utf-8 -*-

import sys
import usb.core
import usb.util
import threading
import time

ID_VENDOR = 0x13d3
ID_PRODUCT = 0x3404

class bcm_fw_up:

  def __init__(self):
    self.dev = usb.core.find(idVendor = 0x13d3, idProduct = 0x3404)

    if self.dev is None:
      raise ValueError('Device not found')

    self.cfg = self.dev.get_active_configuration()
    #self.detach_drivers()

  def detach_drivers(self):
    for intf in self.cfg:
      if self.dev.is_kernel_driver_active(intf.bInterfaceNumber):
        self.dev.detach_kernel_driver(intf.bInterfaceNumber)

  def attach_drivers(self):
    for intf in self.cfg:
      if not self.dev.is_kernel_driver_active(intf.bInterfaceNumber):
        self.dev.attach_kernel_driver(intf.bInterfaceNumber)
  
  def init_upload(self):
    re = read_event_thread(self.dev)
    re.read()
    self.dev.ctrl_transfer(0x20, 0, data_or_wLength = [0x79, 0xfc, 0x00])
    re.join()
    re = read_event_thread(self.dev)
    re.read()
    self.dev.ctrl_transfer(0x20, 0, data_or_wLength = [0x2e, 0xfc, 0x00])
    re.join()

  def finish_upload(self):
    re = read_event_thread(self.dev)
    re.read()
    self.dev.ctrl_transfer(0x20, 0, data_or_wLength = [0x4e, 0xfc, 0x04, 0xff, 0xff, 0xff, 0xff])
    re.join()
    re = read_event_thread(self.dev)
    re.read()
    re.join()
    re = read_event_thread(self.dev)
    re.read()
    self.dev.ctrl_transfer(0x20, 0, data_or_wLength = [0x79, 0xfc, 0x00])
    re.join()
    re = read_event_thread(self.dev)
    re.read()
    #re2 = read_event_thread(self.dev, 0x82)
    #re2.read()
    self.dev.ctrl_transfer(0x20, 0, data_or_wLength = [0x53, 0xfc, 0x01, 0x13])
    re.join()
    #re2.join()

  def upload(self, address, data):
    re = read_event_thread(self.dev)
    re.read()
    self.dev.write(2, '\x4c\xfc' + chr(len(data) + 4) + chr(address & 0xFF) +
      chr((address >> 8) & 0xFF) + chr((address >> 16) & 0xFF) + chr((address >> 24) & 0xFF) + data)
    re.join()

  def reset(self):
    re = read_event_thread(self.dev)
    re.read()
    self.dev.ctrl_transfer(0x20, 0, data_or_wLength = [0x03, 0x0c, 0x00])
    re.join()
    usb.util.dispose_resources(self.dev)
    self.cfg = self.dev.get_active_configuration()


class read_event_thread(threading.Thread):
  def __init__(self, dev, endpoint = 0x81):
    super(read_event_thread, self).__init__()
    self.daemon = True
    self.dev = dev
    self.endpoint = endpoint

  def run(self):
    try:
      self.result = self.dev.read(self.endpoint, 0xff)
    except usb.core.USBError as (errno, strerror):
      print "read event error({0}): {1}".format(errno, strerror)
    print 'event:', self.result

  def read(self):
    self.start()
    time.sleep(0.1)


class intelhex:

  data = []

  def __init__(self, filename = None):
    self.offset = 0
    if filename is None:
      return
    self.load_from_file(filename)

  def load_from_file(self, filename):
    for line in open(filename):
      self.append(line)

  def append(self, line):
    if not line[0] == ':':
      return
    line = line.rstrip()
    length = int(line[1:3], 16)
    address = int(line[3:7], 16)
    rectype = int(line[7:9], 16)
    checksum = int(line[-2:], 16)
    if rectype == 1:
      return
    if rectype == 4:
      self.offset = int(line[9:13], 16) * 0x10000
      return
    self.data.append((length, address + self.offset, line[9:-2].decode('hex'), checksum))


def main():
  hex = intelhex('BCM.hex')
  up = bcm_fw_up()
  up.init_upload()
  for line in hex.data:
    up.upload(line[1], line[2])
  up.finish_upload()
  up.reset()
  #up.attach_drivers()
  return 0

if __name__ == '__main__':
  sys.exit(main())
