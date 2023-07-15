# Neutron

> File and Folder Encryption and Decryption using AES

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Installation

Either install from requirements.txt

```bash
pip install -r requirements.txt
```

OR

Install these two modules

```bash
pip install pycryptodome
```

## How to run

Run Neutron with python, you can use different CLI commands to encrypt and decrypt.

```Python
python Neutron.py --help
```

```
Credit  :       @bannyvishwas
Neutron Encryption Tool Commands:
        -h or --help    :       Opens help commands.
        -e or --encrypt :       Encrypt the files.
        -d or --decrypt :       Decrypt the files.
        -r or --dir     :       Select the directory to encrypt.
        -f or --file    :       Select only a File to Encrypt.
        -x or --ext     :       Select Files with Extension used with -d.
        -k or --key     :       Specified Key for Encryption.

E.g.    neutron -e -r "C:\Users" -x ".jpg,.exe,.txt" -k "MyKey"
        neutron -e -r "C:\Users" -k "MyKey"
        neutron -d -r "C:\Users" -k "MyKey"
        neutron -e -f "C:\Users\img.jpg" -k "MyKey"
```

## Convert Py to EXE
1. Install pyinstaller
   ```bash
   pip install pyinstaller
   pip install Pillow
   ```
2. Use the following command to build exe
   ```bash
   pyinstaller --onefile --console --icon=logo.png Neutron.py
   ```
3. You can find you exe in `dist` folder in root directory.

## Contributing

1. Fork it (<https://github.com/bannyvishwas/neutron/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

For major changes, please open an issue first to discuss what you would like to change. Please make sure to update tests as appropriate.
