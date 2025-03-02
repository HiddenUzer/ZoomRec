**Overview**
[Latest Version](https://github.com/HiddenUzer/ZoomRec/releases/tag/bot)

ZoomRec 1.2.0 is an automation tool that allows users to automatically join Zoom meetings at scheduled times, input credentials, and record the session for a set duration. The tool provides a user-friendly GUI interface to configure meeting details, schedule times, and find button coordinates for seamless automation.

**Features**

1.Automated Zoom Joining: Opens Zoom, enters meeting details, and joins automatically.

2.Recording Functionality: Starts and stops screen recording with Alt+F9 (Nvidia GeForce Experience required)

3.Scheduled Meetings: Checks at custom seconds and joins at the custom scheduled time.

4.GUI Interface: Modify meeting details, schedules, and button positions easily.

5.Auto Button locator: Automatically detects and saves button coordinates

Configurable Settings: Stores meeting details, schedule, and button positions in config.json.

**Installation**

1. Download the Executable
2. Ensure ZoomRec.exe and config.json are in the same folder.
3.Run the Application
4.Configure the Settings
5.Set the Zoom Path (path to Zoom.exe). Example - "C:\\Users\\12345\\AppData\\Roaming\\Zoom\\bin_00\\Zoom.exe"
6. Locate the Join Button using the auto locator. 

**Troubleshooting**

"config.json not found" Error: Ensure config.json is in the same folder as the .exe.

Zoom Fails to Open: Verify the Zoom.exe path in the settings.

Incorrect Button Clicks: Use "Locate Join Button" to update the coordinates.

Meeting Not Starting on Schedule: Check if the current time matches the schedule format (HH:MM).

**Credits**
Developed by HiddenUzer 

**License**
This software is open-source and distributed under the MIT License.
