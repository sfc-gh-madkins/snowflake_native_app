-- Setup script for the Hello Snowflake! application.

CREATE APPLICATION ROLE app_public;

CREATE OR ALTER VERSIONED SCHEMA code;
GRANT USAGE ON SCHEMA code TO APPLICATION ROLE app_public;


CREATE OR REPLACE PROCEDURE code.hello()
  RETURNS STRING
  LANGUAGE SQL
  EXECUTE AS OWNER
  AS
  BEGIN
    RETURN 'Hello Snowflake!';
  END;
  GRANT USAGE ON PROCEDURE code.hello() TO APPLICATION ROLE app_public;


CREATE or REPLACE FUNCTION code.multiply(num1 float, num2 float)
  RETURNS float
  LANGUAGE PYTHON
  RUNTIME_VERSION=3.8
  IMPORTS = ('/src/hello_python.py')
  HANDLER='hello_python.multiply';
GRANT USAGE ON FUNCTION code.multiply(FLOAT, FLOAT) TO APPLICATION ROLE app_public;


CREATE OR REPLACE FUNCTION code.addone(i int)
RETURNS INT
LANGUAGE PYTHON
RUNTIME_VERSION = '3.8'
HANDLER = 'addone_py'
AS
$$
def addone_py(i):
  return i+1
$$;
GRANT USAGE ON FUNCTION code.addone(int) TO APPLICATION ROLE app_public;
