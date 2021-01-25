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

# install base + devel - ok
# kernel - ok
# "pacman -Syy" - ok
# "pacstrap /mnt base base-devel linux linux-firmware linux-headers" - ok
# system config:
# locale, locale2 - ok
# keymap - ok
# timezone - ok
# nm - ok
# wifi - ok
# pppoe - ok
# mobile - ok
# dhcp - ok
# de - ok
# dm - ok
# video driver - ok
# hostname - ok
# multilib - ok
# sudo i sudoers


def c_hostname(hostname):
    setup = open("output/hostname.sh", "a")
    setup.write('#!/bin/bash\n')
    setup.write('echo ' + hostname + ' > /etc/hostname\n')
    setup.write('echo "> /etc/hosts file"\n')
    setup.write('echo 127.0.0.1 ' + 'localhost' + ' > /etc/hosts\n')
    setup.write('echo ::1 ' + 'localhost' + ' >> /etc/hosts\n')
    setup.write('echo 127.0.1.1 ' + hostname + '.localdomain ' + hostname + ' >> /etc/hosts\n')
    setup.write('exit\n')
    setup.close()

def c_timezone(tz):
    setup = open("output/tz.sh", "a")
    setup.write('#!/bin/bash\n')
    setup.write('rm -rf /etc/localtime\n')
    setup.write('ln -sf /usr/share/zoneinfo/' + tz + ' /etc/localtime\n')
    setup.write('timedatectl set-timezone \"' + tz + '"\n')
    setup.write('hwclock --systohc\n')
    setup.write('timedatectl set-ntp true\n')
    setup.write('exit\n')
    setup.close()

def c_lang(lang):
    locale = lang
    split = lang.split(" ")
    locale2 = split[0]
    setup = open("output/lang.sh", "a")
    setup.write('#!/bin/bash\n')
    setup.write('echo "' + locale + '" >> /etc/locale.gen\n')
    setup.write('locale-gen\n')
    setup.write('echo LANG=' + locale2 + ' > /etc/locale.conf\n')
    setup.write('export LANG=' + locale2 + '\n')
    setup.write('exit\n')
    setup.close()

def c_kbd(kbd):
    setup = open("output/kbd.sh", "a")
    setup.write('#!/bin/bash\n')
    setup.write('localectl --no-convert set-x11-keymap ' + kbd + '\n')
    setup.write('echo KEYMAP=' + kbd + ' > /etc/vconsole.conf\n')
    setup.write('setxkbmap ' + kbd + '\n')
    setup.write('exit\n')
    setup.close()

def c_nm(nm, de):
    setup = open("output/nm.sh", "a")
    setup.write('#!/bin/bash\n')
    if nm == "true":
        setup.write('pacman -S --noconfirm --quiet networkmanager nm-connection-editor\n')
        setup.write('systemctl enable NetworkManager.service\n')
        if de == "plasma":
            setup.write('pacman -S --noconfirm --quiet plasma-nm\n')
        else:
            setup.write('pacman -S --noconfirm --quiet network-manager-applet\n')
    setup.write('exit\n')
    setup.close()

def c_dhcp(dhcp):
    setup = open("output/dhcp.sh", "a")
    setup.write('#!/bin/bash\n')
    if dhcp == "true":
        setup.write('pacman -S --noconfirm --quiet dhcpcd\n')
        setup.write('systemctl enable dhcpcd.service\n')
    setup.write('exit\n')
    setup.close()

def c_wifi(wifi):
    setup = open("output/wifi.sh", "a")
    setup.write('#!/bin/bash\n')
    if wifi == "true":
        setup.write('pacman -S --noconfirm --quiet wpa_supplicant dialog\n')
    setup.write('exit\n')
    setup.close()

def c_pppoe(pppoe):
    setup = open("output/pppoe.sh", "a")
    setup.write('#!/bin/bash\n')
    if pppoe == "true":
        setup.write('pacman -S --noconfirm --quiet rp-pppoe\n')
    setup.write('exit\n')
    setup.close()

def c_mobile(mobile):
    setup = open("output/mobile.sh", "a")
    setup.write('#!/bin/bash\n')
    if mobile == "true":
        setup.write('pacman -S --noconfirm --quiet modemmanager mobile-broadband-provider-info usb_modeswitch\n')
    setup.write('exit\n')
    setup.close()

