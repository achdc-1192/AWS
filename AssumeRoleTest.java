package com.amazonaws.samples;

import com.amazonaws.auth.AWSStaticCredentialsProvider;
import com.amazonaws.auth.BasicSessionCredentials;
import com.amazonaws.auth.STSAssumeRoleSessionCredentialsProvider;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3ClientBuilder;
import com.amazonaws.services.s3.model.Bucket;
import com.amazonaws.services.securitytoken.AWSSecurityTokenService;
import com.amazonaws.services.securitytoken.AWSSecurityTokenServiceClientBuilder;
import com.amazonaws.services.securitytoken.model.AssumeRoleRequest;
import com.amazonaws.services.securitytoken.model.AssumeRoleResult;
import com.amazonaws.services.securitytoken.model.GetCallerIdentityRequest;
import com.amazonaws.services.securitytoken.model.GetCallerIdentityResult;

public class AssumeRoleTest {

	public static void main(String[] args) {
		
		GetCallerIdentityRequest callerIdentity = new GetCallerIdentityRequest();
		
		AWSSecurityTokenService client = AWSSecurityTokenServiceClientBuilder.standard().withRegion("us-east-1").build();

		//The following line is to see which credentials are used to perform AssumeRoleRequest
				
		GetCallerIdentityResult res =  client.getCallerIdentity(callerIdentity); 
		System.out.println("The credentials used to assume role are " + res.getArn());

		// Using default credentials from my CLI .aws/credentials profile in my CLI

		//Please modify the ROLE ARN and ROLE SESSION NAME below
		AssumeRoleRequest assume_role = new AssumeRoleRequest().withRoleArn("ROLE-ARN-HERE")
				.withRoleSessionName("ROLE-SESSION-NAME-HERE");
		

		AssumeRoleResult response = client.assumeRole(assume_role);
		
		System.out.println("\n");

		//The following line prints assumed role credentials.
		//System.out.println(response);
		// Loading the AssumeRole credentials into sessionCredentials variable below
		BasicSessionCredentials sessionCredentials = new BasicSessionCredentials(
				response.getCredentials().getAccessKeyId(), response.getCredentials().getSecretAccessKey(),
				response.getCredentials().getSessionToken());
		

		// Building the s3 client with the sessionCredentials variable that has AssumeRole Credentials loaded from above
		// All the subsequent s3 calls are using AssumeRole credentials
		AmazonS3 s3 = AmazonS3ClientBuilder.standard()
				.withCredentials(new AWSStaticCredentialsProvider(sessionCredentials)).withRegion("us-east-1").build();
		
		//AmazonS3 s3AutomaticRefresh = AmazonS3ClientBuilder.standard()
        //       .withCredentials(new STSAssumeRoleSessionCredentialsProvider.Builder("ROLE-ARN-HERE", "test").build() ).withRegion("us-east-1")
        //        .build();
		
		//The following stsClientnew is created just to confirm that we are using role credentials to call S3 list buckets operation
		AWSSecurityTokenService stsClientnew = AWSSecurityTokenServiceClientBuilder.standard()
                .withCredentials(new AWSStaticCredentialsProvider(sessionCredentials)).withRegion("us-east-1").build();
		

		GetCallerIdentityResult resu =  stsClientnew.getCallerIdentity(callerIdentity);		
		System.out.println("The credentials used to call s3 requests are " + resu.getArn());
		
		System.out.println("\n");
		//System.out.println(s3);

		
		System.out.println("Listing buckets");
		for (Bucket bucket : s3.listBuckets()) {
			System.out.println(" - " + bucket.getName());
		}
		System.out.println();
		
	}

}
