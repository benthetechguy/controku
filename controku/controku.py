from requests import get, post
from ssdpy import SSDPClient
from typing import Optional
from urllib.parse import quote
from xml.etree import ElementTree

def discover_devices() -> list:
    """
    Discover Roku devices on the local network.

    :return: A list of dicts containing the name and IP address of each device found.
    """
    search = SSDPClient().m_search("roku:ecp")

    devices = []
    for device in search:
        ip = device['location'][7:-6]

        try:
            info = get(f"http://{ip}:8060/query/device-info").text
        except:
            raise ConnectionError("Couldn't connect to Roku device at {ip}.")

        tree = ElementTree.fromstring(info)
        name = tree.findtext('user-device-name')
        devices.append({"name": name, "ip": ip})

    return devices

def get_device(ip: str) -> dict:
    """
    Get information about a Roku device.

    :param ip: IP address of the device.
    :type ip: str

    :return: A dict containing the device's name, IP address, MAC address,
             user-set location, model, serial number, UDN, current resolution,
             OS version, power state, whether developer mode is enabled or not,
             whether the device is a Smart TV or a just a Roku stick/box,
             whether or not it supports Private Listening, and, if so, whether
             headphones are connected or not.
    """
    try:
        info = get(f"http://{ip}:8060/query/device-info").text
    except:
        raise ConnectionError("Couldn't connect to Roku device at {ip}.")

    tree = ElementTree.fromstring(info)
    device = {}

    device['name'] = tree.findtext('user-device-name')
    device['ip'] = ip
    device['location'] = tree.findtext('user-device-location')

    match tree.findtext('power-mode'):
        case "Ready":
            device['power'] = False
        case "PowerOn":
            device['power'] = True

    device['model'] = tree.findtext('friendly-model-name')
    device['serial'] = tree.findtext('serial-number')
    device['udn'] = tree.findtext('udn')
    device['resolution'] = tree.findtext('ui-resolution')
    device['mac'] = tree.findtext('wifi-mac')
    device['software'] = tree.findtext('software-version')
    device['tv'] = tree.findtext('is-tv') == "true"
    device['stick'] = tree.findtext('is-stick') == "true"
    device['devmode'] = tree.findtext('developer-enabled') == "true"
    device['netsound'] = tree.findtext('supports-private-listening') == "true"
    device['headphones'] = tree.findtext('headphones-connected') == "true"

    return device

def send_key(ip: str, key: str):
    """
    Send a keypress to a Roku device.

    :param ip: IP address of the device.
    :type ip: str

    :param key: Key to send to the device. Common values are seen here: https://developer.roku.com/docs/developer-program/debugging/external-control-api.md#keypress-key-values
    :type key: str
    """
    try:
        post(f"http://{ip}:8060/keypress/{key}")
    except:
        raise ConnectionError("Couldn't connect to Roku device at {ip}.")

def toggle_power(ip: str):
    """
    Turn a Roku device on or off.

    :param ip: IP address of the device.
    :type ip: str
    """
    try:
        info = get(f"http://{ip}:8060/query/device-info").text
    except:
        raise ConnectionError("Couldn't connect to Roku device at {ip}.")

    tree = ElementTree.fromstring(info)
    mode = tree.findtext('power-mode')
    match mode:
        case "Ready":
            send_key(ip, "PowerOn")
        case "PowerOn":
            send_key(ip, "PowerOff")
        case _:
            raise ValueError("Roku is in unknown power state.")