def c_de(de):
    setup = open("output/de.sh", "a")
    setup.write('#!/bin/bash\n')
    if de == "gnome":
        setup.write('pacman -S --noconfirm --quiet gnome gnome-extra\n')
        setup.write('pacman -S --noconfirm --quiet ttf-inconsolata ttf-dejavu ttf-font-awesome ttf-joypixels xdg-user-dirs\n')
        setup.write('pacman -S --noconfirm --quiet pulseaudio pulseaudio-alsa pavucontrol mpg123 libcdio gvfs\n')
    if de == "plasma":
        setup.write('pacman -S --noconfirm --quiet plasma\n')
        setup.write('pacman -S --noconfirm --quiet kde-applications gvfs\n')
        #setup.write('pacman -S --needed --noconfirm --quiet sddm\n')
    if de == "xfce":
        setup.write('pacman -S --noconfirm --quiet xfce4 xfce4-goodies\n')
        setup.write('pacman -S --noconfirm --quiet ttf-inconsolata ttf-dejavu ttf-font-awesome ttf-joypixels xdg-user-dirs\n')
        setup.write('pacman -S --noconfirm --quiet pulseaudio pulseaudio-alsa pavucontrol mpg123 libcdio gvfs\n')
    if de == "mate":
        setup.write('pacman -S --noconfirm --quiet mate mate-extra\n')
        setup.write('pacman -S --noconfirm --quiet ttf-inconsolata ttf-dejavu ttf-font-awesome ttf-joypixels xdg-user-dirs\n')
        setup.write('pacman -S --noconfirm --quiet pulseaudio pulseaudio-alsa pavucontrol mpg123 libcdio gvfs\n')
    if de == "cinnamon":
        setup.write('pacman -S --noconfirm --quiet cinnamon\n')
        setup.write('pacman -S --noconfirm --quiet cinnamon-translations\n')
        setup.write('pacman -S --noconfirm --quiet ttf-inconsolata ttf-dejavu ttf-font-awesome ttf-joypixels xdg-user-dirs\n')
        setup.write('pacman -S --noconfirm --quiet pulseaudio pulseaudio-alsa pavucontrol mpg123 libcdio gvfs\n')
    setup.write('exit\n')
    setup.close()

def c_lm(lm):
    setup = open("output/lm.sh", "a")
    setup.write('#!/bin/bash\n')
    if lm == "lightdm":
        setup.write('pacman -S --noconfirm --quiet lightdm\n')
        setup.write('pacman -S --noconfirm --quiet lightdm-gtk-greeter lightdm-gtk-greeter-settings\n')
        setup.write('systemctl enable lightdm.service\n')
    if lm == "gdm":
        setup.write('pacman -S --noconfirm --quiet gdm\n')
        setup.write('systemctl enable gdm\n')
    setup.write('exit\n')
    setup.close()

def c_video(video):
    setup = open("output/video.sh", "a")
    setup.write('#!/bin/bash\n')
    setup.write('pacman -S --noconfirm --quiet xf86-video-vesa\n')
    setup.write('pacman -S --noconfirm --quiet mesa\n')
    if video == "nvdkms":
        setup.write('pacman -S --noconfirm --quiet dkms nvidia-dkms nvidia-utils nvidia-settings\n')
    if video == "nvnodkms":
        setup.write('pacman -S --noconfirm --quiet nvidia nvidia-utils nvidia-settings\n')
    if video == "nouveau":
        setup.write('pacman -S --noconfirm --quiet xf86-video-nouveau\n')
    if video == "intel":
        setup.write('pacman -S --noconfirm --quiet xf86-video-intel\n')
    if video == "amd":
        setup.write('pacman -S --noconfirm --quiet xf86-video-amdgpu\n')
    if video == "vbox":
        setup.write('pacman -S --noconfirm --quiet virtualbox-guest-utils xf86-video-vmware\n')
        setup.write('systemctl enable vboxservice.service\n')
    setup.write('pacman -S --noconfirm --quiet xorg-server xorg-xinit xorg-xrandr arandr xterm\n')
    setup.write('exit\n')
    setup.close()

def c_ntfs():
    setup = open("output/ntfs.sh", "a")
    setup.write('#!/bin/bash\n')
    setup.write('pacman -S --noconfirm --quiet ntfs-3g\n')
    setup.write('exit\n')
    setup.close()

def c_cups(cups):
    setup = open("output/cups.sh", "a")
    setup.write('#!/bin/bash\n')
    if cups == "true":
        setup.write('pacman -S --noconfirm --quiet cups\n')
        setup.write('systemctl enable cupsd.service\n')
    setup.write('exit\n')
    setup.close()

