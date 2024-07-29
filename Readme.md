# SecureIt Password Manager and File Encryption Tool

This project is a secure password manager and file encryption tool that runs locally on your computer. All data, including passwords and encrypted files, is stored on your machine, ensuring that your sensitive information never leaves your local environment. This eliminates the risk of your data being compromised or leaked online.

## Features

### Password Manager
- Securely store passwords for multiple websites
- Encrypt passwords using AES-256 encryption
- Decrypt passwords using your password
- Add, remove, and update passwords
- Generate random usernames, secure passwords and passphrases
- User authentication and authorization
- Password leak checking

### File Encryption and Decryption
- Encrypt files with AES-256 encryption
- Decrypt encrypted files
- Drag and drop interface for easy file selection

### Additional Features
- Light mode and dark mode options
- Built with security in mind
- Runs locally on your computer, ensuring your data never leaves your machine

## Technologies Used

- **Python**
- **Django** (Backend framework)
- **HTML, CSS, JavaScript** (Frontend)
- **AES-256 Encryption**
- **SHA-256 Hashing**
- **Electron** (for creating desktop application)

## Installation

You can download the latest version of the installer from the following link:

[Download Secure Password Manager and File Encryption Tool](https://github.com/Carson-Spaniel/Encryption_Site/releases/latest)

Please note that this is a secure application, and you should only download it from trusted sources.

## Versions

### v1.2.1 [Latest Release]

- Fixed
  - Updating password bug

### v1.2.0

- Added
  - Notes page to securely keep notes
  - Password data leak checking: checks online if your passwords have appeared in online data leaks.
- Changed
  - Navigation panel now appears through hovering instead of opening and closing

### v1.1.0

- Added
  - Generated usernames, passwords, and passphrases
  - Import/Export passwords
- Changed
  - Installer to keep current passwords and only update features

### v1.0.1

- Bug fixes
  - Some passwords were causing errors

### v1.0.0

- Initial release

[Latest Release]: https://github.com/Carson-Spaniel/Encryption_Site/releases/latest

## Future
- Possibly adding an auto-updater
- Secure file storage with options for bulk or individual files
