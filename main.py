import json
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def get_secret_from_aws(self, secret_name):
    """Retrieve the secret value from AWS Secrets Manager."""
    client = boto3.client('secretsmanager', region_name='us-east-1')

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        
        # Fetch the secret string
        secret = get_secret_value_response['SecretString']
        
        # Parse the secret as JSON (if it's stored as a JSON object)
        secret_dict = json.loads(secret)
        
        # Extract the actual API key value
        api_key = secret_dict.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in the secret.")
        
        return api_key

    except NoCredentialsError:
        raise ValueError("AWS credentials not found. Please configure your AWS credentials.")
    except PartialCredentialsError:
        raise ValueError("Incomplete AWS credentials. Please check your AWS credentials.")
    except Exception as e:
        raise ValueError(f"An error occurred while retrieving the secret: {e}")

# Now when you call this method, it will return only the value of "OPENAI_API_KEY"
