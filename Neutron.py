import os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import sys, getopt
import getpass
from pathlib import Path

parent_folder_index = None

def create_new_dir(filename,postfix):
    filepath = Path(filename)
    dirname = filepath.parent
    fname = filepath.name
    parts = list(filepath.parts)
    parts[parent_folder_index] = parts[parent_folder_index] + postfix
    new_file_path = Path(*parts)
    new_parent = new_file_path.parent

    if not new_parent.exists():
        new_parent.mkdir(parents=True, exist_ok=True)
    
    return str(new_file_path)

def encrypt(key, filename,dir_enable=False):
    chunksize = 64 * 1024
    outputFile = filename+".ntn"
    
    if dir_enable:
        outputFile = create_new_dir(filename,"_enc") + ".ntn"
    
    filesize = str(os.path.getsize(filename)).zfill(16)
    IV = Random.new().read(16)

    encryptor = AES.new(key, AES.MODE_CBC, IV)

    with open(filename, 'rb') as infile:
        with open(outputFile, 'wb') as outfile:
            outfile.write(filesize.encode('utf-8'))
            outfile.write(IV)

            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - (len(chunk) % 16))

                outfile.write(encryptor.encrypt(chunk))
    print('Encrypted\t:\t',filename)


def decrypt(key, filename,dir_enable=False):
    if filename.endswith('.ntn'):
        chunksize = 64 * 1024
        outputFile = filename[:-4]
        if dir_enable:
            outputFile = create_new_dir(filename,"_dec")[:-4]
        
        with open(filename, 'rb') as infile:
            filesize = int(infile.read(16))
            IV = infile.read(16)

            decryptor = AES.new(key, AES.MODE_CBC, IV)

            with open(outputFile, 'wb') as outfile:
                while True:
                    chunk = infile.read(chunksize)

                    if len(chunk) == 0:
                        break

                    outfile.write(decryptor.decrypt(chunk))
                outfile.truncate(filesize)
        print('Decrypted\t:\t',filename)


def getKey(password):
    hasher = SHA256.new(password.encode('utf-8'))
    return hasher.digest()


def helpwn():
      print('')
      print('Credit\t:\t@bannyvishwas')
      print ('Neutron Encryption Tool Commands:')
      print('\t-h or --help\t:\tOpens help commands.')
      print('\t-e or --encrypt\t:\tEncrypt the files.')
      print('\t-d or --decrypt\t:\tDecrypt the files.')
      print('\t-r or --dir\t:\tSelect the directory to encrypt.')
      print('\t-f or --file\t:\tSelect only a File to Encrypt.')
      print('\t-x or --ext\t:\tSelect Files with Extension used with -d.')
    #   print('\t-k or --key\t:\tSpecified Key for Encryption.')
      print('')
      print('E.g.\tneutron -e -r "C:\\Users" -x ".jpg,.exe,.txt"')
      print('\tneutron -e -r "C:\\Users"')
      print('\tneutron -d -r "C:\\Users"')
      print('\tneutron -e -f "C:\\Users\\img.jpg"')
      
def main(argv):
   global parent_folder_index
   inputfile = ''
   inputdir=''
   ext=''
   key=''
   encry=False
   decry=False
   ext_enable=False
   dir_enable=False
   file_enable=False
   key_enable=False
   try:
      opts, args = getopt.getopt(argv,"hr:f:k:x:ed",["help","dir=","file=","ext=","key=","encrypt","decrypt"])
   except getopt.GetoptError:
      helpwn()
      sys.exit(2)
   for opt, arg in opts:
      if opt in ("-h","--help"):
         helpwn()
         sys.exit()
      elif opt in ("-r", "--dir"):
         if not file_enable:
            inputdir = arg
            filepath = Path(inputdir)
            dir_list = filepath.parts
            parent_folder_index = len(dir_list) - 1
            dir_enable=True
         else:
            print('Invalid Syntax : -r cannot be used with -f.')
            sys.exit()
      elif opt in ("-f", "--file"):
         if not dir_enable:
            inputfile = arg
            file_enable=True
         else:
            print('Invalid Syntax : -f cannot be used with -r.')
            sys.exit()
            sys.exit()
      elif opt in ("-x", "--ext"):
         if dir_enable:
            ext = arg
            ext_enable=True
         else:
            print('Invalid Syntax : -x only used with -r.')
            sys.exit()
    #   elif opt in ("-k", "--key"):
    #      key = arg
    #      key_enable=True
      elif opt in ("-e","--encrypt"):
         if not decry:
            encry=True
         else:
            print('Invalid Syntax: -e cannot be used with -d')
            sys.exit()
      elif opt in ("-d","--decrypt"):
         if not encry:
            decry=True
         else:
            print('Invalid Syntax: -d cannot be used with -e')
            sys.exit()

   if (encry or decry) and (file_enable or dir_enable):
      if encry:
        key = getpass.getpass("Enter Encryption Key : ")
      else:
          key = getpass.getpass("Enter Decryption Key : ")
      keyhash=getKey(key)
      exttuple=tuple(ext.split(","))
      if dir_enable:
           if os.path.exists(inputdir) and os.path.isdir(inputdir): 
                 files = []
                 # r=root, d=directories, f = files
                 for r, d, f in os.walk(inputdir):
                        for file in f:
                                if ext_enable:
                                    if str(file).endswith(exttuple):
                                        filepath=os.path.join(r, file)
                                        files.append(filepath)
                                else:
                                    filepath=os.path.join(r, file)
                                    files.append(filepath)
                                #print(filepath)
                 for f in files:
                    try:
                        if encry: 
                            encrypt(keyhash, f, dir_enable=True)
                           #  os.remove(f)
                        else:
                            decrypt(keyhash,f,dir_enable=True)
                           #  os.remove(f)
                    except Exception as e:
                        print('[Skipping] Operation Failed : ',f,e)
                        continue
      elif file_enable:
           if os.path.exists(inputfile) and os.path.isfile(inputfile):
                   try:
                        if encry: 
                            encrypt(keyhash, inputfile)
                           #  os.remove(inputfile)
                        else:
                            decrypt(keyhash,inputfile)
                           #  os.remove(inputfile)
                   except Exception as e:
                        print('Operation Failed : ',e)
      else:
          helpwn()
          sys.exit()
   else:
      helpwn()
      sys.exit()

if __name__ == "__main__":
   main(sys.argv[1:])

