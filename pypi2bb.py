#!/usr/bin/env python

import tempfile
import requests
import argparse
import jinja2
import tarfile
import zipfile
import hashlib
import parsesetup
import sys, os
import re

def sanitize_name(name):
    """
    Sanitizes the package name to something that can be used
    by Yocto.

    The steps are:
     - lower case
     - replace _ with -
     - remove version requirements
    """
    re_ver=re.compile('[=><]')
    name=name.lower()
    name=name.replace('_','-')
    name=re_ver.split(name)[0]
    return name


#
# Arguments to CLI
parser = argparse.ArgumentParser(description='Generate Yocto recipes from PyPi packages')
parser.add_argument('package',help='Name of package')
args=parser.parse_args()

package=args.package.replace('_','-')

#
# Get information from PyPi
r=requests.get('https://pypi.python.org/pypi/{}/json'.format(package))
d=r.json()

license=d['info']['license'].replace(' ','-')

version=d['info']['version']
ext='tar.gz'
v=next(filter(lambda x: x['filename'].endswith('tar.gz'), d['releases'][version]),None)
if v==None:
    ext='zip'
    v=next(filter(lambda x: x['filename'].endswith('zip'), d['releases'][version]),None)

pname=d['info']['name'] if d['info']['name']!=package else None

#
# Download file

# Information to extract
licname=None
licmd5=None
depends=[]
rdepends=[]

with tempfile.TemporaryDirectory() as tmpdirname:
    tarr=requests.get(v['url'])

    with open(tmpdirname+'/'+v['filename'], 'wb') as f:
        for chunk in tarr.iter_content(1024):
            f.write(chunk)

    if ext=='tar.gz':
        tarfh=tarfile.open(tmpdirname+'/'+v['filename'], mode="r")
    else:
        tarfh=zipfile.ZipFile(tmpdirname+'/'+v['filename'], mode="r")
    tarfh.extractall(tmpdirname)
    pdirname=v['filename'][:-len(ext)-1]
    allfiles=os.listdir(tmpdirname+'/'+pdirname)

    # Determine license file
    licnames=['LICENSE','LICENSE.md','LICENSE.txt']
    fakelicnames=['README','README.md','README.txt','setup.py']

    for tlicname in licnames:
        if tlicname in allfiles:
            licname=tlicname

    if licname==None:
        print('WARNING: Unable to find a license file in '+str(allfiles))
        for tlicname in fakelicnames:
            if tlicname in allfiles:
                licname=tlicname

    if licname==None:
        print('ERROR: Unable to find a fake license file.')
        sys.exit(1)

    licmd5=hashlib.md5(open(tmpdirname+'/'+pdirname+'/'+licname,'rb').read()).hexdigest()

    # Get requirements from setup file
    cwd=os.getcwd()
    setup_args = parsesetup.parse_setup(tmpdirname+'/'+pdirname+'/setup.py', trusted='True')
    os.chdir(cwd)

    for pkg in setup_args.get('setup_requires',[]):
        depends.append(sanitize_name(pkg))

    for pkg in setup_args.get('install_requires',[]):
        rdepends.append(sanitize_name(pkg))

#
# Create the files
env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

# inc file
t_inc=env.get_template('python.inc')
incfile=t_inc.render(homepage=d['info']['home_page'], summary=d['info']['summary'], license=license, licname=licname, licmd5=licmd5,
                         realname=pname, pkgext=ext,md5sum=v['digests']['md5'],sha256sum=v['digests']['sha256'],
                         rdepends=rdepends, depends=depends)
f=open('python-{}.inc'.format(package),'w')
f.write(incfile)
f.close()

# recipe file
t_bb=env.get_template('python3.bb')
bbfile=t_bb.render(package=package)
f=open('python3-{}_{}.bb'.format(package,version),'w')
f.write(bbfile)
f.close()


