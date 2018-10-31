package com.amazonaws.samples;

import java.util.concurrent.TimeUnit;

import com.amazonaws.auth.AWSCredentialsProviderChain;
import com.amazonaws.auth.InstanceProfileCredentialsProvider;
import com.amazonaws.services.identitymanagement.AmazonIdentityManagement;
import com.amazonaws.services.identitymanagement.AmazonIdentityManagementClientBuilder;
import com.amazonaws.services.identitymanagement.model.GetUserRequest;
import com.amazonaws.services.identitymanagement.model.GetUserResult;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3ClientBuilder;
import com.amazonaws.services.s3.model.Bucket;

public class InstanceCredsTest {

	public static void main(String[] args) {
		
		AWSCredentialsProviderChain creds = new AWSCredentialsProviderChain(new InstanceProfileCredentialsProvider(true));
		
		
		AmazonS3 s3 = AmazonS3ClientBuilder.standard()
	              .withCredentials(new InstanceProfileCredentialsProvider(false))
	              .build();
		
		
		AmazonIdentityManagement iamautomatic = AmazonIdentityManagementClientBuilder.standard()
	               .withCredentials(creds).withRegion("us-east-1")
	               .build();
		
		for(int i=0; i< 10; i++) {
			
			GetUserRequest request = new GetUserRequest().withUserName("Test");
			GetUserResult response = iamautomatic.getUser(request);
			System.out.println("Test user id is " + response.getUser().getUserId() + " - Access Key used is " + creds.getCredentials().getAWSAccessKeyId());
			
		}
		

		System.out.println("Listing buckets");
		for (Bucket bucket : s3.listBuckets()) {
			System.out.println(" - " + bucket.getName());
		}
		System.out.println();


		
	}

}

