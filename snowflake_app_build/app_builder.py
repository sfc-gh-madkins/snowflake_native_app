import sys
from snowflake.snowpark import Session
import os

connection_parameters = {
  "account": os.getenv("SNOWFLAKE_PROD_BUILD_ACCOUNT"),
  "user": os.getenv("SNOWFLAKE_PROD_BUILD_USERNAME"),
  "password": os.getenv("SNOWFLAKE_PROD_BUILD_PASSWORD"),
  "role": os.getenv("SNOWFLAKE_PROD_BUILD_ROLE"),
  "warehouse": os.getenv("SNOWFLAKE_PROD_BUILD_WAREHOUSE"),
}


def main():
    release_tag =  os.getenv("PACKAGE_RELEASE_VERSION")
    major, minor, patch = parse_release_tag(release_tag)
    print("Release Version:")
    print(major, minor, patch)

    session = Session.builder.configs(connection_parameters).create()

    # Retrieve and print the current Snowflake context details
    print("Current Snowflake Context:")
    print(f"Account: {session.get_session_info().account}")
    print(f"User: {session.get_session_info().user}")
    print(f"Role: {session.get_session_info().role}")
    print(f"Database: {session.get_session_info().database}")
    print(f"Schema: {session.get_session_info().schema}")
    print(f"Warehouse: {session.get_session_info().warehouse}")


def parse_version(version_string):
    # Split the string to isolate the version part
    parts = version_string.split('/')
    if len(parts) != 3:
        raise ValueError("Invalid version string format")

    # Extract the version numbers
    version_numbers = parts[2][1:]  # Remove the leading 'v'
    major, minor, patch = version_numbers.split('.')

    return int(major), int(minor), int(patch)


if __name__ == "__main__":
    main()