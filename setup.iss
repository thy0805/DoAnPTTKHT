[Setup]
AppName=He Thong Quan Ly Thuc An Nhanh
AppVersion=1.0.0
DefaultDirName={autopf}\FastFoodPOS
DefaultGroupName=FastFood POS
OutputDir=Output
OutputBaseFilename=FastFoodPOS_Setup
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin

[Tasks]
Name: "desktopicon"; Description: "Tao shortcut ngoai Desktop"; GroupDescription: "Additional icons:"

[Files]
Source: "dist\launcher.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\app.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "version.json"; DestDir: "{app}"; Flags: ignoreversion
Source: "database.sql"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\FastFood POS"; Filename: "{app}\launcher.exe"
Name: "{commondesktop}\FastFood POS"; Filename: "{app}\launcher.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\launcher.exe"; Description: "Khoi chay phan mem"; Flags: nowait postinstall skipifsilent