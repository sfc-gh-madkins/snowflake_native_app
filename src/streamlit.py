# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session

#from snowflake.ml.registry import model_registry

MODEL_REGISTRY_DB = 'MILES'
MODEL_REGISTRY_SCHEMA = 'ML'
MODEL_NAME = 'MY_RANDOM_FOREST_REGRESSOR'
MODEL_VERSION = 'V1'


# Write directly to the app
st.title("Snowflake Prediction Application")
