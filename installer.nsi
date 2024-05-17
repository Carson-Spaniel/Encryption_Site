; Define product information
Name "SecureIt"
OutFile "SecureItInstaller.exe"
Caption "SecureIt Installation"
BrandingText "Install SecureIt"

; Version information
VIProductVersion "1.0.0.0"
VIAddVersionKey "ProductName" "SecureIt"
VIAddVersionKey "CompanyName" "Carson Spaniel"
VIAddVersionKey "FileVersion" "1.0.0.0"
VIAddVersionKey "FileDescription" "SecureIt Application"
VIAddVersionKey "LegalCopyright" "© 2024 Carson Spaniel"

; Request admin privileges
RequestExecutionLevel admin

; Installation directory
InstallDir "$PROGRAMFILES\SecureIt"

Section "Install"
SetOutPath $INSTDIR
File /r "dist\SecureIt\*"  ; Include all files and directories in the dist folder

; Create Start menu shortcut
CreateShortCut "$SMPROGRAMS\SecureIt\SecureIt.lnk" "$INSTDIR\server.exe"

; Write the uninstaller
WriteUninstaller "$INSTDIR\Uninstall.exe"
SectionEnd

Section -PostInstall
; Open the installation directory
ExecShell "open" "$INSTDIR"
SectionEnd

; Uninstaller
Section "Uninstall"
Delete "$INSTDIR\server.exe"
; Delete other installed files and directories
Delete "$INSTDIR\*.*" ; Deletes all files in the installation directory
RMDir /r "$INSTDIR" ; Recursively removes all directories and subdirectories

; Delete Start menu shortcut
Delete "$SMPROGRAMS\SecureIt\SecureIt.lnk"
RMDir "$SMPROGRAMS\SecureIt"
SectionEnd

; Uninstall information
UninstallText "This will uninstall SecureIt from your computer."

Section "un"
SectionEnd
