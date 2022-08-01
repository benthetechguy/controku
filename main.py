import socket
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from requests import get, post
from bs4 import BeautifulSoup
from ssdpy import SSDPClient

class Window(Gtk.Window):
    def __init__(self):
        global device_id
        device_id = ""
        global search_id

        super().__init__(title="Controku")
        self.set_border_width(10)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(420)

        con_grid = Gtk.Grid()
        stack.add_titled(con_grid, "connection", "Connection")

        rem_grid = Gtk.Grid()
        stack.add_titled(rem_grid, "remote", "Remote")

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)

        vbox.pack_start(stack_switcher, True, True, 0)
        vbox.pack_start(stack, True, True, 0)

        button = Gtk.Button.new_with_label("Keyboard")
        button.connect("clicked", self.keyboard)
        rem_grid.attach(button, 0, 0, 2, 1)

        button = Gtk.Button.new_with_label("⏻")
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

        button = Gtk.Button.new_with_label("⏪")
        button.connect("clicked", self.send_button, "Rev")
        rem_grid.attach(button, 0, 5, 1, 1)

        button = Gtk.Button.new_with_label("⏯")
        button.connect("clicked", self.send_button, "Play")
        rem_grid.attach(button, 1, 5, 1, 1)

        button = Gtk.Button.new_with_label("⏩")
        button.connect("clicked", self.send_button, "Fwd")
        rem_grid.attach(button, 2, 5, 1, 1)

        button = Gtk.Button.new_with_label("🔇")
        button.connect("clicked", self.send_button, "VolumeMute")
        rem_grid.attach(button, 0, 6, 1, 1)

        button = Gtk.Button.new_with_label("🔉")
        button.connect("clicked", self.send_button, "VolumeDown")
        rem_grid.attach(button, 1, 6, 1, 1)

        button = Gtk.Button.new_with_label("🔊")
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
        soup = BeautifulSoup(info, "html.parser")
        mode = soup.find('power-mode').string
        if mode == "Ready":
            self.send_button(button, "PowerOn")
        elif mode == "PowerOn":
            self.send_button(button, "PowerOff")
        else:
            print("Current power status not supported!")

    def keyboard(self, button):
        global device_id
        if device_id == "":
            dialog = Dialog(self)
            dialog.run()
            dialog.destroy()
            return

        print("Opened keyboard")

    def discover_devices(self, button, combo, label1, label2):
        global search_id
        search = SSDPClient().m_search("roku:ecp")

        devices = {}
        for device in search:
            id = device['location']
            info = get(id + "/query/device-info").text
            soup = BeautifulSoup(info, "html.parser")
            name = soup.find('user-device-name').string
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
        soup = BeautifulSoup(info, "html.parser")

        list = {}
        list['Name'] = soup.find('user-device-name').string
        list['IP Address'] = device_id[7:-6]
        print(f"Connected to {list['IP Address']} ({list['Name']})")
        list['Model'] = soup.find('friendly-model-name').string
        list['Serial Number'] = soup.find('serial-number').string
        list['Resolution'] = soup.find('ui-resolution').string
        list['Software'] = soup.find('software-version').string
        if soup.find('power-mode').string == "Ready":
            list['Power'] = "Off"
        elif soup.find('power-mode').string == "PowerOn":
            list['Power'] = "On"

        string1 = "\n\n"
        string2 = "\n\n"
        for thing in list:
            string1 += "<b>" + thing + ":</b>\n"
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

window = Window()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()
