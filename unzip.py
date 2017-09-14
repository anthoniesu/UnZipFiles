import os
import sys
import zipfile

try:
    from unrar import rarfile

except:
    path = '"'+os.path.dirname(sys.executable)+'\\scripts\\pip" install --upgrade pip'
    os.system(path)
    path = '"'+os.path.dirname(sys.executable)+'\\scripts\\pip" install unrar'
    os.system(path)
    from unrar import rarfile


def decryptRarZipFile(filename):

    if filename.endswith('.zip'):
        fp = zipfile.ZipFile(filename)
    elif filename.endswith('.rar'):
        fp = rarfile.RarFile(filename)

    #the destination path of zipfile
    desPath = filename[:-4]
    if not os.path.exists(desPath):
        os.mkdir(desPath)
    #try to use non-password to unzip.
    try:
        fp.extractall(desPath)
        fp.close()
        print('No password')
        return
    #use dictionary to unzip.
    except:
        try:
            if os.path.exists('pwddict.txt'):
                fpPwd = open('pwddict.txt', encoding = 'UTF-8-sig')
            elif os.path.exists('新文字文件.txt'):
                fpPwd = open('新文字文件.txt', encoding = 'UTF-8-sig')
        except:
            print('No dict file pwddict.txt in current directory.')
            return
        for pwd in fpPwd:
            pwd = pwd.rstrip()
            try:
                if filename.endswith('.zip'):
                    for file in fp.namelist():
                        fp.extract(file, path=desPath, pwd=pwd.encode())
                        os.rename(desPath+'\\'+file, desPath+'\\'+file.encode('cp437').decode('gbk'))
                    print('Success! ====>'+pwd)
                    fp.close()
                    break
                elif filename.endswith('.rar'):
                    fp.extractall(path=desPath, pwd=pwd)
                    print('Success! ====>'+pwd)
                    fp.close()
                    break
            except:
                pass
        fpPwd.close()

if __name__ == '__main__':

    filename = sys.argv[1]

    if os.path.isfile(filename) and filename.endswith(('.zip', '.rar')):
        decryptRarZipFile(filename)
    else:

        print('Must be Rar or Zip file')

