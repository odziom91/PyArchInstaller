###
###
###  PyArchInstaller
###  (c)2021 - created by OdzioM
###
###

import gettext
import os
import configparser
import threading
import time
import subprocess
from PySimpleGUI import PySimpleGUI as sg

### desktops
# gnome
gnome_minimal = ["gnome", "xdg-user-dirs", "gvfs"]
gnome_full = ["gnome", "gnome-extra", "xdg-user-dirs", "gvfs"]
# plasma
plasma_minimal = ["plasma", "xdg-user-dirs", "gvfs"]
plasma_full = ["plasma", "kde-applications", "xdg-user-dirs", "gvfs"]
# xfce
xfce_minimal = ["xfce4", "xdg-user-dirs", "gvfs"]
xfce_full = ["xfce4", "xfce4-goodies", "xdg-user-dirs", "gvfs"]
# mate
mate_minimal = ["mate", "xdg-user-dirs", "gvfs"]
mate_full = ["mate", "mate-extra", "xdg-user-dirs", "gvfs"]
# cinnammon
cinnamon_full = ["cinnamon", "cinnamon-translations", "xdg-user-dirs", "gvfs"]

### login managers
# lightdm
lightdm = ["lightdm", "lightdm-gtk-greeter", "lightdm-gtk-greeter-settings"]
# gdm
gdm = ["gdm"]
# sddm
sddm = ["sddm"]

### video drivers
# vesa and mesa
vesa_mesa = ["xf86-video-vesa", "mesa"]
# nvidia
nvidia_dkms = ["dkms", "nvidia-dkms", "nvidia-utils", "nvidia-settings"]
nvidia = ["nvidia", "nvidia-utils", "nvidia-settings"]
nouveau = ["xf86-video-nouveau"]
# intel
intel = ["xf86-video-intel"]
# amd
amd = ["xf86-video-amdgpu"]
# virtualbox, vmware
virtualbox = ["virtualbox-guest-utils", "xf86-video-vmware"]

### display servers
# xorg
xorg = ["xorg-server", "xorg-xinit", "xorg-xrandr", "arandr", "xterm"]
# wayland
wayland = [""]

### sound servers
# pulseaudio
pulseaudio = ["pulseaudio", "pulseaudio-alsa", "pavucontrol"]
# pipewire
pipewire = ["pipewire", "pipewire-alsa", "pipewire-pulse", "pipewire-jack", "pavucontrol"]

### services
# ntfs
ntfs = ["ntfs-3g"]
# cups
cups = ["cups"]
# network manager
nm_other = ["networkmanager", "nm-connection-editor", "network-manager-applet"]
nm_plasma = ["networkmanager", "nm-connection-editor", "plasma-nm"]
# dhcp
dhcp = ["dhcpcd"]
# wifi
wifi = ["wpa_supplicant", "dialog"]
# pppoe
pppoe = ["rp-pppoe"]
# mobile
mobile = ["modemmanager", "mobile-broadband-provider-info", "usb_modeswitch"]
# bluetooth
bluetooth = ["bluez bluez-utils"]
blueman = ["blueman"]
kbluetooth = ["blueman"]

### addons
# codecs
codecs = ["mpg123", "libcdio"]
# fonts
fonts = ["ttf-inconsolata", "ttf-dejavu", "ttf-font-awesome", "ttf-joypixels"]

### grub
# grub - bios/legacy
grub_bios = ["grub", "os-prober"]
# grub - uefi
grub_uefi = ["grub", "efibootmgr", "os-prober"]

def pai_install(outfile, packages):
    setup = open('output/' + outfile + '.sh', 'a')
    setup.write('#!/bin/bash\n')
    setup.write('pacman -S --noconfirm --needed --quiet ')
    for package in packages:
        setup.write(str(package) + ' ')
    setup.write('\nexit\n')
    setup.close()

def pai_service(outfile, service):
    setup = open('output/' + outfile + '.sh', 'a')
    setup.write('#!/bin/bash\n')
    setup.write('systemctl enable ' + service + '\n')
    setup.write('exit\n')
    setup.close()

