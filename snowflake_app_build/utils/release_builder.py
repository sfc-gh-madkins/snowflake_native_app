import sys
from snowflake.snowpark import Session
import os

connection_parameters = {
  "account": os.getenv("SNOWFLAKE_PROD_BUILD_ACCOUNT"),
  "user": os.getenv("SNOWFLAKE_PROD_BUILD_USERNAME"),
  "password": os.getenv("SNOWFLAKE_PROD_BUILD_PASSWORD"),
  "role": os.getenv("SNOWFLAKE_PROD_BUILD_ROLE"),
  "warehouse": os.getenv("SNOWFLAKE_PROD_BUILD_WAREHOUSE"),
  "database": os.getenv("SNOWFLAKE_PROD_BUILD_APPLICATION_PACKAGE")
}


def main():
    release_tag =  os.getenv("PACKAGE_RELEASE_VERSION")
    major, minor, patch = parse_release_tag(release_tag)
    print("Release Version:")
    print(major, minor, patch)

    # Retrieve Snowflake context
    session = Session.builder.configs(connection_parameters).create()

    #Copy files to snowflake
    repo_files = list_files_and_folders(os.getcwd())
    for file in repo_files:
        query = f'''
            put file://{file} @provider.github_repo{file[:file.rfind('/')].replace(os.getcwd(),'')}
            auto_compress=false overwrite=true;
        '''
        session.sql(query).collect()

    # Upgrade Snowflake Application Package
    application_package = os.getenv("SNOWFLAKE_PROD_BUILD_APPLICATION_PACKAGE")

    version_upgrade_sql = f'''
    ALTER APPLICATION PACKAGE {application_package}
        ADD VERSION v{major}_{minor} USING '@{application_package}.provider.github_repo';
    '''
    #session.sql(version_upgrade_sql).collect()

    if int(patch) > 0:
        patch_upgrade_sql = f'''
        ALTER APPLICATION PACKAGE {application_package}
         ADD PATCH {patch} FOR VERSION v{major}_{minor}
         USING '@{application_package}.provider.github_repo';
        '''
        session.sql(patch_upgrade_sql).collect()

    release_directive_sql = f'''
    ALTER APPLICATION PACKAGE {application_package}
      SET DEFAULT RELEASE DIRECTIVE
      VERSION = v{major}_{minor}
      PATCH = {patch};
    '''
    session.sql(release_directive_sql).collect()



def parse_release_tag(version_string):
    # Split the string to isolate the version part
    parts = version_string.split('/')
    if len(parts) != 3:
        raise ValueError("Invalid version string format")

    # Extract the version numbers
    version_numbers = parts[2][1:]  # Remove the leading 'v'
    major, minor, patch = version_numbers.split('.')

    return major, minor, patch

def list_files_and_folders(path):
    result = []
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs]
        for file in files:
            result.append(os.path.join(root, file))

    return result


if __name__ == "__main__":
    main()
