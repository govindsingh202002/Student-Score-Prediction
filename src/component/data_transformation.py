import pandas as pd
from src.Logger import logger
from src.Exception import CustomException
from dataclasses import dataclass
import os
import sys
from src.component.data_ingestion import DataIngestion
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from src.utils import save_files,save_object

@dataclass
class DataTransformerConfig:
    preprocessing_data_transformer_path=os.path.join('artifacts','preprocessing_data_transformer.pkl')
    transformed_train_data=os.path.join('artifacts','train_transfomed.csv')
    transformed_test_data=os.path.join('artifacts','test_transformed.csv')

class DataTransformation:
    def __init__(self):
        self.datatransformerconfig=DataTransformerConfig()
        logger.info("Data transformation config completed")
        self.dataingestion_object=DataIngestion()
        logger.info("Data Ingestion object created")

    def get_data_transfer_object(self,data_path,target_column):
        logger.info("Data transfer object creation started")
        try:
            self.numerical_columns=[]
            self.categorical_columns=[]
            self.data_frame=pd.read_csv(data_path)
            for column in self.data_frame.columns:
                if column!=target_column:
                    if self.data_frame[column].dtype == "O":
                        self.categorical_columns.append(column)
                    else:
                        self.numerical_columns.append(column)

            logger.info("numerical and categorical columns list created")

            '''on numerical data we will apply EDA, standardization and on categorical data we will apply EDA and Encoding'''

            self.numerical_pipeline=Pipeline(steps=[
                ('imputer',SimpleImputer(strategy='mean')),
                ('scaler',StandardScaler())
            ])
            self.categorical_pipeline=Pipeline(steps=[
                ('imputer',SimpleImputer(strategy='most_frequent')),
                ('encoder',OneHotEncoder())
            ])

            self.transformer=ColumnTransformer(
                [
                    ('numerical pipeline',self.numerical_pipeline,self.numerical_columns),
                    ('categorical pipeline',self.categorical_pipeline,self.categorical_columns)
                ]
            )
            logger.info("numerical and categorical pipeline created for data transformation")
            return self.transformer

        except Exception as e:
            raise CustomException(e,sys)


    def initiate_data_transformation(self):
        try:
            self.target_column='math_score'
            _,self.train_data_path,self.test_data_path=self.dataingestion_object.initiate_data_ingestion()
            logger.info("Initiated data ingestion to get train and test dataset path")
            self.data_transformer_object=self.get_data_transfer_object(self.train_data_path,self.target_column)
            '''now we have train & test datasets path and skelton of data transformation object so now
               we will load of datasets and split them into dependent and independent features then 
               we are going to do data transformation then save these splitted data and this transformer 
               in a pkl file
            '''
            self.train_dataframe=pd.read_csv(self.train_data_path)
            self.test_dataframe=pd.read_csv(self.test_data_path)
            logger.info("train and test data sucesfully loaded")

            self.y_train=self.train_dataframe[self.target_column]
            self.y_test=self.test_dataframe[self.target_column]
            self.X_train=self.train_dataframe.drop(columns=[self.target_column],axis=1)
            self.X_test=self.test_dataframe.drop(columns=[self.target_column],axis=1)

            self.X_train=self.data_transformer_object.fit_transform(self.X_train)
            self.X_test=self.data_transformer_object.transform(self.X_test)

            self.train_dataframe=pd.concat([pd.DataFrame(self.X_train),self.y_train],axis=1)
            self.test_dataframe=pd.concat([pd.DataFrame(self.X_test),self.y_test],axis=1)

            save_files(self.datatransformerconfig.transformed_train_data,self.train_dataframe)
            save_files(self.datatransformerconfig.transformed_test_data,self.test_dataframe)

            save_object(self.datatransformerconfig.preprocessing_data_transformer_path,self.data_transformer_object)

            logger.info("Data transformatiob completed")
            return (self.datatransformerconfig.transformed_train_data,
                    self.datatransformerconfig.transformed_test_data,
                    self.datatransformerconfig.preprocessing_data_transformer_path
                    )


        except Exception as e:
            raise CustomException(e,sys)


def main():
    obj=DataTransformation()
    a,b,c=obj.initiate_data_transformation()
    print(a,b,c)

if __name__=="__main__":
    main()