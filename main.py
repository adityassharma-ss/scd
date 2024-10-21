import json
import boto3
from botocore.exceptions import ClientError

def get_secret():
    """Fetch the API key from AWS Secrets Manager."""
    secret_name = "scdappapi"  # The name of your secret in AWS
    region_name = "us-east-1"   # Change to your region

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        # Handle the exception here (e.g., logging or raising an error)
        print(f"Error retrieving secret: {e}")
        return None

    # Extract the secret string
    secret = get_secret_value_response['SecretString']

    # Parse the JSON and retrieve the specific key
    try:
        secret_dict = json.loads(secret)
        api_key = secret_dict["OPEN_API_KEY"]  # Replace with your actual key name if different
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Error parsing secret: {e}")
        return None

    return api_key
