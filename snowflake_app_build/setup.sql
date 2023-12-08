-- Setup script for the Hello Snowflake! application.

CREATE APPLICATION ROLE app_public;
CREATE SCHEMA IF NOT EXISTS core;
GRANT USAGE ON SCHEMA core TO APPLICATION ROLE app_public;

CREATE OR REPLACE PROCEDURE CORE.HELLO()
  RETURNS STRING
  LANGUAGE SQL
  EXECUTE AS OWNER
  AS
  BEGIN
    RETURN 'Hello Snowflake!';
  END;

  GRANT USAGE ON PROCEDURE core.hello() TO APPLICATION ROLE app_public;

  CREATE or REPLACE FUNCTION code_schema.multiply(num1 float, num2 float)
  RETURNS float
  LANGUAGE PYTHON
  RUNTIME_VERSION=3.8
  IMPORTS = ('./hello_python.py')
  HANDLER='hello_python.multiply';

GRANT USAGE ON FUNCTION code_schema.multiply(FLOAT, FLOAT) TO APPLICATION ROLE app_public;
