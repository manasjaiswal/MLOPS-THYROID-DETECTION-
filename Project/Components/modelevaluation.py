from Project.Logger.logging import logging
from Project.Exception.exception import ThyroidException
import pandas as pd
import numpy as np
import os,sys
from Project.Entity.artifactentity import ModelEvaluationArtifact,ModelTrainerArtifact
from Project.Entity.configentity import Model_Evaluation_Entity
from Project.Constants.constants import *
from Project.Helper_functions.helper import read_yaml_file,write_yaml_file,loading_object
import re
import yaml
from Project.Entity.modelfactory import evaluate_classification_model,MetricInfoArtifact2

class ModelEvaluation:
    def __init__(self,model_evaluation_config:Model_Evaluation_Entity,model_trainer_artifact:ModelTrainerArtifact):
        try:
            logging.info(f"{':'*20}MODEL EVALUATION LOG STARTED{':'*20}")
            self.model_evaluation_config=model_evaluation_config
            self.model_trainer_artifact=model_trainer_artifact
        except Exception as e:
            raise ThyroidException(e,sys) from e

    def model_evaluation(self)->ModelEvaluationArtifact:
        try:
            logging.info(f"Reading testing data from the earliest ingested folder for analysis of both models")
            trained_model=self.model_trainer_artifact.model_object
            config_info:dict=read_yaml_file(file_path=CONFIG_FILE_PATH)
            data_ingestion_folder=os.path.join(ROOT_DIR,config_info[TRAINING_PIPELINE_CONFIG_KEY][TRAINING_PIPELINE_NAME_KEY],config_info[TRAINING_PIPELINE_CONFIG_KEY][TRAINING_PIPELINE_ARTIFACT_DIR_KEY],DATA_INGESTION_ARTIFACT_DIR_KEY)
            first_data_folder=os.listdir(data_ingestion_folder)[0]
            test_path=os.path.join(data_ingestion_folder,first_data_folder,config_info[DATA_INGESTION_CONFIG_KEY][DATA_INGESTION_INGESTED_DATA_DIR_KEY],config_info[DATA_INGESTION_CONFIG_KEY][DATA_INGESTION_INGESTED_TEST_DIR_KEY],os.path.basename(config_info[DATA_INGESTION_CONFIG_KEY][DATA_INGESTION_DOWNLOAD_URL_KEY]))
            train_path=os.path.join(data_ingestion_folder,first_data_folder,config_info[DATA_INGESTION_CONFIG_KEY][DATA_INGESTION_INGESTED_DATA_DIR_KEY],config_info[DATA_INGESTION_CONFIG_KEY][DATA_INGESTION_INGESTED_TRAIN_DIR_KEY],os.path.basename(config_info[DATA_INGESTION_CONFIG_KEY][DATA_INGESTION_DOWNLOAD_URL_KEY]))
            test_data=pd.read_csv(test_path,index_col=0)
            train_data=pd.read_csv(train_path,index_col=0)
            test_data[COLUMN_TARGET_COLUMN]=test_data[COLUMN_TARGET_COLUMN].apply(lambda x:re.sub(r"\.\W\d+","",x))
            train_data[COLUMN_TARGET_COLUMN]=train_data[COLUMN_TARGET_COLUMN].apply(lambda x:re.sub(r"\.\W\d+","",x))
            schema_content:dict=read_yaml_file(file_path=SCHEMA_FILE_PATH)
            d:dict=schema_content[SCHEMA_TARGET_COLUMN_CATEGORIES_KEY]
            train_data[COLUMN_TARGET_COLUMN]=train_data[COLUMN_TARGET_COLUMN].map(d)
            test_data[COLUMN_TARGET_COLUMN]=test_data[COLUMN_TARGET_COLUMN].map(d)
            X_train=np.array(train_data.drop(columns=COLUMN_TARGET_COLUMN))
            X_test=np.array(test_data.drop(columns=COLUMN_TARGET_COLUMN))
            y_train=train_data[COLUMN_TARGET_COLUMN]
            y_test=test_data[COLUMN_TARGET_COLUMN]
            model_evaluation_file_path=self.model_evaluation_config.model_evaluation_file_path
            if os.path.exists(path=model_evaluation_file_path):
                evaluation_file_content:dict=read_yaml_file(file_path=model_evaluation_file_path)
                if evaluation_file_content is None:
                    evaluation_file_content={}     
            else:
                evaluation_file_content={}    
            if isinstance(evaluation_file_content,dict):
                if len(evaluation_file_content.keys())==0:
                    logging.info('No model in the production trained model object will be the best model')
                    evaluation_file_content[BEST_MODEL_KEY]=type(trained_model).__name__
                    evaluation_file_content[MODEL_PATH_KEY]=self.model_trainer_artifact.trained_model_file_path
                elif BEST_MODEL_KEY in evaluation_file_content.keys():
                    logging.info('Comparing the best model in production with previously trained model')
                    production_model=loading_object(file_path=evaluation_file_content[MODEL_PATH_KEY])
                    li=[trained_model,production_model]
                    best_model:MetricInfoArtifact2=evaluate_classification_model(model_list=li,X_train=X_train,X_test=X_test,y_test=y_test,y_train=y_train)
                    if best_model.index_number==0:
                        logging.info("trained model outperformed the best model in the production")
                        if HISTORY_KEY in evaluation_file_content.keys():
                            d={}
                            d[BEST_MODEL_KEY]=evaluation_file_content[BEST_MODEL_KEY]
                            d[MODEL_PATH_KEY]=evaluation_file_content[MODEL_PATH_KEY]
                            d['time_stamp']=self.model_evaluation_config.time_stamp
                            evaluation_file_content[HISTORY_KEY]=d
                            evaluation_file_content[BEST_MODEL_KEY]=trained_model
                            evaluation_file_content[MODEL_PATH_KEY]=self.model_trainer_artifact.trained_model_file_path
                    else:
                        logging.info("trained model is not best than the best model in the production")
            write_yaml_file(file_path=model_evaluation_file_path,content=evaluation_file_content)                            
            model_evaluation_artifact=ModelEvaluationArtifact(
                model_evaluation_file_path=model_evaluation_file_path, 
                is_evaluated=True, 
                model_in_production=evaluation_file_content[BEST_MODEL_KEY],
                trained_model=self.model_trainer_artifact.model_object,
                trained_model_file_path=self.model_trainer_artifact.trained_model_file_path
            )
            logging.info(f"Model Evaluation Artifact:{model_evaluation_artifact}")
            return model_evaluation_artifact
            
        except Exception as e:
            raise ThyroidException(e,sys) from e

    def initiate_model_evaluation(self)->ModelEvaluationArtifact:
        try:
            return self.model_evaluation()
        except Exception as e:
            raise ThyroidException(e,sys) from e        

    def __del__(self):
        logging.info(f"{':'*20}MODEL EVALUATION LOG ENDED{':'*20}")        