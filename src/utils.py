import pandas as pd
from src.Exception import CustomException
from src.Logger import logger
import sys
import os
import pickle

def save_files(file_path,file):
    try:
        dir_name=os.path.dirname(file_path)
        os.makedirs(dir_name, exist_ok=True)
        if not isinstance(file,pd.DataFrame):
            file=pd.DataFrame(file)
        file.to_csv(file_path,index=False,header=True)
        logger.info(f"at location {file}, we have saved this .csv file succesfully")
    except Exception as e:
        raise CustomException(e,sys)
    
def save_object(file_path,file):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        
        with open(file_path,'wb') as file_path:
            pickle.dump(file,file_path)

        logger.info(f"at location {file_path} we have saved this .pkl file succesfully")

    except Exception as e:
        raise CustomException(e,sys)