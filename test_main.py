import boto3
import json
from botocore.exceptions import ClientError


def check_bucket_public_access(s3_client, bucket_name):
    """
    Check if a bucket has any form of public access through:
    1. Bucket Policy
    2. Bucket ACL
    3. Block Public Access settings
    """
    is_public = False
    reasons = []

    # Check bucket policy
    try:
        policy = s3_client.get_bucket_policy(Bucket=bucket_name)
        policy_json = json.loads(policy['Policy'])

        # Check for public access in policy
        for statement in policy_json.get('Statement', []):
            principal = statement.get('Principal', {})
            if (isinstance(principal, dict) and principal.get('AWS') == '*') or principal == '*':
                if statement.get('Effect') == 'Allow':
                    is_public = True
                    reasons.append('Public bucket policy')
    except ClientError as e:
        if e.response['Error']['Code'] != 'NoSuchBucketPolicy':
            print(f"Error checking policy for {bucket_name}: {e}")

    # Check bucket ACL
    try:
        acl = s3_client.get_bucket_acl(Bucket=bucket_name)
        for grant in acl.get('Grants', []):
            grantee = grant.get('Grantee', {})
            if grantee.get('URI') == 'http://acs.amazonaws.com/groups/global/AllUsers':
                is_public = True
                reasons.append('Public ACL')
    except ClientError as e:
        print(f"Error checking ACL for {bucket_name}: {e}")

    # Check block public access settings
    try:
        public_access = s3_client.get_public_access_block(Bucket=bucket_name)
        config = public_access['PublicAccessBlockConfiguration']
        if not all([
            config.get('BlockPublicAcls', False),
            config.get('BlockPublicPolicy', False),
            config.get('IgnorePublicAcls', False),
            config.get('RestrictPublicBuckets', False)
        ]):
            is_public = True
            reasons.append('Public access not fully blocked')
    except ClientError as e:
        if e.response['Error']['Code'] != 'NoSuchPublicAccessBlockConfiguration':
            print(f"Error checking public access block for {bucket_name}: {e}")

    return is_public, reasons


def main():
    # AWS credentials
    AWS_ACCESS_KEY = ''
    AWS_SECRET_KEY = ''
    AWS_REGION = 'eu-west-2'  # Change to your region

    # Initialize S3 client with credentials
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION
    )

    try:
        # List all buckets
        response = s3_client.list_buckets()
        buckets = response['Buckets']

        print(f"\nChecking {len(buckets)} buckets for public access...")
        print("-" * 60)

        public_buckets = []

        for bucket in buckets:
            bucket_name = bucket['Name']
            is_public, reasons = check_bucket_public_access(s3_client, bucket_name)

            if is_public:
                public_buckets.append({
                    'name': bucket_name,
                    'reasons': reasons
                })
                print(f"\n⚠️  {bucket_name}")
                print(f"   Reasons: {', '.join(reasons)}")

        print("\n" + "=" * 60)
        print(f"Found {len(public_buckets)} buckets with public access")
        print("=" * 60)

        if public_buckets:
            print("\nRecommended actions:")
            print("1. Enable Block Public Access at the account level")
            print("2. Review and modify bucket policies")
            print("3. Review and modify bucket ACLs")
            print("4. Enable Block Public Access for individual buckets")

    except ClientError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()