"""
To setup a new server:

-- Spawn a new server instance and log in as root
-- Run the command:
	- adduser crypto-server
-- Follow directions and enter a password
-- Add user to sudoers file
-- Run
	- visudo
	- crypto-server ALL=(ALL) ALL
-- Save and exit
-- Setup pub/private keys with the following:
	- su crypto-server
	- cd ~/
	- mkdir .ssh/
	- cd .ssh/
	- ssh-keygen -t rsa

-- Run this script with
	- fab set_host set_user_server setup_server
"""
from fabric.api import env, sudo, local, run, require
from fabric.context_managers import cd

from settings import FAB_HOST, FAB_USER, FAB_PASS

def set_host():
	env.hosts = [FAB_HOST]

def set_user_server():
	env.user = FAB_USER
	env.password = FAB_PASS


def ubuntu_update():
	sudo('apt-get update')


# Git


# Python, PIP
def install_python_core():
	sudo('apt-get -y install build-essential python-dev python-setuptools')

def install_pip():
	sudo('easy_install pip')

def install_virtualenv():
	sudo('pip install virtualenv')

def create_virtualenv():
	with cd('~/'):
		run('virtualenv env')

def install_tornado_in_virtualenv():
	with cd('~/env/'):
		# Must use && and not separate statements
		run('source bin/activate && pip install tornado')

def install_python_modules():
	install_python_core()
	install_pip()
	install_virtualenv()
	create_virtualenv()
	install_tornado_in_virtualenv()


# Install Git

def install_git():
	sudo('apt-get -y install git-core')

# Unfuddle Repositories

def add_github_keys():
	with cd('~/.ssh/'):
		sudo('ssh-keyscan github.com >> authorized_keys')
		sudo('ssh-keyscan github.com >> known_hosts')

def clone_crypto_app():
	with cd('~/env/'):
		run('git clone git://github.com/sirvaliance/crypto.is.git')


def clone_repos():
	add_github_keys()
	clone_crypto_app()


# Nginx
def install_nginx():
	sudo('apt-get -y install nginx')

def copy_nginx_config():
	with cd('~/env/crypto.is/server-setup'):
		sudo('cp nginx.conf /etc/nginx/nginx.conf')

def restart_nginx():
	sudo('/etc/init.d/nginx restart')

def setup_nginx():
	install_nginx()
	copy_nginx_config()
	restart_nginx()

# Daemontools

def install_daemontools():
	sudo('apt-get -y install daemontools')

def create_svscanboot():
	with cd('~/env/crypto.is/server-setup/daemontools/'):
		sudo('cp svscanboot.conf /etc/init/svscanboot.conf')

def create_services():
	sudo('mkdir /etc/service/')
	sudo('mkdir /etc/service/crypto.is/')
	sudo('cp ~/env/crypto.is/server-setup/daemontools/run /etc/service/crypto.is/run')
	sudo('chmod +x /etc/service/crypto.is/run')
	
def start_daemontools():
	sudo('initctl start svscanboot')


# Symlinks

def create_symlinks():
	with cd('/var/www/'):
		sudo('ln -s ~/env/crypto.is/app/static')

def setup_daemontools():
	install_daemontools()
	create_svscanboot()
	create_services()
	start_daemontools()



# Setup MongoDB
def add_mongo_gpg_key():
	sudo('apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10')

def append_mongo_repos_to_sources():
	sudo('echo "deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen" >> /etc/apt/sources.list')

def apt_get_update():
	sudo('apt-get update')

def apt_get_mongo():
	sudo('apt-get install mongodb-10gen')

def install_pymongo():
	with cd('~/env/'):
		# Must use && and not separate statements
		run('source bin/activate && pip install pymongo')

def install_mongokit():
	with cd('~/env/'):
		# Must use && and not separate statements
		run('source bin/activate && pip install mongokit')


def setup_mongodb():
	add_mongo_gpg_key()
	append_mongo_repos_to_sources()
	apt_get_update()
	apt_get_mongo()
	install_pymongo()
	install_mongokit()



def install_py_bcrypt():
	with cd('~/env/'):
		run('source bin/activate && pip install py_bcrypt')

def setup_server():
	ubuntu_update()
	install_python_modules()
	install_git()
	clone_repos()
	setup_nginx()
	setup_daemontools()
	create_symlinks()
	setup_mongodb()
	install_py_bcrypt()



""" Deployment Scripts


"""

def git_pull_application():
	with cd('~/env/crypto.is/'):
		run('git pull origin master')

def touch_application():
	with cd('~/env/crypto.is/app/'):
		run('touch main.py')






















