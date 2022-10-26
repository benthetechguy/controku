![Banner](images/controku-banner.png#gh-dark-mode-only)
![Banner](images/controku-banner-inverted.png#gh-light-mode-only)
Controku allows you to control Roku devices from your own desktop with
a slick GTK3 interface, written in Python.

![Remote UI](images/remote.png#gh-dark-mode-only)
![Remote UI](images/remote-light.png#gh-light-mode-only)
![Connection UI](images/connect.png#gh-dark-mode-only)
![Connection UI](images/connect-light.png#gh-light-mode-only)

## Dependencies
* PyGObject
* requests
* [appdirs](https://github.com/ActiveState/appdirs)
* [SSDPy](https://github.com/MoshiBin/ssdpy)

### Note for Windows users
SSDPy, the library used to discover Roku devices on the local network,
has [problems on Windows](https://github.com/MoshiBin/ssdpy/issues/82)
that make device discovery impossible on the platform. Windows users
will need to place the Roku's IP address in the command line arguments,
or manually add the device to the cache at
`C:\Users\username\AppData\Local\benthetechguy\controku\Cache\devices.json`
with the syntax `[{'name': 'device name here', 'id': 'http://ip-here:8060'}]`.

## Keyboard Control
Instead of just using the mouse, you also can press the following keys:

| Key on keyboard       | Key sent to Roku device |
| --------------------- | ----------------------- |
| Backspace             | Back                    |
| I                     | Info                    |
| Escape or H           | Home                    |
| Up arrow              | Up                      |
| Down arrow            | Down                    |
| Left arrow            | Left                    |
| Right arrow           | Right                   |
| Enter, Space, O, or S | Select/OK               |
| R                     | Rewind                  |
| F                     | Fast Forward            |
| P                     | Play/Pause              |
| U or ]                | Volume Up               |
| D or [                | Volume Down             |
| M or \                | Mute                    |

**Note**: The arrow keys highlight different buttons in the GUI, and
pressing enter or space can activate one of them. To prevent the
activation of an unintended button like power or home, it's recommended
to use O or S for Select/OK instead of enter or space.
