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


zip_name_list = []
pwd_list = []
def decryptRarZipFile(rootdir, filename):

    try:
        if filename.endswith('.zip'):
            fp = zipfile.ZipFile(filename)
        elif filename.endswith('.rar'):
            fp = rarfile.RarFile(filename)
    except:
        return

    #the destination path of zipfile
    desPath = filename[:-4]
    if not os.path.exists(desPath):
        os.mkdir(desPath)

    if fp.namelist in zip_name_list:
        return

    zip_name_list.append(fp.namelist)
    print ("unzip " + filename)
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
                for pwd in fpPwd:
                    pwd = pwd.rstrip()
                    pwd_list.append(pwd)
                fpPwd.close()

        except:
            print('No dict file in current directory.')
        
        for check_pwd in pwd_list:
            try:
                if filename.endswith('.zip'):
                    for file in fp.namelist():
                        fp.extract(file, path=desPath, pwd=check_pwd.encode())
                        os.rename(desPath+'\\'+file, desPath+'\\'+file.encode('cp437').decode('gbk'))
                    print('Success! ====>'+check_pwd)
                    fp.close()
                    break
                elif filename.endswith('.rar'):
                    fp.extractall(path=desPath, pwd=check_pwd)
                    print('Success! ====>'+check_pwd)
                    fp.close()
                    break
            except:
                pass

download_folder = "K:\\下載\\"

def get_public_pwd ():
    public_pwd_path = "C:\\Users\\Anthonie Su\\Desktop\\password.txt"
    if os.path.exists(public_pwd_path):
        fp_public_pwd = open(public_pwd_path, encoding = 'UTF-8-sig')
        for public_pwd in fp_public_pwd:
            public_pwd = public_pwd.rstrip()
            pwd_list.append(public_pwd)

if __name__ == '__main__':

    get_public_pwd ()
    
    for root, dirs, files in os.walk(download_folder):
        for file in files:
            filename = os.path.join(root, file)
            if os.path.isfile(filename) and filename.endswith(('.zip', '.rar')):
                decryptRarZipFile(root, filename)
        for file in files:
            filename = os.path.join(root, file)
            print("del " + filename + " ...")
            if os.path.isfile(filename) and filename.endswith(('.zip', '.rar')):
                os.remove(filename)
