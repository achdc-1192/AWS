var AWS = require('aws-sdk');
// Get credentials from the profile Test in .aws/credentials file
var credentials = new AWS.SharedIniFileCredentials({
    profile: 'Test'
});
// Prints the credentials just the access key
console.log("Initial user credentials to use for assume role call are : ", credentials);

// List of parameters required for AssumeRole API call
var params = {
    DurationSeconds: 3600,
    RoleArn: "arn:aws:iam::123456789012:role/Instance",
    RoleSessionName: "InstanceRole"
};


//Using sts variable to assume the role
var sts = new AWS.STS();
var result = sts.assumeRole(params, function(err, data) {
    if (err)
        console.log("error is : ", err, err.stack);
    else
        console.log("Role Credentials Are : ", data);
    // The following variables use the credentials received from the above sts.assumeRole call
    var roleAccessId = data.Credentials.AccessKeyId;
    var roleSecretKey = data.Credentials.SecretAccessKey;
    var roleSessionToken = data.Credentials.SessionToken;

    // Setting the above role credentials to use by calling creds api call

    var creds = new AWS.Credentials(roleAccessId, roleSecretKey, roleSessionToken)

    // Testing simple EC2 describe calls

    var ec2 = new AWS.EC2({
        region: 'us-east-1'
    });

    ec2.describeInstances(function(err, data) {
        if (err) {
            console.log("Error", err.stack);
        } else {
            console.log("Success", JSON.stringify(data));
        }
    });
});