import json
import boto3

CONFIG_CLIENT = boto3.client('config')

SNS_CLIENT = boto3.client('sns')

topic_arn = "arn:aws:sns:REGION:ACCOUNT-ID:topic/NAME"

def lambda_handler(event, context):
    
    list_rules = CONFIG_CLIENT.describe_config_rules()
    d = {}
    for rulename in list_rules['ConfigRules']:

        d[rulename['ConfigRuleName']] = []
        evaluation_results = CONFIG_CLIENT.get_compliance_details_by_config_rule(ComplianceTypes=['NON_COMPLIANT'], ConfigRuleName=rulename['ConfigRuleName'])

        for resources in evaluation_results['EvaluationResults']:
            # config resource Id will not give complete ARN. So make another call for et_resource_config_history and get the resource ARN
            resource_arn = CONFIG_CLIENT.get_resource_config_history(resourceType=resources['EvaluationResultIdentifier']['EvaluationResultQualifier']['ResourceType']
            ,resourceId=resources['EvaluationResultIdentifier']['EvaluationResultQualifier']['ResourceId'],limit=1)
            
            d[rulename['ConfigRuleName']].append(resource_arn['configurationItems'][0]['arn'])
    #print(d)
    
    for key,values in d.items():
        if d[key]:
            message = "total " + str(len(values)) + " NON_COMPLIANT resources for ConfigRule - " + key + "\n"
            for pos,value in enumerate(values):
                message +=  "\n" + " " + str(pos) + " - " + value
            response = SNS_CLIENT.publish(TopicArn=topic_arn,Message=message)
            print(response)
