'''
Please run this code in Python3 environment

***** NOTE - THIS CODE DOESN'T UPDATE CLOUDFORMATION and CODEBUILD TAGS *****


This rule will use AWS Config "required-tags" rule. The "required-tags" rule will check
if the resources have the following tags
auto-stop : no
auto-delete : never

If the resources don't have these tags, resources are marked as NON_COMPLIANT

Using CloudWatch event we trigger the following lambda which will add tags to the resources.

CloudWatch Rule pattern is as follows:

{
  "source": [
    "aws.config"
  ],
  "detail-type": [
    "AWS API Call via CloudTrail"
  ],
  "detail": {
    "eventSource": [
      "config.amazonaws.com"
    ],
    "eventName": [
      "PutEvaluations"
    ],
    "requestParameters": {
      "evaluations": {
        "complianceType": [
          "NON_COMPLIANT"
        ]
      }
    },
    "additionalEventData": {
      "managedRuleIdentifier": [
        "REQUIRED_TAGS"
      ]
    }
  }
}

'''

import boto3
import json

ACM_CLIENT = boto3.client('acm')
ASG_CLIENT = boto3.client('autoscaling')
DDB_CLIENT = boto3.client('dynamodb')
EC2_CLIENT = boto3.client('ec2')
ELB_CLIENT_1 = boto3.client('elb')
ELB_CLIENT_2 = boto3.client('elbv2')
RDS_CLIENT = boto3.client('rds')
REDSHIFT_CLIENT = boto3.client('redshift')
S3_CLIENT = boto3.client('s3')
CONFIG_CLIENT = boto3.client('config')


def lambda_handler(event, context):
    #print(event["detail"]["requestParameters"]["evaluations"])
    evaluations = event["detail"]["requestParameters"]["evaluations"]
    accountId = event['account']
    region = event["detail"]["awsRegion"]
    for evaluation in evaluations:
        #print(evaluation)
        if evaluation["complianceType"] == "NON_COMPLIANT":

            if 'EC2' in evaluation["complianceResourceType"]:
                ec2_add_tags(evaluation["complianceResourceType"], evaluation["complianceResourceId"])

            elif 'ACM' in evaluation["complianceResourceType"]:
                acm_add_tags(evaluation["complianceResourceType"], evaluation["complianceResourceId"])

            elif 'DynamoDB' in evaluation["complianceResourceType"]:
                dynamodb_add_tags(accountId, region, evaluation["complianceResourceType"], evaluation["complianceResourceId"])

            elif 'Redshift' in evaluation["complianceResourceType"]:
                redshift_add_tags(accountId, region, evaluation["complianceResourceType"], evaluation["complianceResourceId"])

            elif 'RDS' in evaluation["complianceResourceType"]:
                rds_add_tags(accountId, region, evaluation["complianceResourceType"], evaluation["complianceResourceId"])

            elif 'S3' in evaluation["complianceResourceType"]:
                s3_add_tags(evaluation["complianceResourceType"], evaluation["complianceResourceId"])

            elif 'AutoScaling' in evaluation["complianceResourceType"]:
                autoscaling_add_tags(evaluation["complianceResourceType"], evaluation["complianceResourceId"])

            elif evaluation["complianceResourceType"] == "AWS::ElasticLoadBalancing::LoadBalancer":
                elb_1_add_tags(evaluation["complianceResourceType"], evaluation["complianceResourceId"])

            elif evaluation["complianceResourceType"] == "AWS::ElasticLoadBalancingV2::LoadBalancer":
                elb_2_add_tags(evaluation["complianceResourceType"], evaluation["complianceResourceId"])
    return None

def acm_add_tags(complianceResourceType, complianceResourceId):
    try:
        response = ACM_CLIENT.add_tags_to_certificate(CertificateArn=complianceResourceId,Tags=[{'Key': 'auto-stop', 'Value' : 'no'},{'Key': 'auto-delete', 'Value' : 'never'}])
        print("Adding Tags on {} for the resource {}".format(complianceResourceType, complianceResourceId))
        return response
    except Exception as e:
        print("DID_NOT ADD TAGS on {} for the resource {}".format(complianceResourceType, complianceResourceId))
        return e

def autoscaling_add_tags(complianceResourceType,complianceResourceId):
    try:
        response = ASG_CLIENT.create_or_update_tags(Tags=[{'Key': 'auto-stop', 'Value' : 'no', 'ResourceId': complianceResourceId},{'Key': 'auto-delete', 'Value' : 'never', 'ResourceId': complianceResourceId}])
        print("Adding Tags on {} for the resource {}".format(complianceResourceType, complianceResourceId))
        return response
    except Exception as e:
        print("DID_NOT ADD TAGS on {} for the resource {}".format(complianceResourceType, complianceResourceId))
        return e


def dynamodb_add_tags(accountId, region, complianceResourceType,complianceResourceId):
    arn="arn:aws:dynamodb:"+region+":"+accountId+":table/"+complianceResourceId
    try:
        response = DDB_CLIENT.tag_resource(ResourceArn=arn,Tags=[{'Key': 'auto-stop', 'Value' : 'no'},{'Key': 'auto-delete', 'Value' : 'never'}])
        print("Adding Tags on {} for the resource {}".format(complianceResourceType, complianceResourceId))
        return response
    except Exception as e:
        print("DID_NOT ADD TAGS on {} for the resource {}".format(complianceResourceType, complianceResourceId))
        return e


