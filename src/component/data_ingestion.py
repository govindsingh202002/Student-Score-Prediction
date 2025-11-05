import pandas as pd
from dataclasses import dataclass
import os
from src.Logger import logger
from src.Exception import CustomException
import sys
from sklearn.model_selection import train_test_split

@dataclass
class DataIngestionConfig:
    logger.info('creating data ingestion config files in artifacts folder')
    train_path:str=os.path.join('artifacts','train.csv')
    test_path:str=os.path.join('artifacts','test.csv')
    data_path:str=os.path.join('artifacts','data.csv')

class DataIngestion:
    def __init__(self):
        self.ingestionConfig=DataIngestionConfig()

    def initiate_data_ingestion(self):
        logger.info('data ingestion intiated')
        try:
            df=pd.read_csv('./Notebook/data/stud.csv')
            logger.info('Dataset read completed as a Dataframe')
            os.makedirs('artifacts',exist_ok=True)
            self.dataset_csv=self.ingestionConfig.data_path
            df.to_csv(self.dataset_csv,index=False,header=True)
            logger.info("full dataset saved at artifacts/data.csv")
            self.train_csv=self.ingestionConfig.train_path
            self.test_csv=self.ingestionConfig.test_path
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)
            train_set.to_csv(self.train_csv,index=False,header=True)
            test_set.to_csv(self.test_csv,index=False,header=True)
            logger.info("Train and Test data splitted and saved into corresponded .csv files")
            return (self.ingestionConfig.data_path,self.ingestionConfig.train_path,self.ingestionConfig.test_path)
        except Exception as e:
            raise CustomException(e,sys)

