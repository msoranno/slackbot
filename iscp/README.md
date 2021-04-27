# iscp-bot

## How to run it ?

``` 
# Test env.
export SLACK_API_TOKEN="xoxb-861708542357-...."
export IAM_URL="https://x-iam.x-iam.svc:8443" 
export IAM_USER="x-cicd"
export IAM_PASS="aU@Ih...."
export IAM_CLIENT_ID="x-cicd"
export IAM_CLIENT_SECRET="1c2acab1...."
export IAM_REALM="ibm"
export IAM_CA_FILE="/home/sp81891/PycharmProjects/GITHUB/slackbot/iscp/iamCa.pem"
export VAULT_URL="https://x-vault.x-vault:8200"
export VAULT_API_VERSION="v1"
export SA_TOKEN_FILE_LOCATION="/home/sp81891/tmp/sa_token"


./ngrok http -region eu 5000
python3 ./iscp/iscp-bot.py

# Forwards
kubectl -n x-iam port-forward svc/x-iam 8443:443
kubectl -n x-vault port-forward svc/x-vault 8200:8200

# get SA
kubectl -n x-cicd run ubuntu -i -t --restart=Never --image=ubuntu --serviceaccount=tekton-triggers-sa
cat /var/run/secrets/kubernetes.io/serviceaccount/token

# Copy token on
/home/sp81891/tmp/sa_token
```

## On slack workspace

- update 

> Slash Commands -> edit your app -> requested URL

then

> Interactivity and shortcuts -> requested URL

- Reinstall app on your workspace (if needed)

Go to Install App, and click `Reinstall to Workspace`
