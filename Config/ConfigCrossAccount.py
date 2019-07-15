# use python3.7 in lambda function
# If the role is cross account, rule sets it as NON_COMPLIANT
# If the role has a service or same account then it sets to COMPLIANT

import json
import urllib.parse
from datetime import datetime
import boto3

client = boto3.client('config')

# Helper function used to validate input
def check_defined(reference, reference_name):
    if not reference:
        raise Exception('Error: ', reference_name, 'is not defined')
    return reference

# Check whether the resource has been deleted. If the resource was deleted, then the evaluation returns not applicable.   
def is_applicable(configurationItem, event):
    try:
        check_defined(configurationItem, 'configurationItem')
        check_defined(event, 'event')
    except:
        return True
    status = configurationItem['configurationItemStatus']
    eventLeftScope = event['eventLeftScope']
    if status == 'ResourceDeleted':
        print("Resource Deleted, setting Compliance Status to NOT_APPLICABLE.")
    return (status == 'OK' or status == 'ResourceDiscovered') and not eventLeftScope

# Checks if the accountId from event is listed in Trust Relationship then sets it to compliant
# If the trust contains only service, then the rule is set to compliant
def evaluate_compliance(event, configuration_item):
    check_defined(configuration_item, 'configurationItem')
    check_defined(event, 'event')

    assume_policy = urllib.parse.unquote(configuration_item['configuration']['assumeRolePolicyDocument'])
    assume_policy = json.loads(assume_policy)
    account = 0
    for state in assume_policy['Statement']:
        for values in state['Principal'].values():
            if event['accountId'] in str(values) or 'amazonaws.com' in str(values):
                account += 1

    if account >= 1:
        return "COMPLIANT"
    return "NON_COMPLIANT"

def lambda_handler(event, context):
    #print(event)
    invoking_event = json.loads(event["invokingEvent"])
    #invoking_event = event["invokingEvent"] -> This is for test event.
    configuration_item = invoking_event['configurationItem']
    result_token = "None"
    if "resultToken" in event:
        result_token = event["resultToken"]
    #print(configuration_item['configurationItemStatus'])

    compliance_result = "NOT_APPLICABLE"
    
    if is_applicable(configuration_item, event):
        compliance_result = evaluate_compliance(event, configuration_item)
    else:
        print("this is for not applicable resources")
        compliance_result = "NOT_APPLICABLE"
    
    return client.put_evaluations(
        Evaluations = [{
            "ComplianceResourceType" : configuration_item["resourceType"],
            "ComplianceResourceId" : configuration_item["resourceId"],
             "ComplianceType" : compliance_result,
             "Annotation": compliance_result,
             "OrderingTimestamp" : configuration_item["configurationItemCaptureTime"]
             },],
             ResultToken=result_token,
             )
