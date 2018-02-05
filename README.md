# Heraclito

##Schedule and change a ec2 instance type programmatically

####Give execution permition to the script:

#chmod +x heraclito.py

####Insert on the /etc/crontab

36 19 * * * root  /usr/bin/python /root/heraclito.py --modify-ec2 t2.medium --instance-id i-xxxxxxxxxxxx --options ebs-opt-no

00 07 * * * root /usr/bin/python /root/heraclito.py --start --instance-id i-xxxxxxxxxxxxxx  --account xxxxxxxxxxxx 

####Actions

modify-ec2  - Change a ec2 type
stop        - stop ec2
start       - start ec2
account     - When set assume role to that account
