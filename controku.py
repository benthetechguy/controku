#!/usr/bin/env python3

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from requests import get, post
from ssdpy import SSDPClient
from sys import argv
from urllib.parse import quote
from xml.etree import ElementTree

class Window(Gtk.Window):
    def __init__(self):
        global device_id
        global search_id

        if len(argv) >= 2:
            device_id = f"http://{argv[1]}:8060"
        else:
            device_id = ""

        super().__init__(title="Controku")
        self.set_border_width(10)

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

        button = Gtk.Button.new_with_label("Keyboard")
        button.connect("clicked", self.keyboard)
        rem_grid.attach(button, 0, 0, 2, 1)

        button = Gtk.Button.new_from_icon_name("system-shutdown-symbolic", 4)
        button.connect("clicked", self.power)
        rem_grid.attach(button, 2, 0, 1, 1)

        button = Gtk.Button.new_with_label("Back")
        button.connect("clicked", self.send_button, "Back")
        rem_grid.attach(button, 0, 1, 1, 1)

        button = Gtk.Button.new_with_label("*")
        button.connect("clicked", self.send_button, "Info")
        rem_grid.attach(button, 1, 1, 1, 1)

        button = Gtk.Button.new_with_label("Home")
        button.connect("clicked", self.send_button, "Home")
        rem_grid.attach(button, 2, 1, 1, 1)

        button = Gtk.Button.new_with_label("▲")
        button.connect("clicked", self.send_button, "Up")
        rem_grid.attach(button, 1, 2, 1, 1)

        button = Gtk.Button.new_with_label("▼")
        button.connect("clicked", self.send_button, "Down")
        rem_grid.attach(button, 1, 4, 1, 1)

        button = Gtk.Button.new_with_label("◀")
        button.connect("clicked", self.send_button, "Left")
        rem_grid.attach(button, 0, 3, 1, 1)

        button = Gtk.Button.new_with_label("▶")
        button.connect("clicked", self.send_button, "Right")
        rem_grid.attach(button, 2, 3, 1, 1)

        button = Gtk.Button.new_with_label("OK")
        button.connect("clicked", self.send_button, "Select")
        rem_grid.attach(button, 1, 3, 1, 1)

        button = Gtk.Button.new_from_icon_name("media-seek-backward-symbolic", 4)
        button.connect("clicked", self.send_button, "Rev")
        rem_grid.attach(button, 0, 5, 1, 1)

        button = Gtk.Button.new_with_label("⏯")
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

        hbox = Gtk.Box(spacing=6)
        con_grid.attach(hbox, 0, 0, 3, 1)

        combo = Gtk.ComboBoxText()
        combo.set_entry_text_column(0)
        hbox.pack_start(combo, True, True, 0)

        label1 = Gtk.Label()
        con_grid.attach(label1, 0, 1, 1, 6)

        label2 = Gtk.Label()
        con_grid.attach(label2, 1, 1, 2, 6)

        button = Gtk.Button.new_with_label("Search for Devices")
        search_id = button.connect("clicked", self.discover_devices, combo, label1, label2)
        hbox.pack_start(button, True, True, 0)

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
                value = "Back"
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
            case 91:
                value = "VolumeDown"
            case 93:
                value = "VolumeUp"

        self.send_button(self, value)

    def discover_devices(self, button, combo, label1, label2):
        global search_id
        search = SSDPClient().m_search("roku:ecp")

        devices = {}
        for device in search:
            id = device['location']
            info = get(id + "/query/device-info").text
            tree = ElementTree.fromstring(info)
            name = tree.findtext('user-device-name')
            print(f"Found {name} at {id[7:-6]}")
            combo.append(id, name)
        combo.set_active(0)
        button.set_label("Connect")
        button.disconnect(search_id)
        button.connect("clicked", self.connect_device, combo, label1, label2)

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
        list['Resolution'] = tree.findtext('ui-resolution')
        list['Software'] = tree.findtext('software-version')
        if tree.findtext('power-mode') == "Ready":
            list['Power'] = "Off"
        elif tree.findtext('power-mode') == "PowerOn":
            list['Power'] = "On"

        string1 = "\n\n"
        string2 = "\n\n"
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
