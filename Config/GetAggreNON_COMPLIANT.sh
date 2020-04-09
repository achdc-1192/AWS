#!/bin/sh
account=(account1 account2 account3 account4)

for i in "${account[@]}"; 
do 
  aws configservice get-aggregate-compliance-details-by-config-rule  --aws-region us-west-2 --config-rule-name ec2-instance-managed-by-systems-manager --configuration-aggregator-name MASTER-AGGREGATOR --max-items 50 --compliance-type NON_COMPLIANT --account-id $i --query 'AggregateEvaluationResults[].EvaluationResultIdentifier.EvaluationResultQualifier.ResourceId';
done;
