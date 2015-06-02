#### Ansible deployment runner for python deployer

Run using the following after clone

 * ansible-playbook -v -i hosts/servers.ini -D playbooks/deploy.yml 2>&1 |tee logs/run.log
 
Log will be in logs/run.log with the above command


#### Ini setup for Servers

Use hosts/servers.ini and create a file similar to the following

```ini
    [requiresPass]
    10.228.139.156  ansible_ssh_user=jd_daniel  ansible_ssh_pass='YourSSHPass' ansible_sudo=True
    10.228.143.172  ansible_ssh_user=jd_daniel  ansible_ssh_pass='YourSSHPass' ansible_sudo=True
    
    [requiresPem]
    10.228.142.214  ansible_connection=ssh  ansible_ssh_user=root  ansible_ssh_private_key_file=credentials/yourkey.pem
    10.228.142.215  ansible_connection=ssh  ansible_ssh_user=root  ansible_ssh_private_key_file=credentials/yourkey.pem
    10.228.142.212  ansible_connection=ssh  ansible_ssh_user=root  ansible_ssh_private_key_file=credentials/yourkey.pem
```

You can singularly test with the following

 * ansible-playbook -v --limit `{{WHAT TO TEST}}` -i hosts/servers.ini -D playbooks/deploy.yml

Where {{variable}} is `requiresPass` or `requiresPem`


#### Testing credentials etc....

 * ansible-playbook -vvvv -i hosts/servers.ini -D playbooks/knocks.yml 2>&1 |tee logs/debug.log
 
 Look for an output recap similar to the below, analyze faileds and unreachables
 
 ```bash
     PLAY RECAP ********************************************************************
     10.228.000.000             : ok=1    changed=1    unreachable=0    failed=0
     10.228.000.000             : ok=1    changed=1    unreachable=0    failed=0
     10.228.000.000             : ok=1    changed=1    unreachable=0    failed=0
     10.228.000.000             : ok=1    changed=1    unreachable=0    failed=0
     10.228.000.000             : ok=1    changed=1    unreachable=0    failed=0
     10.228.000.000             : ok=1    changed=1    unreachable=0    failed=0
     10.228.000.000             : ok=1    changed=1    unreachable=0    failed=0
     10.228.000.000             : ok=1    changed=1    unreachable=0    failed=0
     10.228.000.000             : ok=1    changed=1    unreachable=0    failed=0
     10.228.000.000             : ok=1    changed=1    unreachable=0    failed=0
     10.228.000.000             : ok=1    changed=1    unreachable=0    failed=0
     10.228.000.000             : ok=1    changed=1    unreachable=0    failed=0
     10.228.000.000             : ok=1    changed=1    unreachable=0    failed=0
     10.228.000.000             : ok=1    changed=1    unreachable=0    failed=0
     10.228.000.000             : ok=1    changed=1    unreachable=0    failed=0
     10.228.000.000             : ok=1    changed=1    unreachable=0    failed=0
     10.228.000.000             : ok=1    changed=1    unreachable=0    failed=0
     10.228.000.000             : ok=1    changed=1    unreachable=0    failed=0
     10.228.000.000             : ok=1    changed=1    unreachable=0    failed=0
     10.228.000.000             : ok=1    changed=1    unreachable=0    failed=0
     10.228.000.000             : ok=1    changed=1    unreachable=0    failed=0
     10.228.000.000             : ok=1    changed=1    unreachable=0    failed=0
     10.228.000.000             : ok=1    changed=1    unreachable=0    failed=0
     10.228.000.000             : ok=1    changed=1    unreachable=0    failed=0
     10.228.000.000             : ok=1    changed=1    unreachable=0    failed=0
     10.228.000.000             : ok=1    changed=1    unreachable=0    failed=0
     10.228.000.000             : ok=1    changed=1    unreachable=0    failed=0
 ```