def search(ip: str, keyword: str, title: Optional[str] = None, type: Optional[str] = None, tmsid: Optional[str] = None, season: Optional[int] = None, unavailable: Optional[bool] = None, matchany: Optional[bool] = None, providerid: Optional[str] = None, provider: Optional[str] = None, launch: Optional[bool] = None):
    """
    Run a search with the given parameters on a Roku device.

    :param ip: IP address of the device.
    :type ip: str

    :param keyword: The content title, channel name, person name, or keyword to be searched.
    :type keyword: str

    :param title: The exact content title or channel/person name to be matched (case-insensitive).
    :type title: Optional[str]

    :param type: What is being searched for; one of "movie", "tv-show", "person", "channel", or "game".
    :type type: Optional[str]

    :param tmsid: TMS ID for a movie, TV show, or person.
    :type tmsid: Optional[str]

    :param season: Season number of TV show to be searched.
    :type season: Optional[int]

    :param unavailable: Allow search results to include upcoming content that is not currently available on Roku.
    :type unavailable: Optional[bool]

    :param matchany: If multiple results match the query, automatically select the first one.
    :type matchany: Optional[bool]

    :param providerid: One or more Roku channel IDs specifying the preferred content provider.
    :type providerid: Optional[str]

    :param provider: One or more Roku channel titles specifying the preferred content provider.
    :type provider: Optional[str]

    :param launch: Automatically launch the channel in which content was found.
    :type launch: Optional[bool]
    """
    options = ["keyword", "title", "type", "tmsid", "season", "unavailable", "matchany", "providerid", "provider", "launch"]
    selected_options = []
    for option in options:
        if locals()[option] is not None:
            if option == "type":
                if type not in ["movie", "tv-show", "person", "channel", "game"]:
                    raise ValueError("`type` must be one of 'movie', 'tv-show', 'person', 'channel', or 'game'.")

            selected_options.append({"name": option, "value": locals()[option]})

    query = ""
    for option in selected_options:
        if option['value'] == True:
            option['value'] == "true"
        elif option['value'] == False:
            option['value'] == "false"

        query += f"{option['name']}={option['value']}&"

    query = quote(query[:-1], safe="/=&")
    try:
        post(f"http://{ip}:8060/search/browse?{query}")
    except:
        raise ConnectionError("Couldn't connect to Roku device at {ip}.")

def get_tv_channels(ip: str) -> list:
    """
    Get a list of the live TV channels available on a Roku device.

    :param ip: IP address of the device.
    :type ip: str

    :return: A list of dicts describing each of the live TV channels
             the device has available. They contain the name, number,
             type (analog vs digital, antenna vs cable), the real
             physical channel number (different from the presented
             "virtual" channel number), and whether or not the user has
             hidden the channel or listed it as a favorite.
    """
    try:
        info = get(f"http://{ip}:8060/query/device-info").text
    except:
        raise ConnectionError("Couldn't connect to Roku device at {ip}.")

    infotree = ElementTree.fromstring(info)
    if infotree.findtext('is-tv') != "true":
        raise ValueError("This Roku device is not a TV.")

    try:
        xml = get(f"http://{ip}:8060/query/tv-channels").text
    except:
        raise ConnectionError("Couldn't connect to Roku device at {ip}.")

    tree = ElementTree.fromstring(xml)
    channels = []
    for channel in tree:
        name = channel.findtext('name')
        number = channel.findtext('number')
        type = channel.findtext('type')
        realchannel = channel.findtext('physical-channel')
        hidden = channel.findtext('user-hidden')
        favorite = channel.findtext('user-favorite')
        channels.append({"name": name, "number": number, "type": type, "channel": realchannel, "hidden": hidden, "favorite": favorite})

    return channels

def get_active_tv_channel(ip: str) -> dict:
    """
    Get a Roku device's active live TV channel; this channel is either
    currently playing, or it was the last live channel played.

    :param ip: IP address of the device.
    :type ip: str

    :return: A dict describing the current active channel. It contains
             the channel's name, number, type, its real physical
             channel number (different from the presented "virtual"
             channel number), whether or not the user has marked it as
             hidden or favorite, its resolution, whether or not it's
             currently playing, and the title, description, and rating
             of its current program.
    """
    try:
        info = get(f"http://{ip}:8060/query/device-info").text
    except:
        raise ConnectionError("Couldn't connect to Roku device at {ip}.")

    infotree = ElementTree.fromstring(info)
    if infotree.findtext('is-tv') != "true":
        raise ValueError("This Roku device is not a TV.")

    try:
        xml = get(f"http://{ip}:8060/query/tv-active-channel").text
    except:
        raise ConnectionError("Couldn't connect to Roku device at {ip}.")

    tree = ElementTree.fromstring(xml)[0]
    channel = {}
    channel['name'] = tree.findtext('name')
    channel['number'] = tree.findtext('number')
    channel['type'] = tree.findtext('type')
    channel['channel'] = tree.findtext('physical-channel')
    channel['hidden'] = tree.findtext('user-hidden')
    channel['favorite'] = tree.findtext('user-favorite')
    channel['active'] = tree.findtext('active-input') == "true"

    match tree.findtext('signal-state'):
        case "valid":
            channel['signal'] = True
        case "none":
            channel['signal'] = False

    channel['resolution'] = tree.findtext('signal-mode')
    channel['title'] = tree.findtext('program-title')
    channel['description'] = tree.findtext('program-description')
    channel['rating'] = tree.findtext('program-ratings')
    channel['captions'] = tree.findtext('program-has-cc') == "true"

    return channel
