The scripts provided in this folder will enable Config in all accounts and in all regions.

EnableConfig.py

- The prerequisites to run this script are:
  1. Each account must have a role with same name "ConfigAdmin" that script assumes to enable config
  2. "ConfigServiceRole" is needed in all the accounts which Config service uses
  3. S3 bucket where Config will store configuration snapshots and configuration history for all the resources Config records
    Bucket Policy should look like the following:
    
    {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AWSConfigBucketPermissionsCheck",
            "Effect": "Allow",
            "Principal": {
                "Service": "config.amazonaws.com"
            },
            "Action": [
                "s3:GetBucketAcl",
                "s3:ListBucket"
            ],
            "Resource": "arn:aws:s3:::example-bucket"
        },
        {
            "Sid": "AWSConfigBucketDelivery",
            "Effect": "Allow",
            "Principal": {
                "Service": "config.amazonaws.com"
            },
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::example-bucket/*",
            "Condition": {
                "StringEquals": {
                    "s3:x-amz-acl": "bucket-owner-full-control"
                }
            }
        }
    ]
}

------------------------------------------------------------------
The file test.csv must contain your account numbers, one per line:
- 123456789012
- 098765432109

To enable config:
- Recording GlobalResources is enabled only in "us-east-1". 

./EnableConfig.py  --assume_role ConfigAdmin --bucket_name example-bucket test.csv


To disable config:
- This script does not disable config in "us-east-1" region. You can modify it easily

./DisableConfig.py --assume_role ConfigAdmin test.csv


-----THE END-------
