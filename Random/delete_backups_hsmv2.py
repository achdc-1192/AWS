import boto3
import time
import argparse

HSM_CLIENT = boto3.client('cloudhsmv2')

parser = argparse.ArgumentParser()
parser.add_argument('--backup_id',
						type=str,
						required=True,
						help="back up id that you don't want to delete")
args = parser.parse_args()
clusters = HSM_CLIENT.describe_clusters()

backups_list = []
backup = HSM_CLIENT.describe_backups()

for backups in backup['Backups']:
	backups_list.append(backups['BackupId'])
while True:
	if 'NextToken' in backup:
		time.sleep(1)
		backup = HSM_CLIENT.describe_backups(NextToken=backup['NextToken'])
		for backups in backup['Backups']:
			backups_list.append(backups['BackupId'])
	else:
		break

for bkup in backups_list:
	print("deleting backup",bkup)
	if bkup != args.backup_id:
		HSM_CLIENT.delete_backup(BackupId=bkup)
	time.sleep(1)
