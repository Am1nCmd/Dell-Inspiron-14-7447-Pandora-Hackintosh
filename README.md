# Dell Inspiron 14 7447 Pandora Hackintosh
[![image.png](https://i.postimg.cc/yN1XXpdF/image.png)](https://postimg.cc/XrPCn89J)

## Update 16 Aug 2021
- Update to OpenCore Bootloader v0.7.2
- Add support with macOS BigSur 11.5.2

## Update 4 Feb 2021
- Adding OpenCore Bootloader
- Now you can choose between Clover or OpenCore Bootloader
- Update and optimize config for macOS Catalina

## How to use it
Place EFI folder on your EFI Partition

## Specification :
- Processor : Intel Core i7 4720HQ
- IGPU : Intel HD Graphics 4600
- GPU Discrette : Nvidia GTX 950M 4GB DDR3
- RAM : 8GB DDR3 PC12800/1600Mhz (4GB + 4GB)
- Storage : SSD Samsung 850 Pro 256GB + HDD Toshiba 1TB
- Audio Codec : Realtek ALC255
- LAN : Realtek RTL8168GU Gigabit Port
- Wifi : Broadcomm BCM94352Z + Bluetooth
- Touchpad : Synaptic PS2 Interface
- Screen Size : 14"
- Screen Resolution : 1366 x 768
- Boot Mode : UEFI
- Bootloader : OpenCore r0.7.2
- macOS Version : macOS Big Sur 11.5.2 Build 20G95


## Work
- QE/CI Graphics of Intel HD 4600
- Restart, Shutdown and Sleep
- CPU Power Management
- Internal Speaker, Internal Mic and External Headphone
- Ethernet
- Wifi
- AirDrop
- Handoff
- HDMI Out (Video & Audio)
- Brightness
- Brightness UP/Down
- All USB Ports
- Touchpad
- Battery Indicator
- Etc


## Not Working
- Nvidia Card (Switchable Graphics is not supported by Hackintosh)
- Etc

##Known Issue
- you need to attach HDMI cable before power on your OS, otherwise HDMI audio will not working (I'm testing it on HDMI (ARC))
- you may need to install ALCPluginFix every time if you want to use headphone / earphone
