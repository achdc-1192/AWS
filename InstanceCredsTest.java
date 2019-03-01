package com.amazonaws.samples;

//import java.util.concurrent.TimeUnit;

import com.amazonaws.auth.AWSCredentialsProviderChain;
import com.amazonaws.auth.InstanceProfileCredentialsProvider;
import com.amazonaws.auth.STSAssumeRoleSessionCredentialsProvider;
import com.amazonaws.services.identitymanagement.AmazonIdentityManagement;
import com.amazonaws.services.identitymanagement.AmazonIdentityManagementClientBuilder;
import com.amazonaws.services.identitymanagement.model.GetUserRequest;
import com.amazonaws.services.identitymanagement.model.GetUserResult;
//import com.amazonaws.services.s3.AmazonS3;
//import com.amazonaws.services.s3.AmazonS3ClientBuilder;
//import com.amazonaws.services.s3.model.Bucket;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3ClientBuilder;
import com.amazonaws.services.s3.model.Bucket;
import com.amazonaws.services.securitytoken.AWSSecurityTokenService;
import com.amazonaws.services.securitytoken.AWSSecurityTokenServiceClientBuilder;
import com.amazonaws.services.securitytoken.model.GetCallerIdentityRequest;
import com.amazonaws.services.securitytoken.model.GetCallerIdentityResult;

public class InstanceCredsTest {

	public static void main(String[] args) {
		
		AWSCredentialsProviderChain creds = new AWSCredentialsProviderChain(new InstanceProfileCredentialsProvider(true));
		
		AmazonIdentityManagement iamautomatic = AmazonIdentityManagementClientBuilder.standard()
	               .withCredentials(creds).withRegion("us-east-1")
	               .build();
		

			
			GetUserRequest request = new GetUserRequest().withUserName("Test");
			GetUserResult response = iamautomatic.getUser(request);
			System.out.println("Test user id is " + response.getUser().getUserId() + " - Access Key used is " + creds.getCredentials().getAWSAccessKeyId());
			

		System.out.println();
		
		// Uses STS assume role credentials provider that has the feature to refresh assumed role credentials automatically
		// Change role arn and role session name
		STSAssumeRoleSessionCredentialsProvider creds1 = new STSAssumeRoleSessionCredentialsProvider.Builder("Role-ARN", "RoleSessionName").build();
		
		GetCallerIdentityRequest callerIdentity = new GetCallerIdentityRequest();		
		AWSSecurityTokenService client = AWSSecurityTokenServiceClientBuilder.standard().withCredentials(creds1).withRegion("us-east-1").build();
		GetCallerIdentityResult res =  client.getCallerIdentity(callerIdentity);
		
		System.out.println("Credentials from STSAssumeRoleSessionCredentialsProvider are : " + res.getArn());
		
		AmazonS3 s3AutomaticRefresh = AmazonS3ClientBuilder.standard()
	               .withCredentials(creds1).withRegion("us-east-1")
	                .build();
		
		System.out.println("Listing buckets");
		for (Bucket bucket : s3AutomaticRefresh.listBuckets()) {
			System.out.println(" - " + bucket.getName());
		}
		System.out.println();


		
	}

}

