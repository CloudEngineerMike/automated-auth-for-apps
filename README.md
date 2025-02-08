# cloud-index-authorizer

![Image](https://github.com/user-attachments/assets/b50ace7c-5ddd-4be6-ab5e-228ac903e3e5)


## Use Case

Through **Cloud Index Authorizer**'s website, customers request access to the **Cloud Index Authorizer** GUI or API for cloud inventory data. Previously, this process was manual and time-consuming. As engineers, we believe in leveraging technology to automate repetitive tasks, leading to the creation of the **Cloud Index Authorizer**.


## Solution

The **Cloud Index Authorizer** is a cloud-native service designed to automate the request process for accessing the **Cloud Index Authorizer** UI or API. This reduces manual intervention, streamlines workflows, and improves efficiency.



## Architecture and Design

![Image](https://github.com/user-attachments/assets/d6a3cf8f-4de6-419c-9b2e-d0e792eb5b0a)

### Key AWS Services Used:

- **DynamoDB** - Stores request and access data
- **API Gateway** - Manages API requests
- **Lambda** - Handles automation logic
- **Secrets Manager** - Secures sensitive information

### Languages:

- **Python** 



## ⚙How It Works

1️⃣ **Customer submits a **CIA Access Request** via Cloud Index Authorizer's interface.

2️⃣ **Engineering Approval** is required before the request can proceed.

3️⃣ Once approved, clicking `Start` on the CIA's interface, which changes the request status to `PENDING`, triggering the automation pipeline.

4️⃣ The request payload is sent via webhook to the **API Gateway Proxy Endpoint**, triggering the automation **Lambda function**.

5️⃣ The Lambda function processes the request based on type:
   - **GUI Access:** Requires user **SSO** or **RBAC GROUP**.
   - **API Access:** Requires a **Special SSO**, verified from Identity Team. If verified, an **API Key** is generated for the customer.

6️⃣ Once all conditions are met, the payload is structured and added to the DynamoDB table to grant user access.

7️⃣ The **Email API** sends an email with the access details and usage instructions.

8️⃣ After verifying access, the request is marked `Completed` in MyHosting.



## 📖 User Documentation

Find the complete user guide Confluence.



## 🚀 Deployment

The **Cloud Index Authorizer** is deployed using **Terraform CLI** for streamlined infrastructure management.



🎯 **Automate, simplify, and optimize cloud access management with the Cloud Index Authorizer!**
