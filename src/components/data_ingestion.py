# reading the dataset from specific data source -> Splitting the data -> Data Transformation

import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass #used for creating class variables


# there might be some inputs required by data ingestion component like where we have to save raw data, training data, test data, etc. All the kinds of inputs will be created in another class.
@dataclass
class DataIngestionConfig:
    train_data_path: str=os.path.join('artifacts',"train.csv") #outputs will be stored in artifiact folder
    test_data_path: str = os.path.join('artifacts',"test.csv")
    raw_data_path: str = os.path.join('artifacts',"rawdata.csv")



'''for only defining variables, using data class is fine, 
but if we need to make functions inside class, init constructor method is better
'''

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):

            'reading from database: can create mongodb client/APIs/MySql,etc in utils file'

            logging.info("Entered the Data Ingestion method or Component")

            try:
                df = pd.read_csv('notebook\data\StudentsPerformance.csv')
                logging.info('Read the csv dataset as dataframe')

                #creating artificats folder
                os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
                
                #converting it into csv
                df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)

                logging.info("Train test data split initiated")
                train_set,test_set = train_test_split(df,test_size=0.2,random_state=42)

                train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
                test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

                logging.info("Ingestion of the data in completed")


                # we will be needing the following information in data transformation process
                return(
                    self.ingestion_config.train_data_path,
                    self.ingestion_config.test_data_path
                )
            
            except Exception as e: 
                raise CustomException(e, sys)
            

#initate and run

if __name__=="__main__":
    obj = DataIngestion()
    obj.initiate_data_ingestion()




'''
import os: Imports the os module for handling file paths.
from dataclasses import dataclass: Imports the dataclass decorator from the dataclasses module.
@dataclass: A decorator that automatically generates special methods like __init__() and __repr__() for the class.
class DataIngestionConfig: A data class that defines the configuration for data ingestion, with default paths for train, test, and raw data files.
'''
