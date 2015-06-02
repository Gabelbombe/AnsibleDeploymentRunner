#!/usr/bin/env python
# Deploy latest from {{BRANCH}} to an environment

# CPR : Jd Daniel :: Ehime-ken
# MOD : 2015-06-02 @ 13:03:10

# INP : $ python deploy.py develop 2dd34f62eee0a309fb3e61e3f333a4329a648010
# INP : # $ python deploy.py /EngradeAppPath develop 2dd34f62eee0a309fb3e61e3f333a4329a648010


import json
import os
import tarfile
import shutil
import argparse             ## requires: pip install argparse
import subprocess
import tempfile
import pwd
import grp
import logging

from github import Github   ## requires: pip install pygithub
import requests             ## requires: pip install requests


# Cheating here, this makes things look good but it's meh
arg_parser = argparse.ArgumentParser(description="Quick and Dirty deployer, emphasis on dirty")
# arg_parser.add_argument('path', help="Path you will be unloading to")
arg_parser.add_argument('branch', help="Branch of the repo you want to maintain")
arg_parser.add_argument('token', help="Token of the Github account to check out from")
arg_parser.add_argument('--organization', default="engrade", help="Name of the organization that holds the repo")
arg_parser.add_argument('--repo', default='Engrade', help="Name of the repo")
arg_parser.add_argument('--no-composer', action='store_false', dest='composer', help="Skip Composer Run")
arg_parser.add_argument('--temp-dir', help="Overwrite the default temp dir", default=tempfile.gettempdir())
arg_parser.add_argument('--owner', help="Default owner of the target directory", default="apache")
arg_parser.add_argument('--group', help="Default group of the target directory", default="apache")
arg_parser.add_argument('--verbose', '-v', help="Increase Verbosity", action="count")
arg_parser.add_argument('--force', help="Force a deploy", action="store_true")
args = arg_parser.parse_args()

# track_file = os.path.join(path, 'deploy_hash_'+args.branch)
track_file = os.path.join('/local/apps/engradepro/engradeapp', 'deploy_hash_'+args.branch)

#temp_dir = '/tmp'

composer = True
log = logging.getLogger("deploy")

#switch would be nice
if args.verbose == 1:
    logging.basicConfig(level=logging.INFO)
elif args.verbose > 1:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.WARNING)


def get_file_handle(track_file, write=False):
    #Check if file exists, if it does open it, if not try to create it, if that fails, scream bloody murder
    mode = 'r'
    if write:
        mode = 'w'
    try:
        fh = open(track_file, mode)
        log.debug("Opened track_file {track_file} with mode {mode}".format(track_file=track_file, mode=mode))
    except IOError as e:
        log.debug("Got IOError exception {elevel}".format(elevel=e.errno))
        if e.errno == 2:
            log.debug("Opened a new track_file {track_file} in w+ mode")
            fh = open(track_file, 'w+')
    return fh

def get_local_hash(fh):
    try:
        object = json.load(fh)
    except:
        object = {
            'current': None,
            'previous': []
        }
    return object


def write_local_hash(fh, object, new_hash):
    if object['current']:
        object['previous'].append(object['current'])
    object['current'] = new_hash
    #injecting some cleanup logic here
    while len(object['previous']) > 5:
        delHash = object['previous'].pop(0)
        shutil.rmtree(os.path.join(args.local_checkout, delHash))
    json.dump(object, fh)


fh = get_file_handle(track_file)
lh = get_local_hash(fh)

#Get Connected
gh = Github(args.token)
repo = gh.get_organization(args.organization).get_repo(args.repo)

#Get Commit
commit = repo.get_branch(args.branch).commit
ch = commit.sha

#most common, current and ref matches
if lh and 'current' in lh.keys() and lh['current'] == ch and not args.force:
    log.info("Deploy current")
    exit(0)

#figure out archive link and download the file temporarily
url = repo.get_archive_link('tarball', ref=commit.sha)
checkout_name = '{org}-{rep}-{com}'.format(org=args.organization, rep=args.repo, com=commit.sha)
local_filename = checkout_name + '.tar.gz'
archive_loc = os.path.join(args.temp_dir, local_filename)
if not os.path.isfile(archive_loc):
    r = requests.get(url, stream=True)
    with open(archive_loc, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
try:
    tf = tarfile.open(archive_loc)
    tf.extractall(args.temp_dir)
    os.unlink(archive_loc)
except:
    log.warn("Couldn't open tarfile")
    exit(2)

print 'Deploying SHA: ',commit.sha

# move stuff around
# target = os.path.join(path+'/jobs/', commit.sha)
target = os.path.join('/local/apps/engradepro/engradeapp/jobs/', commit.sha)

api_target = os.path.join(target, 'engradeapi/w/')

# sym_target = path+'/current'
sym_target = '/local/apps/engradepro/engradeapp/current'

if os.path.islink(sym_link):
#    path = os.readlink(path+'/current')
    path = os.readlink('/local/apps/engradepro/engradeapp/current')
    print path

#run composer
if os.path.isdir(target):
    shutil.rmtree(target)
shutil.move(os.path.join(args.temp_dir, checkout_name), target)
if args.composer:
    for ctarget in [target,api_target]:
        logging.debug("Running Composer in {0} directory".format(ctarget))
        os.chdir(ctarget)
        composer_target = os.path.join(ctarget, 'composer.phar')
        if os.path.isfile(composer_target):
            subprocess.call(composer_target + ' --quiet --no-dev --no-interaction --optimize-autoloader install',
                            shell=True)
#get user and group id
uid = pwd.getpwnam(args.owner).pw_uid
gid = grp.getgrnam(args.group).gr_gid

os.chown(target, uid, gid)
for root, dirs, files in os.walk(target):
    for dir in dirs:
        try:
            os.chown(os.path.join(root, dir), uid, gid)
        except:
            pass
    for file in files:
        try:
            os.chown(os.path.join(root, file), uid, gid)
        except:
            pass


#swap symlinks
if os.path.islink(sym_target):
    os.unlink(sym_target)

print 'Using Target:  ' + target
print 'Using Symlink: ' + sym_target

os.symlink(target, sym_target)

#update the local file
fh = get_file_handle(track_file, True)
write_local_hash(fh, lh, commit.sha)

#restart fpm isn't necessary on local but it will be in prod
#send clean exit signal, not necessary but fun
log.info("Deployment done")
exit(0)