def c_grub(efi, grub):
    setup = open("output/grub.sh", "a")
    setup.write('#!/bin/bash\n')
    if efi == True:
        setup.write("pacman -S --noconfirm --quiet grub efibootmgr os-prober\n")
        setup.write("grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=Arch --recheck\n")
    else:
        setup.write("pacman -S --noconfirm --quiet grub os-prober\n")
        setup.write("mkdir -p /boot/grub/\n")
        setup.write("grub-install --target=i386-pc " + grub + "\n")
    setup.write("grub-mkconfig -o /boot/grub/grub.cfg\n")
    setup.write("exit\n")
    setup.close()

def c_update_repo():
    setup = open("output/update_repo.sh", "a")
    setup.write('#!/bin/bash\n')
    setup.write('pacman -Syy\n')
    setup.write("exit\n")
    setup.close()

def prepare_chroot():
    subprocess.call("cp ./output/hostname.sh /mnt/hostname.sh", shell=True)
    subprocess.call("chmod +x /mnt/hostname.sh", shell=True)
    subprocess.call("cp ./output/tz.sh /mnt/tz.sh", shell=True)
    subprocess.call("chmod +x /mnt/tz.sh", shell=True)
    subprocess.call("cp ./output/lang.sh /mnt/lang.sh", shell=True)
    subprocess.call("chmod +x /mnt/lang.sh", shell=True)
    subprocess.call("cp ./output/kbd.sh /mnt/kbd.sh", shell=True)
    subprocess.call("chmod +x /mnt/kbd.sh", shell=True)
    subprocess.call("cp ./output/nm.sh /mnt/nm.sh", shell=True)
    subprocess.call("chmod +x /mnt/nm.sh", shell=True)
    subprocess.call("cp ./output/dhcp.sh /mnt/dhcp.sh", shell=True)
    subprocess.call("chmod +x /mnt/dhcp.sh", shell=True)
    subprocess.call("cp ./output/wifi.sh /mnt/wifi.sh", shell=True)
    subprocess.call("chmod +x /mnt/wifi.sh", shell=True)
    subprocess.call("cp ./output/pppoe.sh /mnt/pppoe.sh", shell=True)
    subprocess.call("chmod +x /mnt/pppoe.sh", shell=True)
    subprocess.call("cp ./output/mobile.sh /mnt/mobile.sh", shell=True)
    subprocess.call("chmod +x /mnt/hostname.sh", shell=True)
    subprocess.call("cp ./output/de.sh /mnt/de.sh", shell=True)
    subprocess.call("chmod +x /mnt/de.sh", shell=True)
    subprocess.call("cp ./output/lm.sh /mnt/lm.sh", shell=True)
    subprocess.call("chmod +x /mnt/lm.sh", shell=True)
    subprocess.call("cp ./output/video.sh /mnt/video.sh", shell=True)
    subprocess.call("chmod +x /mnt/video.sh", shell=True)
    subprocess.call("cp ./output/ntfs.sh /mnt/ntfs.sh", shell=True)
    subprocess.call("chmod +x /mnt/ntfs.sh", shell=True)
    subprocess.call("cp ./output/cups.sh /mnt/cups.sh", shell=True)
    subprocess.call("chmod +x /mnt/cups.sh", shell=True)
    subprocess.call("cp ./output/grub.sh /mnt/grub.sh", shell=True)
    subprocess.call("chmod +x /mnt/grub.sh", shell=True)
    subprocess.call("cp ./output/update_repo.sh /mnt/update_repo.sh", shell=True)
    subprocess.call("chmod +x /mnt/update_repo.sh", shell=True)

def remove_chroot():
    subprocess.call("rm /mnt/hostname.sh", shell=True)
    subprocess.call("rm /mnt/tz.sh", shell=True)
    subprocess.call("rm /mnt/lang.sh", shell=True)
    subprocess.call("rm /mnt/kbd.sh", shell=True)
    subprocess.call("rm /mnt/nm.sh", shell=True)
    subprocess.call("rm /mnt/dhcp.sh", shell=True)
    subprocess.call("rm /mnt/wifi.sh", shell=True)
    subprocess.call("rm /mnt/pppoe.sh", shell=True)
    subprocess.call("rm /mnt/mobile.sh", shell=True)
    subprocess.call("rm /mnt/de.sh", shell=True)
    subprocess.call("rm /mnt/lm.sh", shell=True)
    subprocess.call("rm /mnt/video.sh", shell=True)
    subprocess.call("rm /mnt/ntfs.sh", shell=True)
    subprocess.call("rm /mnt/cups.sh", shell=True)
    subprocess.call("rm /mnt/grub.sh", shell=True)
    subprocess.call("rm /mnt/update_repo.sh", shell=True)

