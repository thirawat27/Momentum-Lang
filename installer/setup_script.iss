; Inno Setup Script for Momentum Language (v1.0)
; Full integration with custom logo

[Setup]
AppName=Momentum Language
AppVersion=1.0
AppPublisher=Momentum Project
DefaultDirName={autopf}\Momentum
DefaultGroupName=Momentum Language
DisableProgramGroupPage=yes
OutputDir=.\Output
OutputBaseFilename=Momentum_Setup_v1.0
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
; --- ใช้โลโก้สำหรับตัวติดตั้ง ---
SetupIconFile=momentum_logo.ico
; --- ใช้โลโก้สำหรับตัวถอนการติดตั้ง (ใน Control Panel) ---
UninstallDisplayIcon={app}\momentum_logo.ico

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
;Name: "thai"; MessagesFile: "compiler:Languages\Thai.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}";
Name: "addtopath"; Description: "เพิ่ม Momentum ไปยัง PATH (เพื่อให้รันจาก command prompt ได้)"; GroupDescription: "การตั้งค่าขั้นสูง"; Flags: checkedonce

[Files]
; --- ติดตั้งไฟล์ทั้งหมดที่จำเป็น ---
Source: "momentum.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "mn.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "momentum_logo.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; --- ไอคอนใน Start Menu และ Desktop จะมาจากไฟล์ .exe ที่ฝังไอคอนไว้แล้ว ---
Name: "{group}\Momentum"; Filename: "{app}\momentum.exe"
Name: "{autodesktop}\Momentum"; Filename: "{app}\momentum.exe"; Tasks: desktopicon

[Registry]
; --- การเชื่อมโยงไฟล์ .mn ให้ใช้โลโก้โดยตรง ---
Root: HKA; Subkey: "Software\Classes\.mn"; ValueType: string; ValueName: ""; ValueData: "Momentum.File"; Flags: uninsdeletekey; Tasks: addtopath
Root: HKA; Subkey: "Software\Classes\Momentum.File"; ValueType: string; ValueName: ""; ValueData: "Momentum Source File"; Flags: uninsdeletekey; Tasks: addtopath
; --- เปลี่ยนให้ไฟล์ .mn แสดงผลด้วย momentum_logo.ico ---
Root: HKA; Subkey: "Software\Classes\Momentum.File\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\momentum_logo.ico"; Tasks: addtopath
Root: HKA; Subkey: "Software\Classes\Momentum.File\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\momentum.exe"" ""%1"""; Tasks: addtopath

; --- เขียนค่า PATH ลงใน Registry ---
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; \
    ValueType: expandsz; ValueName: "Path"; ValueData: "{olddata};{app}"; Tasks: addtopath

[Run]
Filename: "{app}\momentum.exe"; Description: "{cm:LaunchProgram,Momentum}"; Flags: nowait postinstall skipifsilent