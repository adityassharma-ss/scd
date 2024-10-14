# AWS IAM User Activity Tracker 📊

[![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)
[![Boto3](https://img.shields.io/badge/Boto3-Library-orange)](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
[![AWS](https://img.shields.io/badge/AWS-CloudTrail%20|%20IAM-yellow)](https://aws.amazon.com/)

This Python script automates the process of listing all IAM users in your AWS account and analyzing their activities over the past 90 days. Leveraging **AWS CloudTrail**, it tracks how often users access AWS and outputs relevant information for auditing purposes.

## ✨ Features

- **List All IAM Users**: Retrieve all IAM users in your AWS account.
- **Track User Activity**: Analyze CloudTrail logs to see which users have performed actions in the last 90 days.
- **Time-based Analysis**: Define custom time periods to audit user activity.
- **CSV Output**: (Upcoming feature) Export results to CSV for reporting.

## 🛠️ Installation

### Prerequisites
- Python 3.x
- AWS credentials configured via environment variables or `aws configure` command.
- Install the required Python packages:

```bash
pip install -r requirements.txt