def ec2_add_tags(complianceResourceType,complianceResourceId):
    try:
        response = EC2_CLIENT.create_tags(Resources=[complianceResourceId],Tags=[{'Key': 'auto-stop', 'Value' : 'no'},{'Key': 'auto-delete', 'Value' : 'never'}])
        print("Adding Tags on {} for the resource {}".format(complianceResourceType, complianceResourceId))
        return response
    except Exception as e:
        print("DID_NOT ADD TAGS on {} for the resource {}".format(complianceResourceType, complianceResourceId))
        return e


def elb_1_add_tags(complianceResourceType,complianceResourceId):
    try:
        response = ELB_CLIENT_1.add_tags(LoadBalancerNames=[complianceResourceId],Tags=[{'Key': 'auto-stop', 'Value' : 'no'},{'Key': 'auto-delete', 'Value' : 'never'}])
        print("Adding Tags on {} for the resource {}".format(complianceResourceType, complianceResourceId))
        return response
    except Exception as e:
        print("DID_NOT ADD TAGS on {} for the resource {}".format(complianceResourceType, complianceResourceId))
        return e

def elb_2_add_tags(complianceResourceType,complianceResourceId):
    try:
        response = ELB_CLIENT_2.add_tags(ResourceArns=[complianceResourceId],Tags=[{'Key': 'auto-stop', 'Value' : 'no'},{'Key': 'auto-delete', 'Value' : 'never'}])
        print("Adding Tags on {} for the resource {}".format(complianceResourceType, complianceResourceId))
        return response
    except Exception as e:
        print("DID_NOT ADD TAGS on {} for the resource {}".format(complianceResourceType, complianceResourceId))
        return e

def rds_add_tags(accountId, region, complianceResourceType,complianceResourceId):
    arn = ""
    if complianceResourceType == "AWS::RDS::DBInstance":
        rds_db_details = CONFIG_CLIENT.list_discovered_resources(resourceType="AWS::RDS::DBInstance",resourceIds=[complianceResourceId])
        rds_db_name = rds_db_details["resourceIdentifiers"][0]["resourceName"]
        arn="arn:aws:rds:"+region+":"+accountId+":db:"+rds_db_name
    elif complianceResourceType == "AWS::RDS::DBSecurityGroup":
        arn="arn:aws:rds:"+region+":"+accountId+":secgrp:"+complianceResourceId
    elif complianceResourceType == "AWS::RDS::DBSnapshot":
        arn="arn:aws:rds:"+region+":"+accountId+":snapshot:"+complianceResourceId
    elif complianceResourceType == "AWS::RDS::DBSubnetGroup":
        arn="arn:aws:rds:"+region+":"+accountId+":subgrp:"+complianceResourceId
    else:
        arn="arn:aws:rds:"+region+":"+accountId+":es:"+complianceResourceId
    print(arn)
    try:
        response = RDS_CLIENT.add_tags_to_resource(ResourceName=arn,Tags=[{'Key': 'auto-stop', 'Value' : 'no'},{'Key': 'auto-delete', 'Value' : 'never'}])
        print("Adding Tags on {} for the resource {}".format(complianceResourceType, complianceResourceId))
        return response
    except Exception as e:
        print("DID_NOT ADD TAGS on {} for the resource {}".format(complianceResourceType, complianceResourceId))
        return e

def redshift_add_tags(accountId, region, complianceResourceType,complianceResourceId):
    arn = ""
    if complianceResourceType == "AWS::Redshift::Cluster":
        arn="arn:aws:redshift:"+region+":"+accountId+":cluster:"+complianceResourceId
    elif complianceResourceType == "AWS::Redshift::ClusterParameterGroup":
        arn="arn:aws:redshift:"+region+":"+accountId+":parametergroup:"+complianceResourceId
    elif complianceResourceType == "AWS::Redshift::ClusterSecurityGroup":
        arn="arn:aws:redshift:"+region+":"+accountId+":securitygroup:"+complianceResourceId
    elif complianceResourceType == "AWS::Redshift::ClusterSnapshot":
        arn="arn:aws:redshift:"+region+":"+accountId+":snapshot:"+complianceResourceId
    elif complianceResourceType == "AWS::Redshift::ClusterSubnetGroup":
        arn="arn:aws:redshift:"+region+":"+accountId+":subnetgroup:"+complianceResourceId
    else:
        arn="arn:aws:redshift:"+region+":"+accountId+":eventsubscription:"+complianceResourceId
        

    try:
        response = REDSHIFT_CLIENT.create_tags(ResourceName=arn,Tags=[{'Key': 'auto-stop', 'Value' : 'no'},{'Key': 'auto-delete', 'Value' : 'never'}])
        print("Adding Tags on {} for the resource {}".format(complianceResourceType, complianceResourceId))
        return response
    except Exception as e:
        print("DID_NOT ADD TAGS on {} for the resource {}".format(complianceResourceType, complianceResourceId))
        return e

def s3_add_tags(complianceResourceType,complianceResourceId):
    try:
        response = S3_CLIENT.put_bucket_tagging(Bucket=complianceResourceId,Tagging={'TagSet' : [{'Key': 'auto-stop', 'Value' : 'no'},{'Key': 'auto-delete', 'Value' : 'never'}]})
        print("Adding Tags on {} for the resource {}".format(complianceResourceType, complianceResourceId))
        return response
    except Exception as e:
        print("DID_NOT ADD TAGS on {} for the resource {}".format(complianceResourceType, complianceResourceId))
        return e


