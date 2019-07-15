package com.amazonaws.samples;

import com.amazonaws.auth.DefaultAWSCredentialsProviderChain;
import com.amazonaws.auth.profile.ProfileCredentialsProvider;
import com.amazonaws.services.securitytoken.AWSSecurityTokenService;
import com.amazonaws.services.securitytoken.AWSSecurityTokenServiceClientBuilder;
import com.amazonaws.services.securitytoken.model.GetCallerIdentityRequest;
import com.amazonaws.services.securitytoken.model.GetCallerIdentityResult;

public class CredentialsProviderTest {

	public static void main(String[] args) {
		
		DefaultAWSCredentialsProviderChain creds = new DefaultAWSCredentialsProviderChain();
		
    /*
    To check default credentials from Instance Profile are used. I have no credentials in .aws/credentials or ENV variables
    To learn how aws java sdk finds credentials see the link below:
    https://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/credentials.html#credentials-default
    */
		
		GetCallerIdentityRequest callerIdentity = new GetCallerIdentityRequest();		
		AWSSecurityTokenService client = AWSSecurityTokenServiceClientBuilder.standard().withCredentials(creds).withRegion("us-east-1").build();
		GetCallerIdentityResult res =  client.getCallerIdentity(callerIdentity);
		
		System.out.println("Credentials from DefaultAWSCredentialsProviderChain are : " + res.getArn());
		
		System.out.println("\n");
		
		// Testing Profile Credentials Provider
		// Credentials are used from the profile admin in .aws/credentials
		ProfileCredentialsProvider profile = new ProfileCredentialsProvider("admin");
		
		GetCallerIdentityRequest callerIdentity1 = new GetCallerIdentityRequest();		
		AWSSecurityTokenService client1 = AWSSecurityTokenServiceClientBuilder.standard().withCredentials(profile).withRegion("us-east-1").build();
		GetCallerIdentityResult res1 =  client1.getCallerIdentity(callerIdentity1);
		System.out.println("Credentials from ProfileCredentialsProvider are : " + res1.getArn());
				
	}

}
