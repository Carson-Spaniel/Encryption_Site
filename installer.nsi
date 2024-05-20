; Version information
VIProductVersion "1.0.0.0"
VIAddVersionKey "ProductName" "SecureIt"
VIAddVersionKey "CompanyName" "Carson Spaniel"
VIAddVersionKey "FileVersion" "1.0.0.0"
VIAddVersionKey "FileDescription" "SecureIt Application"
VIAddVersionKey "LegalCopyright" "© 2024 Carson Spaniel"

!include "MUI2.nsh"
!include WinMessages.nsh
 
; Local bitmap path.
!define BITMAP_FILE "secureit.bmp"
!define MUI_WELCOMEPAGE_BITMAP "secureit.bmp"
!define MUI_ICON "secureit.ico"
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP "secureit.bmp"
!define MUI_HEADERIMAGE_RIGHT
 
; --------------------------------------------------------------------------------------------------
; Installer Settings
; --------------------------------------------------------------------------------------------------
 
Name "SecureIt Password Manager"
OutFile "SecureItInstaller.exe"
Icon "secureit.ico"
Caption "SecureIt Installation"
BrandingText "Install SecureIt"
UninstallIcon "secureit.ico"
 
ShowInstDetails show
 
; --------------------------------------------------------------------------------------------------
; Modern UI Settings
; --------------------------------------------------------------------------------------------------
 
!define MUI_COMPONENTSPAGE_NODESC
!define MUI_FINISHPAGE_NOAUTOCLOSE
!define MUI_CUSTOMFUNCTION_GUIINIT MyGUIInit
 
; --------------------------------------------------------------------------------------------------
; Definitions
; --------------------------------------------------------------------------------------------------
 
Var hBitmap
 
; --------------------------------------------------------------------------------------------------
; Pages
; --------------------------------------------------------------------------------------------------
 
!define MUI_PAGE_CUSTOMFUNCTION_SHOW WelcomePageShow
!insertmacro MUI_PAGE_WELCOME
!define MUI_PAGE_CUSTOMFUNCTION_SHOW LicensePageShow
!insertmacro MUI_PAGE_LICENSE license.nsi
!define MUI_PAGE_CUSTOMFUNCTION_SHOW ComponentsPageShow
!insertmacro MUI_PAGE_COMPONENTS
!define MUI_PAGE_CUSTOMFUNCTION_SHOW InstFilesPageShow
!insertmacro MUI_PAGE_INSTFILES
!define MUI_PAGE_CUSTOMFUNCTION_SHOW FinishPageShow
!insertmacro MUI_PAGE_FINISH
 
; --------------------------------------------------------------------------------------------------
; Languages
; --------------------------------------------------------------------------------------------------
 
!insertmacro MUI_LANGUAGE English
 
; --------------------------------------------------------------------------------------------------
; Macros
; --------------------------------------------------------------------------------------------------
 
; Destroy a window.
!macro DestroyWindow HWND IDC
  GetDlgItem $R0 ${HWND} ${IDC}
  System::Call `user32::DestroyWindow(i R0)`
!macroend
 
; Give window transparent background.
!macro SetTransparent HWND IDC
  GetDlgItem $R0 ${HWND} ${IDC}
  SetCtlColors $R0 0x000000 transparent
!macroend
 
; Refresh window.
!macro RefreshWindow HWND IDC
  GetDlgItem $R0 ${HWND} ${IDC}
  ShowWindow $R0 ${SW_HIDE}
  ShowWindow $R0 ${SW_SHOW}
!macroend
 
; --------------------------------------------------------------------------------------------------
; Functions
; --------------------------------------------------------------------------------------------------
 
Function MyGUIInit
  ; Extract bitmap image.
  InitPluginsDir
  ReserveFile `${BITMAP_FILE}`
  File `/ONAME=$PLUGINSDIR\secureit.bmp` `${BITMAP_FILE}`
FunctionEnd
 
; Refresh parent window controls.
; Has to be done for some controls if they have a
; transparent background.
Function RefreshParentControls
  !insertmacro RefreshWindow  $HWNDPARENT 1037
  !insertmacro RefreshWindow  $HWNDPARENT 1038
FunctionEnd
 
