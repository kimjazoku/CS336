import paramiko # make sure install (pip install paramiko)
from getpass import getpass
import sys

# https://web.archive.org/web/20101230075444/http://jessenoller.com/2009/02/05/ssh-programming-with-paramiko-completely-different/

# Configure before running
user = 'htn52'
env_path = 'source ~/336/2_project/projenv/bin/activate'
stub_path = '~/336/2_project/stub.py'

# Would be whatever the parsed query is
# Make sure to enclose in quotes
if (len(sys.argv) > 1):
	cmd = f'\"{sys.argv[1]}\"'
else:
	cmd = ""


password = getpass('Password: ')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('frost.cs.rutgers.edu', username=user,password=password)

try:
	stdin, stdout, stderr = ssh.exec_command(f'{env_path}\npython {stub_path} {cmd}')
except:
	print("There was an error with the server connection, please try again.")
	sys.exit(1)

# Interactive mode, allow the user to input a command and send it over the ssh connection to stdin for the recieving stub.py
if cmd == "":
	cmd = input("Please write your SQL statement here: ")
	stdin.write(cmd + "\n")
	stdin.flush


for line in stderr.readlines():
	sys.stdout.write(line)

for line in stdout.readlines():
	sys.stdout.write(line)