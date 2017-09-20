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

def mkdir_dest(desPath):
    if not os.path.exists(desPath):
        os.mkdir(desPath)

def rmdir_dest(desPath):
    if os.path.exists(desPath):
        os.rmdir(desPath)

zip_name_list = []
pwd_list = []
def decryptRarZipFile(rootdir, filename):

    try:
        if filename.endswith('.zip'):
            fp = zipfile.ZipFile(filename)
        elif filename.endswith('.rar'):
            fp = rarfile.RarFile(filename)
    except Exception as e:
        return False, ""

    #the destination path of zipfile
    desPath = filename[:-4]
    mkdir_dest(desPath)
    
    print ("unzip " + filename)
    #try to use non-password to unzip.
    try:
        #mkdir_dest(desPath)
        fp.extractall(desPath)
        fp.close()
        print('No password')
        return True, filename
    #use dictionary to unzip.
    except:
        #rmdir_dest(desPath)
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
                    #mkdir_dest(desPath)
                    for file in fp.namelist():
                        fp.extract(file, path=desPath, pwd=check_pwd.encode())
                        os.rename(desPath+'\\'+file, desPath+'\\'+file.encode('cp437').decode('gbk'))
                    print('Success! ====>'+check_pwd)
                    fp.close()
                    return True, filename
                    break
                elif filename.endswith('.rar'):
                    #fp.setpassword(check_pwd)
                    #if fp.namelist() in zip_name_list:
                    #    os.rmdir(desPath)
                    #    return False
                    #mkdir_dest(desPath)
                    fp.extractall(path=desPath, pwd=check_pwd)
                    #zip_name_list.append(fp.namelist())
                    print('Success! ====>'+check_pwd)
                    fp.close()
                    return True, filename
                    break
            except Exception as e:
                #try:
                #    rmdir_dest(desPath)
                #except:
                #    pass
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
        unzipped = False
        unzipName = ""
        for file in files:
            filename = os.path.join(root, file)
            if filename[:-7] == unzipName[:-7]:
                break
            if os.path.isfile(filename) and filename.endswith(('.zip', '.rar')):
                ret, unzipName = decryptRarZipFile(root, filename)
                if (ret == True):
                    unzipped = ret
        for file in files:
            filename = os.path.join(root, file)
            if os.path.isfile(filename) and filename.endswith(('.zip', '.rar')):
                if unzipped == True:
                    print("del " + filename + " ...")
                    os.remove(filename)
