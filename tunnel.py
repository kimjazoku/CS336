import paramiko # make sure install (pip install paramiko)
from getpass import getpass
import sys

# https://web.archive.org/web/20101230075444/http://jessenoller.com/2009/02/05/ssh-programming-with-paramiko-completely-different/

# Configure before running
user = 'stl71'
env_path = 'source ~/Projects/336env/bin/activate'
stub_path = '~/Projects/336/p2/stub.py'

# Would be whatever the parsed query is
# Make sure to enclose in quotes
cmd = '\"SELECT as_of_year, agency_name FROM preliminary limit 1;\"'

password = getpass('Password: ')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('frost.cs.rutgers.edu', username=user,password=password)
stdin, stdout, stderr = ssh.exec_command(f'{env_path}\npython {stub_path} {cmd}')
# print(stderr.readlines())
for line in stdout.readlines():
	sys.stdout.write(line)
