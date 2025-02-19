# AWS Automated Authentication
_Automated authentication workflow for verifying user payloads and granting access to GUI or API._


![Image](./assets/cia.svg)

## Overview
This AWS-based authentication system automatically verifies user payloads to determine access to a **GUI** or **API** for interacting with a database table. The authentication system leverages an **external API** for verification and, once validated, sends an email via **AWS SES** with the user’s new **API key** or **GUI access notification**.

## Diagram
![AWS Authentication Diagram](./assets/cia-diagram.svg)

## Workflow
1. **User submits an authentication request** with a payload containing credentials.
2. **Payload verification** occurs:
   - The payload is checked against a **database** via an **external API**.
3. **Access Determination**:
   - If valid, grant **GUI** or **API key access**.
   - If invalid, reject the request.
4. **Email Notification**:
   - **AWS SES** sends an email notifying the user of their new **API key** or **GUI access status**.

## AWS Services Used
- **AWS Lambda** → Handles request processing and verification.
- **Amazon API Gateway** → Facilitates API access for authentication.
- **Amazon DynamoDB** → Stores user authentication data.
- **External API** → Used for verifying payload authentication.
- **AWS SES (Simple Email Service)** → Sends authentication confirmation emails.

## Setup & Deployment
### 1. Prerequisites
- AWS account with necessary IAM permissions.
- AWS CLI installed and configured.
- API access to the external database.

### 2. Clone the Repository
```sh
git clone https://github.com/<your-org>/<your-repo>
cd <your-repo>
```

### 3. Deploy AWS Lambda Functions
#### Install dependencies:
```sh
npm install
```

#### Deploy using AWS SAM:
```sh
sam build && sam deploy --guided
```
OR
#### Deploy using AWS CDK:
```sh
cdk deploy
```

### 4. API Invocation
Manually test the API with:
```sh
curl -X POST https://<api-gateway-url>/authenticate \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "password": "securepassword"}'
```

### 5. Check Email Notification
- If authentication is successful, the user will receive an email from **AWS SES** containing either:
  - Their **new API key**.
  - A notification of **GUI access**.

## 🚀 Execution Stages
| Stage | Service | Description |
|-------|---------|-------------|
| **Authentication Request** | API Gateway | User submits credentials payload. |
| **Verification** | Lambda + External API | Payload is compared with database records. |
| **Access Decision** | Lambda | Determines API key issuance or GUI access. |
| **Notification** | AWS SES | Sends confirmation email to user. |

## 📖 Resources
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
- [Amazon API Gateway Documentation](https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html)
- [Amazon DynamoDB Documentation](https://docs.aws.amazon.com/dynamodb/latest/developerguide/)
- [AWS SES Documentation](https://docs.aws.amazon.com/ses/latest/dg/)