; For welcome page.
Function WelcomePageShow
  ; Set transparent backgrounds.
  SetCtlColors $MUI_HWND 0x000000 transparent
  !insertmacro SetTransparent $MUI_HWND 1200
  !insertmacro SetTransparent $MUI_HWND 1201
  !insertmacro SetTransparent $MUI_HWND 1202

  ; Create bitmap control.
  System::Call `kernel32::GetModuleHandle(i 0) i.R3`
  System::Call `user32::CreateWindowEx(i 0, t "STATIC", t "", i ${SS_BITMAP}|${WS_CHILD}|${WS_VISIBLE}, i 0, i 0, i 120, i 120, i $HWNDPARENT, i 0, i R3, i 0) i.R1`
  System::Call `user32::LoadImage(i 0, t "$PLUGINSDIR\secureit.bmp", i ${IMAGE_BITMAP}, i 0, i 0, i ${LR_LOADFROMFILE}) i.s`
  Pop $hBitmap
  SendMessage $R1 ${STM_SETIMAGE} ${IMAGE_BITMAP} $hBitmap
FunctionEnd
 
; For license page.
Function LicensePageShow
  ; Set transparent backgrounds.
  SetCtlColors $MUI_HWND 0x000000 transparent
  !insertmacro SetTransparent $MUI_HWND 1040
  !insertmacro SetTransparent $MUI_HWND 1000
  !insertmacro SetTransparent $MUI_HWND 1006
  !insertmacro SetTransparent $MUI_HWND 1034
  !insertmacro SetTransparent $MUI_HWND 1035
 
  ; Refresh controls.
  Call RefreshParentControls
FunctionEnd
 
; For components page.
Function ComponentsPageShow
  ; Set transparent backgrounds.
  SetCtlColors $MUI_HWND 0x000000 transparent
  !insertmacro SetTransparent $MUI_HWND 1017
  !insertmacro SetTransparent $MUI_HWND 1022
  !insertmacro SetTransparent $MUI_HWND 1021
  !insertmacro SetTransparent $MUI_HWND 1023
  !insertmacro SetTransparent $MUI_HWND 1006
  !insertmacro SetTransparent $MUI_HWND 1032
 
  ; Refresh controls.
  Call RefreshParentControls
FunctionEnd
 
; For instfiles page.
Function InstFilesPageShow
  ; Set transparent backgrounds.
  SetCtlColors $MUI_HWND 0x000000 transparent
  !insertmacro SetTransparent $MUI_HWND 1027
  !insertmacro SetTransparent $MUI_HWND 1004
  !insertmacro SetTransparent $MUI_HWND 1006
  !insertmacro SetTransparent $MUI_HWND 1016
 
  ; Refresh controls.
  Call RefreshParentControls
FunctionEnd
 
; For finish page.
Function FinishPageShow
  ; Set transparent backgrounds.
  SetCtlColors $MUI_HWND 0x000000 transparent
  !insertmacro SetTransparent $MUI_HWND 1200
  !insertmacro SetTransparent $MUI_HWND 1201
  !insertmacro SetTransparent $MUI_HWND 1202
  !insertmacro SetTransparent $MUI_HWND 1203
  !insertmacro SetTransparent $MUI_HWND 1204
  !insertmacro SetTransparent $MUI_HWND 1205
  !insertmacro SetTransparent $MUI_HWND 1206
FunctionEnd
 
; Free loaded resources.
Function .onGUIEnd
  ; Destroy the bitmap.
  System::Call `gdi32::DeleteObject(i s)` $hBitmap
FunctionEnd
 
; --------------------------------------------------------------------------------------------------
; Install section
; --------------------------------------------------------------------------------------------------
 
Section "SecureIt"
SetOutPath $INSTDIR
File /r "dist\SecureIt\*"  ; Include all files and directories in the dist folder

; Create Start menu shortcut
CreateShortCut "$SMPROGRAMS\SecureIt\SecureIt.lnk" "$INSTDIR\SecureIt.exe"

; Write the uninstaller
WriteUninstaller "$INSTDIR\Uninstall SecureIt.exe"
SectionEnd

; Request admin privileges
RequestExecutionLevel admin

; Installation directory
InstallDir "$PROGRAMFILES\SecureIt"

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
