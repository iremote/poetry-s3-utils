import boto3
import os
import botocore.exceptions
import csv
from dotenv import load_dotenv

load_dotenv()

BUCKET_NAME = os.getenv("BUCKET_NAME")
S3_REGION = os.getenv("S3_REGION")
AWS_PROFILE = os.getenv("AWS_PROFILE")
INVESTORS_FILE = os.getenv("INVESTORS_FILE")
DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR")
FILE_PATTERN_KEYWORD = os.getenv("FILE_PATTERN_KEYWORD").lower()

boto3.setup_default_session(profile_name=AWS_PROFILE)
s3_client = boto3.client('s3', region_name=S3_REGION)

os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_files():
    with open(INVESTORS_FILE, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            user_id = row["user_id"].strip()
            first_name = row["first_name"].strip()
            last_name = row["last_name"].strip()
            prefix = f"user/{user_id}/"

            try:
                response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)

                if "Contents" in response:
                    for obj in response["Contents"]:
                        s3_key = obj["Key"]
                        filename = os.path.basename(s3_key)

                        if FILE_PATTERN_KEYWORD in filename.lower():
                            local_filename = f"{first_name}-{last_name}-{FILE_PATTERN_KEYWORD}.pdf"
                            local_path = os.path.join(DOWNLOAD_DIR, local_filename)

                            print(f"Downloading {s3_key} to {local_path}...")
                            s3_client.download_file(BUCKET_NAME, s3_key, local_path)
                            print(f"Downloaded {local_filename}")
                else:
                    print(f"No files found for user: {user_id}")
            except botocore.exceptions.NoCredentialsError:
                print("Error: AWS credentials not found. Ensure you are authenticated.")
            except botocore.exceptions.PartialCredentialsError:
                print("Error: Incomplete AWS credentials configuration.")
            except botocore.exceptions.ClientError as e:
                print(f"AWS ClientError: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

    print("Download complete.")


if __name__ == "__main__":
    download_files()
