; setup.iss - Inno Setup script for Kitty Assistant

[Setup]
AppName=Kitty Assistant
AppVersion=1.0.0
DefaultDirName={pf}\Kitty Assistant
DefaultGroupName=Kitty Assistant
OutputBaseFilename=setup_KittyAssistant
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
; Include everything PyInstaller output (adjust path if needed)
Source: "dist\KittyAssistant\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs
; Include custom shortcut icon (place kitty_icon.ico in project root)
Source: "kitty_icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Main Start Menu entry
Name: "{group}\Kitty Assistant"; Filename: "{app}\KittyAssistant.exe"; IconFilename: "{app}\kitty_icon.ico"
; Desktop shortcut (task-controlled)
Name: "{commondesktop}\Kitty Assistant"; Filename: "{app}\KittyAssistant.exe"; IconFilename: "{app}\kitty_icon.ico"; Tasks: desktopicon
; Startup folder shortcut (task-controlled for autostart)
Name: "{userstartup}\Kitty Assistant"; Filename: "{app}\KittyAssistant.exe"; IconFilename: "{app}\kitty_icon.ico"; Tasks: autostart

[Tasks]
Name: desktopicon; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"; Flags: unchecked
Name: autostart; Description: "Launch Kitty Assistant at Windows &startup"; GroupDescription: "Additional icons:"; Flags: unchecked

[Run]
Filename: "{app}\KittyAssistant.exe"; Description: "Launch Kitty Assistant"; Flags: nowait postinstall skipifsilent