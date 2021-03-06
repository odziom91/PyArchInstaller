###
###
###  PyArchInstaller
###  (c)2021 - created by OdzioM
###
###

import gettext
import os
import configparser
import subprocess
from PySimpleGUI import PySimpleGUI as sg

def pai_mount(lang, part, size, fstype):
    localedir = './locale'
    translate = gettext.translation('part', localedir, languages=[lang], fallback=True)
    translate.install()
    _ = translate.gettext
    mp = open("./lists/mountpoints.gen", "r").read().split("\n")
    ans = True
    while ans:
        sg.SetOptions(font=("Monospace Regular", 12), margins=(0, 0))
        sg.theme("Dark")
        wnd = [
            [sg.Text(_("Choosed partition:") + part)],
            [sg.Text(_("Partition size:") + size)],
            [sg.Text(_("Partition type:") + fstype)],
            [sg.Text(_("Choose mountpoint:"), size=(55, 1))],
            [sg.Combo(values=mp, enable_events=True, key="mountpoint", size=(30, 1))],
        ]
        save_settings = [
            [sg.Button(_("Mount"), size=(10, 1), pad=((4, 4), (0, 4)), key="btn_mount"), sg.Button(_("Cancel"), size=(10, 1), pad=((4, 4), (0, 4)), key="btn_cancel")]
        ]
        gui = [
            [sg.Column(layout=wnd)],
            [sg.Column(layout=save_settings)]
        ]
        window = sg.Window("PyArchInstaller", gui, finalize=True, size=(320, 200), location=(100, 100))
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "btn_cancel":
                ans = False
                break
            if event == "btn_mount":
                try:
                    ans = False
                    if values["mountpoint"] == "swap":
                        subprocess.call("swapon " + part, shell=True)
                    else:
                        subprocess.call("mkdir -p /mnt" + values["mountpoint"], shell=True)
                        subprocess.call("mount " + part + " /mnt" + values["mountpoint"], shell=True)
                    break
                except IndexError as e:
                    print("Nie wybrano partycji z listy.")
        window.close()


def pai_umount(mountpoint):
    try:
        subprocess.call("umount " + mountpoint, shell=True)
    except Exception as e:
        print(str(e))
        

def pai_partitioning(lang):
    localedir = './locale'
    translate = gettext.translation('part', localedir, languages=[lang], fallback=True)
    translate.install()
    _ = translate.gettext
    lsblk = subprocess.check_output("lsblk -np --output PATH,SIZE,FSTYPE,TYPE,MOUNTPOINT", shell=True).decode("utf-8").splitlines()
    lsblk_grub = subprocess.check_output("lsblk -npd --output PATH,MODEL,SIZE", shell=True).decode("utf-8").splitlines()
    part = []
    grub_disk = []
    for line in lsblk:
        if "part" in line:
            part.append(line)
    for line in lsblk_grub:
        if ("/dev/sr" not in line) and ("/dev/loop" not in line):
            grub_disk.append(line)
    ans = True
    while ans:
        sg.SetOptions(font=("Monospace Regular", 12), margins=(0, 0))
        sg.theme("Dark")
        logo = [
            [sg.Image("./gfx/small_logo.png")]
        ]
        gparted = [
            [sg.Text(_("Create or modify partition on disks with GParted:"), size=(55, 1))],
            [sg.Button(_("Run GParted"), size=(56, 1), pad=((4, 4), (0, 4)), key="btn_gparted")],
        ]
        mount = [
            [sg.Text(_("Partitions:"), size=(35, 1))],
            [sg.Listbox(part,  size=(57, 7), font=("Monospace Regular", 12), enable_events=True, key="partitions")],
            [sg.Button(_("Mount"), size=(26, 1), pad=((4, 4), (0, 4)), key="btn_mount"), sg.Button(_("Unmount"), size=(26, 1), pad=((4, 4), (0, 4)), key="btn_umount")]
        ]
        if int(subprocess.check_output("ls /sys/firmware/efi/efivars | wc -l", shell=True)) > 1:
            grub = [
                [sg.Text(_("UEFI installation detected."), size=(55, 1))],
                [sg.Text(_("EFI partition not mounted!"), key="efi", size=(55, 1), text_color="red")]
            ]
        else:
            grub = [
                [sg.Text(_("Choose disk for GRUB installation:"), size=(55, 1))],
                [sg.Combo(values=grub_disk, enable_events=True, key="grub", size=(55, 1))]
            ]
        exit_settings = [
            [sg.Button(_("Save settings"), size=(56, 1), pad=((4, 4), (0, 4)), key="btn_save")]
        ]
        gui = [
            [sg.Column(layout=logo)],
            [sg.Column(layout=gparted)],
            [sg.Column(layout=mount)],
            [sg.Column(layout=grub)],
            [sg.Column(layout=exit_settings)]
        ]
        window = sg.Window("PyArchInstaller", gui, finalize=True, size=(600, 520), location=(100, 100))
        while True:
            if int(subprocess.check_output("ls /sys/firmware/efi/efivars | wc -l", shell=True)) > 1:
                check_bootpart = subprocess.check_output("lsblk -np --output PATH,MOUNTPOINT", shell=True).decode("utf-8").splitlines()
                for line in check_bootpart:
                    if ("/mnt/boot" in line) or ("/mnt/boot/efi" in line) and ("vfat" in line):
                        window.Element("efi").update(value=_("EFI partition mounted."), text_color="white")
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                ans = False
                break
            if event == "btn_gparted":
                try:
                    subprocess.run(["gparted"])
                    lsblk = subprocess.check_output("lsblk -np --output PATH,SIZE,FSTYPE,TYPE,MOUNTPOINT", shell=True).decode("utf-8").splitlines()
                    part = []
                    for line in lsblk:
                        if "part" in line:
                            part.append(line)
                    window.Element("partitions").update(values=part)
                except Exception as e:
                    print(str(e))
            if event == "btn_mount":
                try:
                    sel_part_split = str(values["partitions"][0]).split()
                    pai_mount(lang, sel_part_split[0], sel_part_split[1], sel_part_split[2])
                    lsblk = subprocess.check_output("lsblk -np --output PATH,SIZE,FSTYPE,TYPE,MOUNTPOINT", shell=True).decode("utf-8").splitlines()
                    part = []
                    for line in lsblk:
                        if "part" in line:
                            part.append(line)
                    window.Element("partitions").update(values=part)
                except Exception as e:
                    print(str(e))
            if event == "btn_umount":
                try:
                    sel_part_split = str(values["partitions"][0]).split()
                    pai_umount(sel_part_split[4])
                    lsblk = subprocess.check_output("lsblk -np --output PATH,SIZE,FSTYPE,TYPE,MOUNTPOINT", shell=True).decode("utf-8").splitlines()
                    part = []
                    for line in lsblk:
                        if "part" in line:
                            part.append(line)
                    window.Element("partitions").update(values=part)
                except IndexError as e:
                    print("Nie wybrano partycji z listy.")
            if event == "btn_save":
                try:
                    ans = False
                    if int(subprocess.check_output("ls /sys/firmware/efi/efivars | wc -l", shell=True)) > 1:
                        part_grub = 'efi'
                    else:
                        sel_grub_split = str(values["grub"]).split()
                        part_grub = sel_grub_split[0]
                    config = configparser.ConfigParser()
                    config.read("config/settings.cfg")
                    config.set('Grub', 'grub', part_grub)
                    config.set('Summary', 'Grub', 'True')
                    with open('config/settings.cfg', 'w') as configfile:
                        config.write(configfile)
                except Exception as e:
                    print(str(e))
                break
                
        window.close()
