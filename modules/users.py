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


def pai_users():
    ans = True

    while ans:
        sg.SetOptions(font=("Monospace Regular", 12), margins=(0, 0))
        sg.theme("Dark")
        logo = [
            [sg.Image("./gfx/small_logo.png")]
        ]
        users = [
            [sg.Text("Konfiguracja roota: ", size=(35, 1))],
            [sg.Text("Hasło: ", size=(24, 1)), sg.InputText("", enable_events=True, key="rootpwd", size=(32, 1))],
            [sg.Text("Powtórz hasło: ", size=(24, 1)), sg.InputText("", enable_events=True, key="r_rootpwd", size=(32, 1))],
            [sg.Button("Skonfiguruj hasło roota", size=(56, 1), pad=((4, 4), (0, 4)), key="btn_root", enable_events=True)],
            [sg.Text("Konfiguracja użytkownika: ", size=(35, 1))],
            [sg.Text("Nazwa użytkownika: ", size=(25,1)), sg.InputText("", enable_events=True, key="username", size=(32, 1))],
            [sg.Text("Hasło: ", size=(25,1)), sg.InputText("", enable_events=True, key="userpwd", size=(32, 1))],
            [sg.Text("Powtórz hasło: ", size=(25,1)), sg.InputText("", enable_events=True, key="r_userpwd", size=(32, 1))],
            [sg.Checkbox("Użytkownik z uprawnieniami administratora", key="admin")],
            [sg.Button("Skonfiguruj użytkownika", size=(56, 1), pad=((4, 4), (0, 4)), key="btn_user", enable_events=True)]
        ]
        gui = [
            [sg.Column(layout=logo)],
            [sg.Column(layout=users)]
        ]
        window = sg.Window("PyArchInstaller", gui, finalize=True, size=(600, 520), location=(100, 100))
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                ans = False
                break
            if event == "btn_root":
                try:
                    if values["rootpwd"] == values["r_rootpwd"]:
                        setup = open("output/root_pwd.sh", "a")
                        setup.write('#!/bin/bash\n')
                        setup.write('echo "' + "root" + ':' + values["rootpwd"] + '" | chpasswd\n')
                        setup.write('exit\n')
                        setup.close()    
                        subprocess.call("cp ./output/root_pwd.sh /mnt/root_pwd.sh", shell=True)
                        subprocess.call("chmod +x /mnt/root_pwd.sh", shell=True)
                        subprocess.call("arch-chroot /mnt bash -c \"./root_pwd.sh\"", shell=True)
                        subprocess.call("rm /mnt/root_pwd.sh", shell=True)
                    else:
                        print("Błąd! Hasła nie są identyczne!")
                except Exception as e:
                    print(str(e))
                break
            if event == "btn_user":
                try:
                    if values["userpwd"] == values["r_userpwd"]:
                        setup = open("output/user_pwd.sh", "a")
                        setup.write('#!/bin/bash\n')
                        if values["admin"]:
                            setup.write('useradd -m -G sys,log,network,floppy,scanner,power,rfkill,users,video,storage,optical,lp,audio,wheel,adm -s /bin/bash ' + values["username"] + '\n')
                        else:
                            setup.write('useradd -m -G sys,log,network,floppy,scanner,power,rfkill,users,video,storage,optical,lp,audio,adm -s /bin/bash ' + values["username"] + '\n')
                        setup.write('echo "' + values["username"] + ':' + values["userpwd"] + '" | chpasswd\n')
                        setup.write('exit\n')
                        setup.close()
                        subprocess.call("cp ./output/user_pwd.sh /mnt/user_pwd.sh", shell=True)
                        subprocess.call("chmod +x /mnt/user_pwd.sh", shell=True)
                        subprocess.call("arch-chroot /mnt bash -c \"./user_pwd.sh\"", shell=True)
                        subprocess.call("rm /mnt/user_pwd.sh", shell=True)
                    else:
                        print("Błąd! Hasła nie są identyczne!")
                except Exception as e:
                    print(str(e))
                break
        window.close()
