import json
import boto3
import requests
import base64
import os
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Attr

def lambda_handler(event, context):
    body = json.loads(event['body'])
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.getenv('DYNAMO_TABLE'))

    def send_success_email(access_type, generated_key=None):
        secret_name = os.getenv('EMAIL_APP_SECRET_NAME')
        email_app_url = os.getenv('EMAIL_APP_API_URL') + "/sendemail/_____"
        postman_key = get_secret(secret_name)

        if access_type == "API":
            long_desc = "Included below is your API key. To get started, visit: <URL>"
            api_key_string = f"API Key: {generated_key}"
        else:
            long_desc = "You can now access the cloud-index-authorizer at <URL>"
            api_key_string = ""

        email_body = {"KEY": "VALUE"}
        headers = {'Content-type': 'application/json', 'x-api-key': postman_key}
        requests.post(email_app_url, json=email_body, headers=headers)

    def parse_auth_groups(groups):
        if "VendorType" in body:
            for vendor in body["VendorType"]:
                group_map = {"AWS": "aws-only-vendor", "Azure": "azure-only-vendor"}
                if vendor in group_map:
                    groups.append(group_map[vendor])
        return groups

    def BU_auth_groups(groups):
        BU = {"BRANCH": "UNIQUE_KEY"}
        if "RequestedBranch" in body:
            for unit in body["RequestedBranch"]:
                if unit in BU:
                    groups.append(BU[unit])
        return groups

    def get_secret(secret_name):
        client = boto3.client('secretsmanager', region_name="<REGION>")
        try:
            response = client.get_secret_value(SecretId=<secret_name>)
            return response.get('SecretString', base64.b64decode(response.get('SecretBinary', b'')))
        except ClientError as e:
            raise e

    def <verify_group_name>():
        api_key = get_secret("<INSERT-ARN>")
        response = requests.get(f"<URL>?<GroupNumber>={body['<GROUP_NUMBER>']}", headers={'x-api-key': api_key}).json()
        if not response:
            print('Error: Invalid groupNumber.')
        return response.get("groupName")

    def verify_SSO_name():
        api_key = get_secret("<INSERT-ARN>")
        response = requests.get(f"<URL>?sso={body['SSO']}", headers={'x-api-key': api_key}).json()
        if not response or "<EmployeeName>" not in response:
            print("Error: Invalid SSO response.")
            return None
        return response["EmployeeName"]

    def generate_api_key():
        api_gateway_client = boto3.client('apigateway')
        response = api_gateway_client.create_api_key(
            name=f"cmc_{body['SSO']}",
            description=f"Generated for SR {body['Fake_ID']} | Requester: {body['Fake_Requester']}",
            enabled=True,
            generateDistinctId=True,
        )
        api_gateway_client.create_usage_plan_key(
            usagePlanId=os.getenv('CIA_USAGE_PLAN'),
            keyId=response["id"],
            keyType="API_KEY"
        )
        return response["id"], response["value"]

    def gui_request():
        if "<GroupNumber>" in body:
            entry = {
                ...
            }
        else:
            entry = {
               ...
            }
        entry["groups"] = BU_auth_groups(parse_auth_groups(entry["groups"]))
        table.put_item(Item=entry)
        send_success_email("GUI")

    def api_request():
        if "SSO" in body and len(body["SSO"]) == 9 and body["SSO"].startswith("5"):
            SN = verify_SSO_name()
            if SN:
                API_ID, API_KEY = generate_api_key()
                entry = {
                    ...
                }
                entry["groups"] = BU_auth_groups(parse_auth_groups(entry["groups"]))
                table.put_item(Item=entry)
                send_success_email("API", API_KEY)
        else:
            print("Error: Invalid SSO format.")

    try:
        if table.scan(FilterExpression=Attr('orderID').eq(body["ID"]))['Items']:
            print("Duplicate order ID. Skipping run...")
            return {"statusCode": 200}
    except Exception:
        pass

    valid = False
    for component in body["Components"]:
        if component == "GUI":
            gui_request()
            valid = True
        elif component == "API":
            api_request()
            valid = True
    
    if not valid:
        print("Invalid component in request.")
        return {"statusCode": 400}
    return {"statusCode": 200}