def pai_prepare(efi):
    #
    # odczyt plików
    #
    config = configparser.ConfigParser()
    config.read("config/config.cfg")
    de = configparser.ConfigParser()
    de.read("config/de.cfg")
    services = configparser.ConfigParser()
    services.read("config/services.cfg")
    video = configparser.ConfigParser()
    video.read("config/video.cfg")
    part = configparser.ConfigParser()
    part.read("config/part.cfg")
    # config
    hostname = config["General"]["hostname"]
    lang = config["General"]["lang"]
    kbd = config["General"]["kbd"]
    tz = config["General"]["tz"]
    # de
    desktop = de["Desktop Environment"]["de"]
    lm = de["Desktop Environment"]["lm"]
    # services
    nm = services["Services"]["nm"]
    dhcp = services["Services"]["dhcp"]
    wifi = services["Services"]["wifi"]
    pppoe = services["Services"]["pppoe"]
    mobile = services["Services"]["mobile"]
    cups = services["Services"]["cups"]
    # video
    v_driver = video["Video"]["driver"]
    # part
    grub = part["Partitioning"]["grub"]
    #
    #   przygotowanie skryptów
    #
    c_hostname(hostname)
    c_timezone(tz)
    c_lang(lang)
    c_kbd(kbd)
    c_nm(nm, desktop)
    c_dhcp(dhcp)
    c_wifi(wifi)
    c_pppoe(pppoe)
    c_mobile(mobile)
    c_de(desktop)
    c_lm(lm)
    c_video(v_driver)
    c_ntfs()
    c_cups(cups)
    c_grub(efi, grub)
    c_update_repo()
    prepare_chroot()