def pai_grub(outfile, part):
    setup = open('output/' + outfile + '.sh', 'a')
    setup.write('#!/bin/bash\n')
    if part == "true":
        setup.write("grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=Arch --recheck\n")
    else:
        setup.write("mkdir -p /boot/grub/\n")
        setup.write("grub-install --target=i386-pc " + part + "\n")
    setup.write("grub-mkconfig -o /boot/grub/grub.cfg\n")
    setup.write("exit\n")
    setup.close()

def pai_chroot(filename):
    subprocess.call('cp ./output/' + filename + '.sh /mnt', shell=True)
    subprocess.call('chmod +x /mnt/' + filename + '.sh', shell=True)
    subprocess.call('arch-chroot /mnt bash -c "./' + filename + '.sh"', shell=True)
    subprocess.call('rm /mnt/' + filename + '.sh', shell=True)

def pai_hostname(hostname):
    setup = open('output/hostname.sh', 'a')
    setup.write('#!/bin/bash\n')
    setup.write('echo ' + hostname + ' > /etc/hostname\n')
    setup.write('echo "> /etc/hosts file"\n')
    setup.write('echo 127.0.0.1 ' + 'localhost' + ' > /etc/hosts\n')
    setup.write('echo ::1 ' + 'localhost' + ' >> /etc/hosts\n')
    setup.write('echo 127.0.1.1 ' + hostname + '.localdomain ' + hostname + ' >> /etc/hosts\n')
    setup.write('exit\n')
    setup.close()

def pai_timezone(tz):
    setup = open('output/tz.sh', 'a')
    setup.write('#!/bin/bash\n')
    setup.write('rm -rf /etc/localtime\n')
    setup.write('ln -sf /usr/share/zoneinfo/' + tz + ' /etc/localtime\n')
    setup.write('timedatectl set-timezone \"' + tz + '"\n')
    setup.write('hwclock --systohc\n')
    setup.write('timedatectl set-ntp true\n')
    setup.write('exit\n')
    setup.close()

def pai_lang(lang):
    locale = lang
    split = lang.split(" ")
    locale2 = split[0]
    setup = open('output/lang.sh', 'a')
    setup.write('#!/bin/bash\n')
    setup.write('echo "' + locale + '" >> /etc/locale.gen\n')
    setup.write('locale-gen\n')
    setup.write('echo LANG=' + locale2 + ' > /etc/locale.conf\n')
    setup.write('export LANG=' + locale2 + '\n')
    setup.write('exit\n')
    setup.close()

def pai_kbd(kbd):
    setup = open('output/kbd.sh', 'a')
    setup.write('#!/bin/bash\n')
    setup.write('localectl --no-convert set-x11-keymap ' + kbd + '\n')
    setup.write('echo KEYMAP=' + kbd + ' > /etc/vconsole.conf\n')
    setup.write('setxkbmap ' + kbd + '\n')
    setup.write('exit\n')
    setup.close()

def pai_update_repo():
    setup = open('output/update_repo.sh', 'a')
    setup.write('#!/bin/bash\n')
    setup.write('pacman -Syy\n')
    setup.write('exit\n')
    setup.close()

