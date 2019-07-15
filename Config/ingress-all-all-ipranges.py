# Description: Check that security groups do not have an inbound rule with ALL protocols, ALL port range and 0.0.0.0/0 IP
#
# Trigger Type: Change Triggered
# Scope of Changes: EC2:SecurityGroup
# Accepted Parameters: None
# Your Lambda function execution role will need to have a policy that provides
# the appropriate permissions. Here is a policy that you can consider.
# You should validate this for your own environment.
#
# {
#    "Version": "2012-10-17",
#    "Statement": [
#        {
#            "Effect": "Allow",
#            "Action": [
#                "logs:CreateLogGroup",
#                "logs:CreateLogStream",
#                "logs:PutLogEvents"
#            ],
#            "Resource": "arn:aws:logs:*:*:*"
#        },
#        {
#            "Effect": "Allow",
#            "Action": [
#                "config:PutEvaluations"
#            ],
#            "Resource": "*"
#        }
#    ]
# }


import boto3
import json


APPLICABLE_RESOURCES = ["AWS::EC2::SecurityGroup"]


def evaluate_compliance(configuration_item):

    # Start as compliant
    compliance_type = 'COMPLIANT'
    annotation = "Security group is compliant."
    
    # This is the part I modified. This bit loops through custom IP ranges in Security groups and appends to cidrlist array
    cidrlist = []
    for i in configuration_item['configuration']['ipPermissions']:
        for ip in i["ipRanges"]:
            cidrlist.append(ip)
    print(cidrlist)
        

    # Check if resource was deleted
    if configuration_item['configurationItemStatus'] == "ResourceDeleted":
        compliance_type = 'NOT_APPLICABLE'
        annotation = "This resource was deleted."

    # Check resource for applicability
    elif configuration_item["resourceType"] not in APPLICABLE_RESOURCES:
        compliance_type = 'NOT_APPLICABLE'
        annotation = "The rule doesn't apply to resources of type " \
                     + configuration_item["resourceType"] + "."

    else:
        # Iterate over IP permissions
        for i in configuration_item['configuration']['ipPermissions']:
            # inbound rules with Port = "All" and protocols = ALL and checks if 0.0.0.0/0 exists from the above cidrlist array
            if "fromPort" not in i and i['ipProtocol'] == "-1" and "0.0.0.0/0" in cidrlist:
                compliance_type = 'NON_COMPLIANT'
                annotation = 'Security group is not compliant.'
                break

    return {
        "compliance_type": compliance_type,
        "annotation": annotation
    }


def lambda_handler(event, context):

    invoking_event = json.loads(event['invokingEvent'])
    configuration_item = invoking_event["configurationItem"]
    evaluation = evaluate_compliance(configuration_item)
    config = boto3.client('config')

    print('Compliance evaluation for %s: %s' % (configuration_item['resourceId'], evaluation["compliance_type"]))
    print('Annotation: %s' % (evaluation["annotation"]))

    response = config.put_evaluations(
       Evaluations=[
           {
               'ComplianceResourceType': invoking_event['configurationItem']['resourceType'],
               'ComplianceResourceId':   invoking_event['configurationItem']['resourceId'],
               'ComplianceType':         evaluation["compliance_type"],
               "Annotation":             evaluation["annotation"],
               'OrderingTimestamp':      invoking_event['configurationItem']['configurationItemCaptureTime']
           },
       ],
       ResultToken=event['resultToken'])
