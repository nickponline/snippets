import usb.core

dev = usb.core.find(idVendor=0xfffe, idProduct=0x0001)
if dev is None:
    raise ValueError('Our device is not connected')