from dotenv import load_dotenv
import openai
import boto3
from botocore.exceptions import ClientError
import os

class Config:
    def __init__(self):
        # Load .env file for local development
        load_dotenv()
        
        # First, try getting OpenAI key from the environment variables (.env for local)
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        
        # If key is not set in the environment, try fetching it from AWS Secrets Manager
        if not self.openai_api_key:
            self.openai_api_key = self.get_secret()
        
        # Validate the key
        self._validate_openai_key()

        # Initialize OpenAI API with the key
        self._initialize_openai_api()

    def _validate_openai_key(self):
        """Ensure that the OpenAI API key exists."""
        if not self.openai_api_key:
            raise ValueError("OpenAI API key is missing! Please set it in the env file or AWS Secrets Manager.")

    def _initialize_openai_api(self):
        """Initialize OpenAI with the API key."""
        openai.api_key = self.openai_api_key

    def get_secret(self):
        """Fetch the secret from AWS Secrets Manager"""
        secret_name = "openai_key"  # The name of your secret in AWS
        region_name = "us-east-1"   # Change to your region

        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            raise e

        # Extract the secret string (this is assuming your secret is stored as a plain string)
        secret = get_secret_value_response['SecretString']

        return secret

    def get_openai_api_key(self):
        """Optionally provide a method to get the OpenAI API key programmatically."""
        return self.openai_api_key