def pai_installation(lang, window):
    ###
    ### start installation
    ###
    window["-PROBAR-"].update_bar(0)
    window["-STATUS-"].update("Status: Przygotowanie do instalacji")

    #################################################################
    #                                                               #
    #                       NON-CHROOT PART                         #
    #                                                               #
    #################################################################

    ###
    ### read configs
    ###
    # read config file
    config = configparser.ConfigParser()
    config.read("config/settings.cfg")
    # General
    cfg_hostname = config["General"]["hostname"]
    cfg_lang = config["General"]["lang"]
    cfg_kbd = config["General"]["kbd"]
    cfg_tz = config["General"]["tz"]
    # Desktop
    cfg_desktop = config["Desktop"]["de"]
    cfg_lm = config["Desktop"]["lm"]
    # Services
    cfg_nm = config["Services"]["nm"]
    cfg_dhcp = config["Services"]["dhcp"]
    cfg_wifi = config["Services"]["wifi"]
    cfg_pppoe = config["Services"]["pppoe"]
    cfg_mobile = config["Services"]["mobile"]
    cfg_bt = config["Services"]["bluetooth"]
    cfg_cups = config["Services"]["cups"]
    #cfg_ntfs = config["Services"]["ntfs"]
    # Video
    cfg_vdriver = config["Video"]["driver"]
    # Grub
    cfg_grub = config["Grub"]["grub"]
    # Kernel
    cfg_kernel = config["General"]["kernel"]
    # Multilib
    cfg_multilib = config["Services"]["multilib"]

    ###
    ### update repo before pacstrap
    ### 
    window["-PROBAR-"].update_bar(5)
    window["-STATUS-"].update("Status: Aktualizacja repozytoriów")
    subprocess.call("pacman -Syy --noconfirm --quiet archlinux-keyring", shell=True)

    ###
    ### install base + kernel
    ###
    window["-PROBAR-"].update_bar(10)
    window["-STATUS-"].update(_("Base+Kernel installation"))
    if cfg_kernel == "stable":
        subprocess.call("pacstrap /mnt base base-devel linux linux-firmware linux-headers sudo nano dialog reflector", shell=True)
    if cfg_kernel == "longterm":
        subprocess.call("pacstrap /mnt base base-devel linux-lts linux-firmware linux-lts-headers sudo nano dialog reflector", shell=True)
    if cfg_kernel == "zen":
        subprocess.call("pacstrap /mnt base base-devel linux-zen linux-firmware linux-zen-headers sudo nano dialog reflector", shell=True)
    if cfg_kernel == "hardened":
        subprocess.call("pacstrap /mnt base base-devel linux-hardened linux-firmware linux-hardened-headers sudo nano dialog reflector", shell=True)

    ###
    ### generate fstab file
    ###
    window["-PROBAR-"].update_bar(15)
    window["-STATUS-"].update(_("Generate fstab file"))
    subprocess.call("genfstab -U /mnt >> /mnt/etc/fstab", shell=True)
    
    ###
    ### config mirrorlist
    ###
    window["-PROBAR-"].update_bar(20)
    window["-STATUS-"].update(_("Generate mirrorlist"))
    subprocess.call("cp /etc/pacman.d/mirrorlist /mnt/etc/pacman.d/mirrorlist", shell=True)
    subprocess.call("pacman -Syy", shell=True)
    # config multilib if enabled
    if cfg_multilib == "true":
        window["-PROBAR-"].update_bar(25)
        window["-STATUS-"].update(_("Multilib repository configuration"))
        subprocess.call("echo \"\" >> /mnt/etc/pacman.conf", shell=True)    
        subprocess.call("echo \"[multilib]\" >> /mnt/etc/pacman.conf", shell=True)
        subprocess.call("echo \"Include = /etc/pacman.d/mirrorlist\" >> /mnt/etc/pacman.conf", shell=True)

    #################################################################
    #                                                               #
    #                         CHROOT PART                           #
    #                                                               #
    #################################################################

    ### update repo
    window["-PROBAR-"].update_bar(30)
    window["-STATUS-"].update(_("Repository update"))
    pai_update_repo()
    pai_chroot("update_repo")

    ###
    # Configuration
    ###

    ### config hostname
    window["-PROBAR-"].update_bar(35)
    window["-STATUS-"].update(_("Hostname configuration"))
    pai_hostname(cfg_hostname)
    pai_chroot("hostname")
    ### config timezone
    window["-PROBAR-"].update_bar(40)
    window["-STATUS-"].update(_("Time zone configuration"))
    pai_timezone(cfg_tz)
    pai_chroot("tz")
    ### config language
    window["-PROBAR-"].update_bar(45)
    window["-STATUS-"].update(_("System language configuration"))
    pai_lang(cfg_lang)
    pai_chroot("lang")

    ###
    # Software installation
    ###

    ### install desktop
    window["-PROBAR-"].update_bar(50)
    window["-STATUS-"].update(_("Desktop Environment installation"))
    # desktop
    if cfg_desktop == "gnome_minimal":
        pai_install("de", gnome_minimal)
    if cfg_desktop == "gnome":
        pai_install("de", gnome_full)
    if cfg_desktop == "plasma_minimal":
        pai_install("de", plasma_minimal)
    if cfg_desktop == "plasma":
        pai_install("de", plasma_full)
    if cfg_desktop == "xfce_minimal":
        pai_install("de", xfce_minimal)
    if cfg_desktop == "xfce":
        pai_install("de", xfce_full)
    if cfg_desktop == "mate_minimal":
        pai_install("de", mate_minimal)
    if cfg_desktop == "mate":
        pai_install("de", mate_full)
    if cfg_desktop == "cinnamon":
        pai_install("de", cinnamon_full)
    pai_chroot("de")
    ### install login manager
    window["-PROBAR-"].update_bar(55)
    window["-STATUS-"].update(_("Login Manager installation"))
    # login manager
    if cfg_lm == "lightdm":
        pai_install("lm", lightdm)
        pai_service("lm_service", "lightdm.service")
    if cfg_lm == "gdm":
        pai_install("lm", gdm)
        pai_service("lm_service", "gdm")
    if cfg_lm == "sddm":
        pai_install("lm", sddm)
        pai_service("lm_service", "sddm")
    pai_chroot("lm")
    pai_chroot("lm_service")
    ### install video driver
    window["-PROBAR-"].update_bar(60)
    window["-STATUS-"].update(_("Video driver installation"))
    pai_install("vesa_mesa", vesa_mesa)
    pai_install("xorg", xorg)
    pai_chroot("vesa_mesa")
    pai_chroot("xorg")
    if cfg_vdriver == "nvdkms":
        pai_install("video", nvidia_dkms)
        pai_chroot("video")
    if cfg_vdriver == "nvnodkms":
        pai_install("video", nvidia)
        pai_chroot("video")
    if cfg_vdriver == "nouveau":
        pai_install("video", nouveau)
        pai_chroot("video")
    if cfg_vdriver == "intel":
        pai_install("video", intel)
        pai_chroot("video")
    if cfg_vdriver == "amd":
        pai_install("video", amd)
        pai_chroot("video")
    if cfg_vdriver == "vbox":
        pai_install("video", virtualbox)
        pai_service("video_service", "vboxservice.service")
        pai_chroot("video")
        pai_chroot("video_service")
    ### install sound server
    window["-PROBAR-"].update_bar(65)
    window["-STATUS-"].update(_("Sound server installation"))
    # todo pipewire support
    pai_install("sound", pulseaudio)
    pai_chroot("sound")
    ### install codecs
    window["-PROBAR-"].update_bar(70)
    window["-STATUS-"].update(_("Codecs installation"))
    pai_install("codecs", codecs)
    pai_chroot("codecs")
    ### install fonts
    window["-PROBAR-"].update_bar(75)
    window["-STATUS-"].update(_("Fonts installation"))
    pai_install("fonts", fonts)
    
    ###
    # Services installation
    ###

    ### install network mananger
    if cfg_nm == "true":
        window["-PROBAR-"].update_bar(80)
        window["-STATUS-"].update(_("Network Manager installation"))
        if "plasma" in cfg_desktop:
            pai_install("nm", nm_plasma)
            pai_service("nm_service", "NetworkManager.service")
        else:
            pai_install("nm", nm_other)
            pai_service("nm_service", "NetworkManager.service")
        pai_chroot("nm")
        pai_chroot("nm_service")
    ### install DHCP
    if cfg_dhcp == "true":
        window["-PROBAR-"].update_bar(81)
        window["-STATUS-"].update(_("DHCP service installation"))
        pai_install("dhcp", dhcp)
        pai_service("dhcp_service", "dhcpcd.service")
        pai_chroot("dhcp")
        pai_chroot("dhcp_service")
    ### install wifi
    if cfg_wifi == "true":
        window["-PROBAR-"].update_bar(82)
        window["-STATUS-"].update(_("Wi-Fi support installation"))
        pai_install("wifi", wifi)
        pai_chroot("wifi")
    ### install pppoe
    if cfg_pppoe == "true":
        window["-PROBAR-"].update_bar(83)
        window["-STATUS-"].update(_("PPPoE support installation"))
        pai_install("pppoe", pppoe)
        pai_chroot("pppoe")
    ### install mobile
    if cfg_mobile == "true":
        window["-PROBAR-"].update_bar(84)
        window["-STATUS-"].update(_("Broadband support installation"))
        pai_install("mobile", mobile)
        pai_chroot("mobile")
    ### install bluetooth
    if cfg_bt == "true":
        window["-PROBAR-"].update_bar(85)
        window["-STATUS-"].update(_("Bluetooth support installation"))
        pai_install("bluetooth", bluetooth)
        pai_service("bluetooth_service", "bluetooth")
        pai_chroot("bluetooth")
        pai_chroot("bluetooth_service")
    ### install NTFS
    window["-PROBAR-"].update_bar(86)
    window["-STATUS-"].update(_("NTFS support installation"))
    pai_install("ntfs", ntfs)
    pai_chroot("ntfs")
    ### install CUPS
    if cfg_cups == "true":
        window["-PROBAR-"].update_bar(87)
        window["-STATUS-"].update(_("CUPS - Printing service installation"))
        pai_install("cups", cups)
        pai_service("cups_service", "cupsd.service")
        pai_chroot("cups")
        pai_chroot("cups_service")
    ### keyboard layout configuration
    window["-PROBAR-"].update_bar(90)
    window["-STATUS-"].update(_("Keyboard layout configuration"))
    pai_kbd(cfg_kbd)
    pai_chroot("kbd")

    ###
    # Bootloader
    ###

    ### install bootloader
    window["-PROBAR-"].update_bar(95)
    window["-STATUS-"].update(_("Bootloader installation"))
    if int(subprocess.check_output("ls /sys/firmware/efi/efivars | wc -l", shell=True)) > 1:
        pai_install("grub", grub_uefi)
        pai_grub("grub_config", "true")
    else:
        pai_install("grub", grub_bios)
        pai_grub("grub_config", cfg_grub)
    pai_chroot("grub")
    pai_chroot("grub_config")    
    window["-PROBAR-"].update_bar(100)
    window["-STATUS-"].update(_("Installation complete - please close this window."))
    config.set('Summary', 'Installation', 'True')
    with open('config/settings.cfg', 'w') as configfile:
        config.write(configfile)



def pai_install_wnd(lang):
    ans = True
    while ans:
        sg.SetOptions(font=("Monospace Regular", 12), margins=(0, 0))
        sg.theme("Dark")
        logo = [
            [sg.Image("./gfx/small_logo.png")]
        ]
        install = [
            [sg.Text(_("ArchLinux Installation"), size=(35, 1))],
            [sg.ProgressBar(100, orientation='h', size=(62, 30), key='-PROBAR-')],
            [sg.Text("", size=(62, 1), key='-STATUS-')]
        ]
        run_installer = [
            [sg.Button(_("Install ArchLinux"), size=(56, 1), pad=((4, 4), (0, 4)), key="btn_run")]
        ]
        gui = [
            [sg.Column(layout=logo)],
            [sg.Column(layout=install)],
            [sg.Column(layout=run_installer)]
        ]
        window = sg.Window("PyArchInstaller", gui, finalize=True, size=(600, 520), location=(100, 100))
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                ans = False
                break
            if event == "btn_run":
                try:
                    window.Element("btn_run").update(disabled=True)
                    ans = False
                    x = threading.Thread(target=pai_installation, args=(lang, window, ))
                    x.start()
                except Exception as e:
                    print(str(e))
        window.close()

