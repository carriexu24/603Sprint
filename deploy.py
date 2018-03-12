import paramiko
import os

def login_server(hostname, username, key):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    k = paramiko.RSAKey.from_private_key_file(key)
    ssh.connect(hostname=hostname, username=username, pkey=k)
    return ssh

def copy_repo_2_server(ssh, git_repo):
    repo_path = os.path.basename(git_repo).split('.')[0]

    ssh.exec_command("rm -rf %s" % repo_path) #delete if the repo_path already exists 
    ssh.exec_command("git clone %s" % git_repo) #git clone
    
    return repo_path

def set_crontab(ssh, repo_path, script, prefix):
    # remove current crontab
    ssh.exec_command('crontab -r')

    # add new crontab
    ssh.exec_command("echo '*/2 * * * * python %s/%s %s' > ~/crontabfile" % (repo_path, script, prefix)) 
    ssh.exec_command('crontab ~/crontabfile')

def deploy(hostname, username, key, git_repo, prefix):
    ssh = login_server(hostname, username, key) #log into the server 
    print('You have logged into the server successfully!')

    repo_path = copy_repo_2_server(ssh, git_repo) #git clone
    print('You have cloned the repo into the server successfully!')

    ## two ways to run the command on the server
#   stdin, stdout, stderr = ssh.exec_command('python %s/%s %s' % (repo_path, 'process_json_sprint2.py', prefix)))
    ssh.exec_command('python %s/%s %s' % (repo_path, 'process_json_sprint2.py', prefix))
    print('You have processed json files successfully!')

    set_crontab(ssh, repo_path, 'log_rotate_sprint2.py', prefix) #set crontab
    print('You have set crontab successfully!')

    ssh.close() #log out  

# if __name__ == '__main__':
#     hostname = 
#     username = 
#     key = 
#     git_repo = 'https://github.com/carriexu24/603Sprint'
#     prefix = 'a'

#     deploy(hostname, username, key, git_repo, prefix)