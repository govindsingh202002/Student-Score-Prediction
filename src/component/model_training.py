import os
import sys
import pandas as pd
import numpy as np
from dataclasses import dataclass
from src.component.data_transformation import DataTransformation
from src.Logger import logger
from src.Exception import CustomException
from sklearn.linear_model import LinearRegression,Ridge,ElasticNet,Lasso
from xgboost import XGBRegressor
from catboost import CatBoostRegressor
from sklearn.ensemble import RandomForestRegressor,AdaBoostRegressor,GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
from src.utils import save_object

@dataclass
class ModelTrainConfig:
    model_training_file_path=os.path.join('artifacts','trained_model.pkl')


class ModelTrainer:
    def __init__(self):
        try:
            self.ModelTrainConfig_obj=ModelTrainConfig()
            self.DataTransformation_obj=DataTransformation()

            self.transformed_train_data_path,self.transformed_test_data_path,_=self.DataTransformation_obj.initiate_data_transformation()

        except Exception as e:
            raise CustomException(e,sys)
        
    def get_model_definition(self):
        try:
            self.models={
                'linear_regression':LinearRegression(),
                'ridge':Ridge(),
                'lasso':Lasso(),
                'elasticnet':ElasticNet(),
                'xgboost':XGBRegressor(),
                'catboost':CatBoostRegressor(verbose=False),
                'randomforest':RandomForestRegressor(),
                'adaboost':AdaBoostRegressor(),
                'svr':SVR(),
                'decisiontree':DecisionTreeRegressor(),
                'knn':KNeighborsRegressor(),
                'gradientboosting':GradientBoostingRegressor()
            }
            logger.info("all models definition created")
            self.parameters={
                'linear_regression':{},
                'ridge':{},
                'lasso':{},
                'elasticnet':{},
                'xgboost':{
                        'learning_rate':[.1,.01,.05,.001],
                        'n_estimators': [8,16,32,64,128,256]
                },
                'catboost':{
                        'depth': [6,8,10],
                        'learning_rate': [0.01, 0.05, 0.1],
                        'iterations': [30, 50, 100]},
                'randomforest':{
                    'n_estimators': [8,16,32,64,128,256]
                    },
                'adaboost':{
                        'learning_rate':[.1,.01,0.5,.001],
                        # 'loss':['linear','square','exponential'],
                        'n_estimators': [8,16,32,64,128,256]},
                'svr':{},
                'decisiontree':{
                    'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson']
                    },
                'knn':{},
                'gradientboosting':{
                        'learning_rate':[.1,.01,.05,.001],
                        'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
                        'n_estimators': [8,16,32,64,128,256]
                }
            }
            logger.info("all models cross validation parameters created")
            return (self.models,self.parameters)
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_model_training(self):
        try:
            self.models_list,self.models_parameters=self.get_model_definition()
            self.train_data=pd.read_csv(self.transformed_train_data_path)
            self.test_data=pd.read_csv(self.transformed_test_data_path)

            self.target_column='math_score'

            self.y_train=self.train_data[self.target_column]
            self.X_train=self.train_data.drop(columns=[self.target_column],axis=1)
            self.y_test=self.test_data[self.target_column]
            self.X_test=self.test_data.drop(columns=[self.target_column],axis=1)
            logger.info("train and test data loaded and splited into dependent and independent")
            models_training_report={}

            for model_name,model in self.models_list.items():
                grid_search_cv=GridSearchCV(model,self.models_parameters[model_name],cv=3)
                grid_search_cv.fit(self.X_train,self.y_train)

                model.set_params(**grid_search_cv.best_params_)
                model.fit(self.X_train,self.y_train)

                y_test_pred=model.predict(self.X_test)
                model_r2_score=r2_score(self.y_test,y_test_pred)
                print(model_name,model_r2_score)
                models_training_report[model_name]=[model,model_r2_score]

            logger.info("model trained and report created")
            models_training_report=sorted(models_training_report.items(),key=lambda x : x[1][1],reverse=True)

            models_training_report=list(models_training_report)
            best_model_name,(best_model,best_models_r2_score)=models_training_report[0]

            print(f"Best model is {best_model_name} and r2 score is {best_models_r2_score}")

            save_object(self.ModelTrainConfig_obj.model_training_file_path,best_model)

        except Exception as e:
            raise CustomException(e,sys)


def main():
    obj=ModelTrainer()
    obj.initiate_model_training()

if __name__=='__main__':
    main()