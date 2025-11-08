import sys
import os
from src.Logger import logger
from src.Exception import CustomException
from src.utils import load_pkl_obj
import pandas as pd

class PredictPipeline:
    def predict(self,features):
        try:
            model_file_path=os.path.join('artifacts','trained_model.pkl')
            data_transform_file_path=os.path.join('artifacts','preprocessing_data_transformer.pkl')
            transfomer=load_pkl_obj(data_transform_file_path)
            model=load_pkl_obj(model_file_path)
            logger.info('both data transformation and trained model file loaded successfully')
            transfomred_feature=transfomer.transform(features)
            prediction=model.predict(transfomred_feature)
            logger.info(f"model predicted the transfomrmed value and output is {prediction}")
            return prediction
        except Exception as e:
            raise CustomException(e,sys)


class InputDataTransformation:
    def __init__(  self, gender: str, race_ethnicity: str, parental_level_of_education, lunch: str, test_preparation_course: str, reading_score: int, writing_score: int):
        self.gender=gender
        self.race_ethnicity=race_ethnicity
        self.parental_level_of_education=parental_level_of_education
        self.lunch=lunch
        self.test_preparation_course=test_preparation_course
        self.reading_score=reading_score
        self.writing_score=writing_score

    def get_input_data_as_dataframe(self):
        try:
            input_data_as_dict={
                'gender':[self.gender],
                'race_ethnicity':[self.race_ethnicity],
                'parental_level_of_education':[self.parental_level_of_education],
                'lunch':[self.lunch],
                'test_preparation_course':[self.test_preparation_course],
                'reading_score':[self.reading_score],
                'writing_score':[self.writing_score]
            }
            logger.info("data converting into dataframe")
            return pd.DataFrame(input_data_as_dict)
        except Exception as e:
            raise CustomException(e,sys)


