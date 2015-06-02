#### Ansible deployment runner for python deployer

Run using the following after clone

 * ansible-playbook -v -i hosts/servers.ini -D playbooks/deploy.yml 2>&1 |tee logs/run.log
 
Log will be in logs/run.log with the above command


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