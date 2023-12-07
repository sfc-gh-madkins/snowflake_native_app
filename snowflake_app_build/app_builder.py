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
    print(f"Role: {session.get_current_role()}")
    print(f"Warehouse: {session.get_current_warehouse()}")


def parse_release_tag(version_string):
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
