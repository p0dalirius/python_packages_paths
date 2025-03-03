#!/usr/bin/env python3


import requests
from bs4 import BeautifulSoup

def get_pypi_modules():
    print("[+] Getting pypi modules ...")
    r = requests.get('https://pypi.org/simple/')
    print("[+] Parsing pypi /simple/ page ...")
    soup = BeautifulSoup(r.text, 'html.parser')
    modules = soup.find_all('a')
    module_names = [a.get('href').split('/')[2].strip('/') for a in modules if a.get('href').startswith('/simple/')]
    print(f"[+] Found {len(module_names)} modules")
    return module_names

def get_pypi_module_versions(module_name):
    print(f"[+] Getting pypi module versions for {module_name} ...")
    r = requests.get(f'https://pypi.org/simple/{module_name}/')
    print(f"[+] Parsing pypi /simple/{module_name}/ page ...")
    soup = BeautifulSoup(r.text, 'html.parser')
    modules = soup.find_all('a')
    module_versions = [a.get('href').split('/')[-1] for a in modules]
    module_versions = [v[len(module_name):].replace('.tar.gz','-').replace('.zip','-').split('-')[1] for v in module_versions if v.startswith(module_name)]
    module_versions = sorted(list(set(module_versions)))
    print(f"[+] Found {len(module_versions)} versions")
    return module_versions

if __name__ == "__main__":
    modules = get_pypi_modules()
    for module in modules:
        versions = get_pypi_module_versions(module)
        print(f"[+] Module {module} has {len(versions)} versions")
        for version in versions:
            print(f"    - {version}")
