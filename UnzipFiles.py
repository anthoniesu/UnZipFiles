import os
import sys
import zipfile

try:
    import rarfile

except:
    path = '"'+os.path.dirname(sys.executable)+'\\scripts\\pip" install --upgrade pip'
    os.system(path)
    path = '"'+os.path.dirname(sys.executable)+'\\scripts\\pip" install rarfile'
    os.system(path)
    import rarfile

rarfile.UNRAR_TOOL='UnRAR.exe'

def decryptRarZipFile(rootdir, filename):

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
            password_path = os.path.join(rootdir, '新文字文件.txt')
            if os.path.exists(password_path):
                fpPwd = open(password_path, encoding = 'UTF-8-sig')
        except:
            print('No dict file in current directory.')
            return
        for pwd in fpPwd:
            pwd = pwd.rstrip()
            try:
                print ("unzip " + filename + "...")
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

download_folder = "K:\\下載\\"

if __name__ == '__main__':

    for root, dirs, files in os.walk(download_folder):
        unzip = False
        for file in files:
            filename = os.path.join(root, file)
            if os.path.isfile(filename) and filename.endswith(('.zip', '.rar')):
                if unzip == False:
                    decryptRarZipFile(root, filename)
                    unzip = True
                os.remove(filename)
