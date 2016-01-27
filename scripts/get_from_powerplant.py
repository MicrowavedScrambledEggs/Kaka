from urllib import request
from urllib.error import HTTPError
import re
import os
from platform import platform


def get_files(path):
    proxy = request.ProxyHandler({'http': 'http://proxy.pfr.co.nz:8080'})
    opener = request.build_opener(proxy)
    request.install_opener(opener)
    powerplant_address = 'http://storage.powerplant.pfr.co.nz/workspace/cfphxd/Kaka/data/'
    urlpath = request.urlopen(powerplant_address + path)
    string = urlpath.read().decode('utf-8')
    pattern = re.compile('(?<=href=")((\S+)((\.gz)|(\.csv)))(?=">)')
    cwd = os.getcwd()
    windows = 'Windows' in platform()
    # print("Current working directory: " + cwd)
    if windows:
        cwdsplit = cwd.split('\\')
    else:
        cwdsplit = cwd.split('/')
    print("CWD split: " + str(cwdsplit))
    rebuild = []
    for dir in cwdsplit:
        rebuild.append(dir)
        if dir == 'Kaka':
            break
    rebuild.append('data')
    if windows:
        rebuild.append(path.replace('/', '\\'))
        savepath = '\\'.join(rebuild)
    else:
        rebuild.append(path)
        savepath = '/'.join(rebuild)
    # print("Save Path: " + savepath)
    if not os.path.exists(savepath):
        os.makedirs(savepath)
    for match in pattern.finditer(string):
        address = powerplant_address + path + match.group(1)
        save = savepath + match.group(1)
        try:
            request.urlretrieve(address, save)
        except HTTPError as e:
            print("Could not retrieve: " + address + ": " + e.msg)


def run():
    get_files('genotype/Ach')
    get_files('genotype/East12')
    get_files('genotype/GBS_Workshop_Maize')
