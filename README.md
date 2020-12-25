# code-time

code-time is a python application which runs in the background and tracks how much time you spend coding. This data is
then being stored locally and can be exported as PNG to share it online. The interface between user and program happens
using a tray menu.

![statistics](https://i.ibb.co/vZ14ffZ/code-time-25122020.png)

## Features

* Track coding time
* Tray menu
* Run in background
* Display statistics
* Export statistics as PNG
* Custom user image and username
* Automatically start tracking after login
* Customize colors

## Installation

### macOS

Download the latest release from the Releases section. It includes the executable file called `main`, `config.json` and
two folders called `res` for resources, and a folder called `data` which stores all tracking data. Copy everything and
put it into a folder of your desire.

### Windows

Windows is currently not being supported.

### Linux

Linux is currently not being supported.

## Usage

### Start code-time manually

#### macOS

Run the following bash command.

```bash
<path-to-main-file>/main
```

### Start tracking

code-time works by tracking which application is in the foreground. To add a new application, go to the Activities
section in settings. Click the `ADD NEW ACTIVITY` button to add an application.

![Add activity](https://i.ibb.co/ZKJ9Lvs/Bildschirmfoto-2020-12-25-um-17-12-00.png)

If you bring the desired application into the foreground and then switch back to code-time, the application will show up
in the list and can be added using the `ADD SELECTED ACTIVITY` button.

### Enable autostart

To make autostart run automatically after you logged in into your computer. Go to the Autostart section in the settings.

### Export statistics

In the tray menu, expand statistics and click your desired date. This will open a preview of the statistics and provides
an option to export it as a PNG file.

![statistics preview](https://i.ibb.co/whjdZ1h/Bildschirmfoto-2020-12-25-um-17-33-15.png)

### Change assets

Note that instead of replacing files in the `res` directory, paths to files can be changed in `config.json`.

#### Background image

The background image is being stored in the `res` folder. It is called `default_background.png` and can be replaced with
any image as long as it is 1080x1080.

#### User image

The user image can be changed in the User Image section of the settings or by replacing the `default_user` image in the
`res` folder.

![change user image](https://i.ibb.co/ZGtQRmh/Bildschirmfoto-2020-12-25-um-17-20-48.pngA)


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[GNU](https://choosealicense.com/licenses/gpl-3.0/)

## Note

Icons source: Fontawesome