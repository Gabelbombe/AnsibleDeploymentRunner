#### Ansible deployment runner for python deployer

Run using the following after clone

 * ansible-playbook -v -i hosts/servers.ini -D playbooks/deploy.yml 2>&1 |tee logs/run.log
 
Log will be in logs/run.log with the above command