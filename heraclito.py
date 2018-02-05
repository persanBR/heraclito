# -*- coding: utf-8 -*-
#!/usr/bin/python
# Nada é permanente, salvo a mudança.
# VERSAO: 0.0
# NOME:                         	  heraclito.py
# CRIADO POR:                   Alan.Pereira
#---------------------------------------------------------------------------------------#

import boto3,argparse,sys,logging,time
from argparse import RawTextHelpFormatter

logging.basicConfig(filename='/var/log/heraclito.log',level=logging.INFO,
                                             format='%(asctime)s %(levelname)s %(message)s')
def assumerole(account_id):
    sts_client = boto3.client('sts',)

    assumedRoleObject = sts_client.assume_role(
        RoleArn="arn:aws:iam::"+account_id+":role/infra-bastion",
        RoleSessionName="InfraBastion"
    )
    credentials = assumedRoleObject['Credentials']

    ec2 = boto3.resource(
           'ec2',
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken'],
    )
    return ec2

def modify_ec2 (instanceid, new_instance_type,options):
        instanceChange = ec2.Instance(instanceid)
        if ((instanceChange.instance_type) != (new_instance_type)) or ((not new_instance_type) and (options)):
                stop_ec2(instanceid)
                if (options):
                    ec2_options(options,instanceChange)
                if(new_instance_type != 'none'):
                    modify = instanceChange.modify_attribute(InstanceType={'Value': new_instance_type})
                    logging.info('Modifying ' +  instanceid + ': ' + str(modify))
                start_ec2(instanceid)

def ec2_options (options,instanceChange):
    for a in options:
        if a == 'ebs-opt-no':
           modifyEBS = instanceChange.modify_attribute(EbsOptimized={'Value': False})
        if a == 'ebs-opt-yes':
           modifyEBS = instanceChange.modify_attribute(EbsOptimized={'Value': True})

def start_ec2 (instanceid):
        print 'starting ' +  instanceid
        instance = ec2.Instance(instanceid)
        action = instance.start().get('StartingInstances',[])[0]
        logging.info('Starting ' +  instanceid + ': ' + str(action))

def stop_ec2 (instanceid):
        print 'stoping ' + instanceid
        instance = ec2.Instance(instanceid)
        action = instance.stop().get('StoppingInstances',[])[0]
        logging.info('Stoping ' +  instanceid + ': ' + str(action))
        try:
              instance.wait_until_stopped()
        except:
              return 1

parser = argparse.ArgumentParser(description='Realiza Acoes sobre instancias', formatter_class=RawTextHelpFormatter)
parser.add_argument('--start', action="store_true", help="Start an Ec2.")
parser.add_argument('--stop', action="store_true", help="Stop an Ec2.")
parser.add_argument('--instance-id', action="store", dest="instanceid",  help="Ec2 instance id.")
parser.add_argument('--modify-ec2', action="store", dest="modify", help="Modify the ec2 to the new type.")
parser.add_argument('--account', action="store", dest="account", help="Account to assume role.")
parser.add_argument('--options', action="store", dest="options", nargs='*', help='''ebs-opt-no - disable ebs-optimized \nebs-opt-yes - enable ebs-optimized''')
args = parser.parse_args()

if (len(sys.argv) == 1) or ( not args.instanceid):
        parser.print_help()
        #inserir mensagem de erro
        sys.exit(1)

if (args.instanceid) and ((not args.start) and (not args.stop) and (not args.modify) and (not args.options)):
        parser.print_help()
        print "Nenhuma Acao encontrada"
        sys.exit(1)

if args.account:
        ec2 = assumerole(args.account)
else:
        ec2 = boto3.resource('ec2')

if args.start:
        start_ec2(args.instanceid)

if args.stop:
        stop_ec2(args.instanceid)

if args.modify:
        modify_ec2(args.instanceid, args.modify, args.options)
else:
        if args.options:
             modify_ec2(args.instanceid, 'none', args.options)



