package com.amazonaws.samples;

import java.util.concurrent.TimeUnit;

import com.amazonaws.auth.STSAssumeRoleSessionCredentialsProvider;
import com.amazonaws.services.identitymanagement.AmazonIdentityManagement;
import com.amazonaws.services.identitymanagement.AmazonIdentityManagementClientBuilder;
import com.amazonaws.services.identitymanagement.model.GetUserRequest;
import com.amazonaws.services.identitymanagement.model.GetUserResult;

public class STSAutomaticRefreshTest {

	public static void main(String[] args) throws InterruptedException {
		
		//STSAssumeRoleSessionCredentialsProvider is used to assume the role. This method refreshes the credentials automatically
		STSAssumeRoleSessionCredentialsProvider creds = new STSAssumeRoleSessionCredentialsProvider.Builder("ROLE-ARN-HERE", "ROLE-SESSION-NAME")
     		   .withRoleSessionDurationSeconds(900).build();
		
				
		AmazonIdentityManagement iamautomatic = AmazonIdentityManagementClientBuilder.standard()
		               .withCredentials(creds).withRegion("us-east-1")
		               .build();
		
		//The for loop is just to test the credentials are indeed rotating automatically.
		
		for(int i=0; i< 10; i++) {
			
			GetUserRequest request = new GetUserRequest().withUserName("Test");
			GetUserResult response = iamautomatic.getUser(request);
			System.out.println("Test user id is " + response.getUser().getUserId() +"Access Key used is " + creds.getCredentials().getAWSAccessKeyId());
			TimeUnit.SECONDS.sleep(300);
		}
		
		/*
		BasicAWSCredentials awsCreds = new BasicAWSCredentials("access_key_id", "secret_key_id");
		AmazonS3 s3Client = (AmazonS3) AmazonS3ClientBuilder.standard()
		                        .withCredentials(new AWSStaticCredentialsProvider(awsCreds))
		                        .build().listObjects("testbucket");
		*/
		//System.out.println(iam);
		
		/*
		System.out.println("Listing buckets");
		for (Bucket bucket : s3.listBuckets()) {
			System.out.println(" - " + bucket.getName());
		}
		System.out.println();
		
		*/
		
	}

}
