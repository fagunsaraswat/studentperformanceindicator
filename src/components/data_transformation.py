import sys
import os
from dataclasses import dataclass

# We use @dataclass decorator, because inside any traditional class, to define the class variables we basically use __init__, 
# but if we use this @dataclass decorator, it enables us to define the class variables and their data types directly.

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer  # used in creating pipeline
from sklearn.impute import SimpleImputer  # missing values
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.utils import save_object

# StandardScaler is used to bring all the values in a range or scaling them in a similar range, another scaler is minmax scaler
# OneHotEncoder is used for forming new column for categorical values

from src.exception import CustomException
from src.logger import logging

# For inputs to data transformation component
@dataclass
class DataTransformationConfig:
    preproccessor_obj_file_path = os.path.join('artifacts', "preprocessor.pkl")  # pickle file/model file

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        '''
        This function is responsible for data transformation
        '''
        try:
            numerical_columns = ["writing score", "reading score"]
            categorical_columns = [
                "gender", 
                "race/ethnicity", 
                "parental level of education",
                "lunch",
                "test preparation course"
            ]

            # Numerical pipeline which'll run on the training dataset -> fit_transform
            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),  # for handling missing values
                    ("scaler", StandardScaler(with_mean=False))
                ]
            )

            # Missing values, converting into numerical
            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder()),  # or target guided encoder in case we had a lot of categories
                    ("scaler", StandardScaler(with_mean=False))
                ]
            )

            logging.info("Numerical Columns standard scaling completed")
            logging.info(f"Numerical Columns: {numerical_columns}")

            logging.info("Categorical columns encoding completed")
            logging.info(f"Categorical Columns: {categorical_columns}")

            # Combining numerical and categorical pipeline
            preprocessor = ColumnTransformer(
                [
                    ("Numerical_pipeline", num_pipeline, numerical_columns),  # pipeline name, which pipeline, for what variables
                    ("Categorical_pipeline", cat_pipeline, categorical_columns)
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Train and test data read successfully")

            logging.info("Obtaining preprocessing object")

            preprocessing_obj = self.get_data_transformer_object()

            target_column_name = "math score"
            numerical_columns = ["writing score", "reading score"]

            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]
            
            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info("Applying preprocessing object on training dataframe and testing dataframe")

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]

            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info("Saved preprocessing object")

            save_object(
                file_path=self.data_transformation_config.preproccessor_obj_file_path,
                obj=preprocessing_obj
            )

            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preproccessor_obj_file_path,
            )
        
        except Exception as e:
            raise CustomException(e, sys)
