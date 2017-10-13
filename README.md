
### Settings to start development

1. Install the Google Cloud SDK, initialize it and run core gcloud commands from the command-line on your development systems.
Perform the following steps:
```bash
# Create an environment variable for the correct distribution
export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)"

# Add the Cloud SDK distribution URI as a package source
echo "deb http://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

# Import the Google Cloud Platform public key
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -

# Update the package list and install the Cloud SDK
sudo apt-get update && sudo apt-get install google-cloud-sdk

```

2. Provide your credentials to the tool with the command:
 ```bash
gcloud auth application-default login 
```
Result:
```bash
Credentials saved to file: [/home/ygrigortsevich/.config/gcloud/application_default_credentials.json]
```
