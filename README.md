# poetry-s3-utilities

This is a python project that provides utilities to interact with AWS S3. 
It provides the following functionalities:
- List files in a bucket by pattern matching
- Download files from a bucket by pattern matching

## Authors

- Ramesh Doddi, CTO, iRemote, Inc. https://www.iremote.ai/

## Pre-requisites

- Python 3.6 or higher
- Poetry
- AWS credentials configured using `aws configure` as profile
- Login to AWS account having S3 bucket access `aws sso login --profile <profile-name>`
- Update the `.env` file with the `profile-name` and required values
- AWS S3 bucket with files

## Running the project

Install the dependencies using poetry

```bash
poetry install
```

Update the `.env`
Create `lookup-data.csv` file with the following columns:
- `user_id`
- `first_name`
- `last_name`

```bash
poetry run s3-download
```

This will create a `downloads` directory with the downloaded files.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
