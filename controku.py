#!/usr/bin/env python3

import gi
import sys
gi.require_version("Gtk", "3.0")
from appdirs import user_cache_dir
from gi.repository import Gtk
from json import dump, load
from os import path, makedirs
from requests import get, post
from ssdpy import SSDPClient
from urllib.parse import quote
from xml.etree import ElementTree

class Window(Gtk.Window):
    def __init__(self):
        global device_id
        global cached_devices
        global cache_path

        if len(sys.argv) >= 2:
            device_id = f"http://{sys.argv[1]}:8060"
        else:
            device_id = ""

        cache_path = user_cache_dir("controku", "benthetechguy")
        makedirs(cache_path, exist_ok=True)
        if path.isfile(path.join(cache_path, "devices.json")):
            with open(path.join(cache_path, "devices.json")) as file:
                cached_devices = load(file)
        else:
            cached_devices = []

        super().__init__(title="Controku")
        self.set_border_width(10)

        # pyinstaller puts relative path in _MEIPASS; detect if running under pyinstaller
        try:
            basepath = sys._MEIPASS
        except Exception:
            basepath = path.abspath(".")

        Gtk.IconTheme.get_default().append_search_path(path.join(basepath, "images"))
        self.set_icon_from_file(path.join(basepath, "images/controku.png"))

        con_grid = Gtk.Grid()
        rem_grid = Gtk.Grid()
        rem_grid.connect("key-press-event", self.keypress)
        if device_id == "":
            vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
            self.add(vbox)

            stack = Gtk.Stack()
            stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
            stack.set_transition_duration(420)

            stack.add_titled(con_grid, "connection", "Connection")
            stack.add_titled(rem_grid, "remote", "Remote")

            stack_switcher = Gtk.StackSwitcher()
            stack_switcher.set_stack(stack)

            vbox.pack_start(stack_switcher, True, True, 0)
            vbox.pack_start(stack, True, True, 0)
        else:
            self.add(rem_grid)

        button = Gtk.Button.new_from_icon_name("input-keyboard-symbolic", 4)
        button.connect("clicked", self.keyboard)
        rem_grid.attach(button, 0, 0, 1, 1)

        button = Gtk.Button.new_from_icon_name("refresh-symbolic", 4)
        button.connect("clicked", self.send_button, "InstantReplay")
        rem_grid.attach(button, 1, 0, 1, 1)

        button = Gtk.Button.new_from_icon_name("system-shutdown-symbolic", 4)
        button.connect("clicked", self.power)
        rem_grid.attach(button, 2, 0, 1, 1)

        button = Gtk.Button.new_with_label("Back")
        button.connect("clicked", self.send_button, "Back")
        rem_grid.attach(button, 0, 1, 1, 1)

        button = Gtk.Button.new_with_label("Info")
        button.connect("clicked", self.send_button, "Info")
        rem_grid.attach(button, 1, 1, 1, 1)

        button = Gtk.Button.new_with_label("Home")
        button.connect("clicked", self.send_button, "Home")
        rem_grid.attach(button, 2, 1, 1, 1)

        button = Gtk.Button.new_from_icon_name("media-up-symbolic", 4)
        button.connect("clicked", self.send_button, "Up")
        rem_grid.attach(button, 1, 2, 1, 1)

        button = Gtk.Button.new_from_icon_name("media-down-symbolic", 4)
        button.connect("clicked", self.send_button, "Down")
        rem_grid.attach(button, 1, 4, 1, 1)

        button = Gtk.Button.new_from_icon_name("media-left-symbolic", 4)
        button.connect("clicked", self.send_button, "Left")
        rem_grid.attach(button, 0, 3, 1, 1)

        button = Gtk.Button.new_from_icon_name("media-right-symbolic", 4)
        button.connect("clicked", self.send_button, "Right")
        rem_grid.attach(button, 2, 3, 1, 1)

        button = Gtk.Button.new_with_label("OK")
        button.connect("clicked", self.send_button, "Select")
        rem_grid.attach(button, 1, 3, 1, 1)

        button = Gtk.Button.new_from_icon_name("media-seek-backward-symbolic", 4)
        button.connect("clicked", self.send_button, "Rev")
        rem_grid.attach(button, 0, 5, 1, 1)

        button = Gtk.Button.new_from_icon_name("media-play-pause-symbolic", 4)
        button.connect("clicked", self.send_button, "Play")
        rem_grid.attach(button, 1, 5, 1, 1)

        button = Gtk.Button.new_from_icon_name("media-seek-forward-symbolic", 4)
        button.connect("clicked", self.send_button, "Fwd")
        rem_grid.attach(button, 2, 5, 1, 1)

        button = Gtk.Button.new_from_icon_name("audio-volume-muted-symbolic", 4)
        button.connect("clicked", self.send_button, "VolumeMute")
        rem_grid.attach(button, 0, 6, 1, 1)

        button = Gtk.Button.new_from_icon_name("audio-volume-low-symbolic", 4)
        button.connect("clicked", self.send_button, "VolumeDown")
        rem_grid.attach(button, 1, 6, 1, 1)

        button = Gtk.Button.new_from_icon_name("audio-volume-high-symbolic", 4)
        button.connect("clicked", self.send_button, "VolumeUp")
        rem_grid.attach(button, 2, 6, 1, 1)

        combo = Gtk.ComboBoxText()
        combo.set_entry_text_column(0)
        con_grid.attach(combo, 0, 1, 2, 1)
        for device in cached_devices:
            combo.append(device['id'], device['name'])
        combo.set_active(0)

        button = Gtk.Button.new_with_label("Search for Devices")
        button.connect("clicked", self.discover_devices, combo)
        con_grid.attach(button, 0, 0, 2, 1)

        button = Gtk.Button.new_with_label("Remove Device")
        button.connect("clicked", self.remove_device, combo)
        con_grid.attach(button, 0, 2, 2, 1)

        label1 = Gtk.Label()
        con_grid.attach(label1, 0, 3, 1, 4)

        label2 = Gtk.Label()
        con_grid.attach(label2, 1, 3, 2, 4)

        button = Gtk.Button.new_with_label("Connect")
        button.connect("clicked", self.connect_device, combo, label1, label2)
        con_grid.attach(button, 2, 1, 1, 1)

    def send_button(self, button, value):
        global device_id
        if device_id == "":
            dialog = Dialog(self)
            dialog.run()
            dialog.destroy()
            return

        post(device_id + "/keypress/" + value)
        print("Sent " + value)

    def power(self, button):
        global device_id
        if device_id == "":
            dialog = Dialog(self)
            dialog.run()
            dialog.destroy()
            return

        info = get(device_id + "/query/device-info").text
        tree = ElementTree.fromstring(info)
        mode = tree.findtext('power-mode')
        match mode:
            case "Ready":
                self.send_button(button, "PowerOn")
            case "PowerOn":
                self.send_button(button, "PowerOff")
            case _:
                print("Current power status not supported!")

    def keyboard(self, button):
        global device_id
        if device_id == "":
            dialog = Dialog(self)
            dialog.run()
            dialog.destroy()
            return

        keyboard = Keyboard(self)
        print("Opened keyboard")
        keyboard.run()
        keyboard.destroy()

    def keypress(self, widget, key):
        match key.keyval:
            case 65288:
                value = "Back"
            case 65307:
                value = "Home"
            case 104:
                value = "Home"
            case 105:
                value = "Info"
            case 65361:
                value = "Left"
            case 65362:
                value = "Up"
            case 65363:
                value = "Right"
            case 65364:
                value = "Down"
            case 65293:
                value = "Select"
            case 32:
                value = "Select"
            case 111:
                value = "Select"
            case 115:
                value = "Select"
            case 114:
                value = "Rev"
            case 112:
                value = "Play"
            case 102:
                value = "Fwd"
            case 109:
                value = "VolumeMute"
            case 92:
                value = "VolumeMute"
            case 100:
                value = "VolumeDown"
            case 91:
                value = "VolumeDown"
            case 117:
                value = "VolumeUp"
            case 93:
                value = "VolumeUp"

        self.send_button(self, value)

    def discover_devices(self, button, combo):
        global cached_devices
        global cache_path
        search = SSDPClient().m_search("roku:ecp")

        devices = {}
        for device in search:
            id = device['location'][:-1]
            info = get(id + "/query/device-info").text
            tree = ElementTree.fromstring(info)
            name = tree.findtext('user-device-name')
            print(f"Found {name} at {id[7:-6]}")

            if {"name": name, "id": id} not in cached_devices:
                cached_devices.append({"name": name, "id": id})
                combo.append(id, name)

        combo.set_active(0)
        with open(path.join(cache_path, "devices.json"), "w") as file:
            dump(cached_devices, file)

    def remove_device(self, button, combo):
        global cached_devices
        global cache_path

        for i in range(len(cached_devices)):
            if cached_devices[i]['name'] == combo.get_active_text() and cached_devices[i]['id'] == combo.get_active_id():
                del cached_devices[i]
                print(f"Removed {combo.get_active_text()} from list")
                break
        with open(path.join(cache_path, "devices.json"), "w") as file:
            dump(cached_devices, file)

        combo.remove(combo.get_active())
        combo.set_active(0)

    def connect_device(self, button, combo, label1, label2):
        global device_id
        device_id = combo.get_active_id()
        info = get(device_id + "/query/device-info").text
        tree = ElementTree.fromstring(info)

        list = {}
        list['Name'] = tree.findtext('user-device-name')
        list['IP Address'] = device_id[7:-6]
        print(f"Connected to {list['IP Address']} ({list['Name']})")
        list['Model'] = tree.findtext('friendly-model-name')
        list['Serial Number'] = tree.findtext('serial-number')
        if tree.findtext('power-mode') == "Ready":
            list['Power'] = "Off"
        elif tree.findtext('power-mode') == "PowerOn":
            list['Power'] = "On"

        string1 = "\n"
        string2 = "\n"
        for thing in list:
            string1 += f"<b>{thing}:</b>\n"
            string2 += list[thing] + "\n"
        label1.set_markup(string1)
        label2.set_markup(string2)

class Dialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="No Connection", transient_for=parent, flags=0)

        self.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.set_default_size(250, 120)
        label = Gtk.Label(label="\nYou need to connect to a device\nbefore you can use the remote.")

        box = self.get_content_area()
        box.add(label)
        self.show_all()

class Keyboard(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Roku Keyboard", transient_for=parent, flags=0)

        entry = Gtk.Entry()
        entry.connect("key-press-event", self.send_key, parent)

        box = self.get_content_area()
        box.add(entry)
        self.show_all()

    def send_key(self, entry, key, parent):
        if quote(key.string) == "%08":
            parent.send_button(parent, "Backspace")
        elif quote(key.string) == "%0D":
            parent.send_button(parent, "Enter")
            self.destroy()
        elif quote(key.string) != "":
            parent.send_button(parent, "Lit_" + quote(key.string))

window = Window()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()