def i_installation(efi, window):
    window["-PROBAR-"].update_bar(0)
    window["-STATUS-"].update("Status: Przygotowanie do instalacji")
    config = configparser.ConfigParser()
    config.read("config/config.cfg")
    services = configparser.ConfigParser()
    services.read("config/services.cfg")
    kernel = config["General"]["kernel"]
    multilib = services["Services"]["multilib"]
    pai_prepare(efi)
    window["-PROBAR-"].update_bar(10)
    window["-STATUS-"].update("Status: Aktualizacja repozytoriów")
    subprocess.call("pacman -Syy --noconfirm --quiet archlinux-keyring", shell=True)
    window["-PROBAR-"].update_bar(20)
    window["-STATUS-"].update("Status: Instalacja systemu - base+kernel - może potrwać kilka minut...")
    if kernel == "stable":
        subprocess.call("pacstrap /mnt base base-devel linux linux-firmware linux-headers sudo nano dialog reflector", shell=True)
    if kernel == "longterm":
        subprocess.call("pacstrap /mnt base base-devel linux-lts linux-firmware linux-lts-headers sudo nano dialog reflector", shell=True)
    if kernel == "zen":
        subprocess.call("pacstrap /mnt base base-devel linux-zen linux-firmware linux-zen-headers sudo nano dialog reflector", shell=True)
    if kernel == "hardened":
        subprocess.call("pacstrap /mnt base base-devel linux-hardened linux-firmware linux-hardened-headers sudo nano dialog reflector", shell=True)
    window["-PROBAR-"].update_bar(40)
    window["-STATUS-"].update("Status: Generowanie pliku fstab")
    subprocess.call("genfstab -U /mnt >> /mnt/etc/fstab", shell=True)
    window["-PROBAR-"].update_bar(45)
    window["-STATUS-"].update("Status: Konfiguracja mirrorlist")
    subprocess.call("cp /etc/pacman.d/mirrorlist /mnt/etc/pacman.d/mirrorlist", shell=True)
    subprocess.call("pacman -Syy", shell=True)
    if multilib == "true":
        window["-PROBAR-"].update_bar(47)
        window["-STATUS-"].update("Status: Konfiguracja repozytorium multilib")
        subprocess.call("echo \"\" >> /mnt/etc/pacman.conf", shell=True)    
        subprocess.call("echo \"[multilib]\" >> /mnt/etc/pacman.conf", shell=True)
        subprocess.call("echo \"Include = /etc/pacman.d/mirrorlist\" >> /mnt/etc/pacman.conf", shell=True)
    window["-PROBAR-"].update_bar(50)
    window["-STATUS-"].update("Status: Aktualizacja repozytoriów")
    subprocess.call("arch-chroot /mnt bash -c \"./update_repo.sh\"", shell=True)
    window["-PROBAR-"].update_bar(51)
    window["-STATUS-"].update("Status: Konfiguracja hostname")
    subprocess.call("arch-chroot /mnt bash -c \"./hostname.sh\"", shell=True)
    window["-PROBAR-"].update_bar(52)
    window["-STATUS-"].update("Status: Konfiguracja strefy czasowej")
    subprocess.call("arch-chroot /mnt bash -c \"./tz.sh\"", shell=True)
    window["-PROBAR-"].update_bar(53)
    window["-STATUS-"].update("Status: Konfiguracja lokalizacji systemowej")
    subprocess.call("arch-chroot /mnt bash -c \"./lang.sh\"", shell=True)
    window["-PROBAR-"].update_bar(54)
    window["-STATUS-"].update("Status: Instalacja Network Manager")
    subprocess.call("arch-chroot /mnt bash -c \"./nm.sh\"", shell=True)
    window["-PROBAR-"].update_bar(60)
    window["-STATUS-"].update("Status: Instalacja usługi DHCP")
    subprocess.call("arch-chroot /mnt bash -c \"./dhcp.sh\"", shell=True)
    window["-PROBAR-"].update_bar(65)
    window["-STATUS-"].update("Status: Instalacja obsługi sieci Wi-Fi")
    subprocess.call("arch-chroot /mnt bash -c \"./wifi.sh\"", shell=True)
    window["-PROBAR-"].update_bar(70)
    window["-STATUS-"].update("Status: Instalacja obsługi sieci PPPoE")
    subprocess.call("arch-chroot /mnt bash -c \"./pppoe.sh\"", shell=True)
    window["-PROBAR-"].update_bar(75)
    window["-STATUS-"].update("Status: Instalacja obsługi sieci komórkowych")
    subprocess.call("arch-chroot /mnt bash -c \"./mobile.sh\"", shell=True)
    window["-PROBAR-"].update_bar(80)
    window["-STATUS-"].update("Status: Instalacja środowiska graficznego")
    subprocess.call("arch-chroot /mnt bash -c \"./de.sh\"", shell=True)
    window["-PROBAR-"].update_bar(85)
    window["-STATUS-"].update("Status: Instalacja menedżera logowania")
    subprocess.call("arch-chroot /mnt bash -c \"./lm.sh\"", shell=True)
    window["-PROBAR-"].update_bar(90)
    window["-STATUS-"].update("Status: Instalacja sterownika wideo")
    subprocess.call("arch-chroot /mnt bash -c \"./video.sh\"", shell=True)
    window["-PROBAR-"].update_bar(91)
    window["-STATUS-"].update("Status: Instalacja obsługi plików NTFS")
    subprocess.call("arch-chroot /mnt bash -c \"./ntfs.sh\"", shell=True)
    window["-PROBAR-"].update_bar(92)
    window["-STATUS-"].update("Status: Instalacja serwera druku CUPS")
    subprocess.call("arch-chroot /mnt bash -c \"./cups.sh\"", shell=True)
    window["-PROBAR-"].update_bar(93)
    window["-STATUS-"].update("Status: Konfiguracja klawiatury")
    subprocess.call("arch-chroot /mnt bash -c \"./kbd.sh\"", shell=True)
    window["-PROBAR-"].update_bar(95)
    window["-STATUS-"].update("Status: Instalacja bootloadera")
    subprocess.call("arch-chroot /mnt bash -c \"./grub.sh\"", shell=True)
    window["-PROBAR-"].update_bar(100)
    window["-STATUS-"].update("Status: Instalacja zakończona!")
    remove_chroot()


def pai_install(efi):
    ans = True
    while ans:
        sg.SetOptions(font=("Liberation Sans", 12), margins=(0, 0))
        sg.theme("Dark")
        logo = [
            [sg.Image("./gfx/small_logo.png")]
        ]
        install = [
            [sg.Text("Instalacja systemu ArchLinux", size=(35, 1))],
            [sg.ProgressBar(100, orientation='h', size=(62, 30), key='-PROBAR-')],
            [sg.Text("", size=(62, 1), key='-STATUS-')]
        ]
        run_installer = [
            [sg.Button("Rozpocznij instalację!", size=(62, 1), pad=((4, 4), (0, 4)), key="btn_run")]
        ]
        gui = [
            [sg.Column(layout=logo)],
            [sg.Column(layout=install)],
            [sg.Column(layout=run_installer)]
        ]
        window = sg.Window("PyArchInstaller", gui, finalize=True, size=(600, 260))
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                ans = False
                break
            if event == "btn_run":
                try:
                    window.Element("btn_run").update(disabled=True)
                    ans = False
                    x = threading.Thread(target=i_installation, args=(efi, window, ))
                    x.start()
                except Exception as e:
                    print(str(e))
        window.close()

