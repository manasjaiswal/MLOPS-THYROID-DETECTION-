from Project.Exception.exception import ThyroidException
from Project.Logger.logging import logging
import os,sys
from Project.Entity.configentity import *
from Project.Entity.artifactentity import *
from Project.Config.configuration import Configuration
from Project.Components.dataingestion import DataIngestion
from Project.Components.datavalidation import DataValidation
from Project.Components.datatransformation import DataTransformation
from Project.Components.modeltrainer import ModelTrainer
from Project.Components.modelevaluation import ModelEvaluation
from Project.Components.modelpusher import Model_Pusher
from Project.Helper_functions.helper import read_yaml_file
from Project.Constants.constants import CONFIG_FILE_PATH
from typing import List

class Pipeline:
    def __init__(self,configuration:Configuration=Configuration(config_file_path=CONFIG_FILE_PATH)):
        try:
            logging.info(f"{':'*20}PIPELINE LOG STARTED{':'*20}")
            self.configuration=configuration
        except Exception as e:
            raise ThyroidException(e,sys) from e

    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            data_ingestion_config:Data_Ingestion_Entity=self.configuration.get_data_ingestion_config()
            di=DataIngestion(data_ingestion_config=data_ingestion_config)
            data_ingestion_artifact:DataIngestionArtifact=di.initiate_data_ingestion()
            return data_ingestion_artifact
        except Exception as e:
            raise ThyroidException(e,sys) from e        

    def start_data_validation(self)->List:
        try:
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_config:Data_Validation_Entity=self.configuration.get_data_validation_config()
            dv=DataValidation(data_ingestion_artifact=data_ingestion_artifact,data_validation_config=data_validation_config)
            data_validation_artifact=dv.initiate_data_validation()
            return [data_ingestion_artifact,data_validation_artifact]
        except Exception as e:
            raise ThyroidException(e,sys) from e        

    def start_data_transformation(self)->DataTransformationArtifact:
        try:
            data_ingestion_artifact,data_validation_artifact=self.start_data_validation()
            data_transformation_config:Data_Transfomation_Entity=self.configuration.get_data_transformation_config()
            dt=DataTransformation(data_ingestion_artifact=data_ingestion_artifact,data_validation_artifact=data_validation_artifact,data_transformation_config=data_transformation_config)
            data_transformation_artifact=dt.initiate_data_transformation()
            return data_transformation_artifact
        except Exception as e:
            raise ThyroidException(e,sys) from e

    def start_model_training(self)->ModelTrainerArtifact:
        try:
            data_transformation_artifact:DataTransformationArtifact=self.start_data_transformation()
            model_trainer_config:Model_Trainer_Entity=self.configuration.get_model_trainer_config()
            mt=ModelTrainer(data_transformation_artifact=data_transformation_artifact,model_trainer_config=model_trainer_config)
            model_trainer_artifact=mt.initiate_model_training()
            return model_trainer_artifact
        except Exception as e:
            raise ThyroidException(e,sys) from e        

    def start_model_evaluation(self)->ModelEvaluationArtifact:
        try:
            model_trainer_artifact:ModelTrainerArtifact=self.start_model_training()
            model_evaluation_config:Model_Evaluation_Entity=self.configuration.get_model_evaluation_config()
            me=ModelEvaluation(model_evaluation_config=model_evaluation_config,model_trainer_artifact=model_trainer_artifact)
            model_evaluation_artifact=me.initiate_model_evaluation()
            return model_evaluation_artifact
        except Exception as e:
            raise ThyroidException(e,sys) from e        

    def start_model_pushing(self)->ModelPusherArtifact:
        try:
            model_evaluation_artifact:ModelEvaluationArtifact=self.start_model_evaluation()
            model_pusher_config:Model_Pusher_Entity=self.configuration.get_model_pusher_config()
            mp=Model_Pusher(model_pusher_config=model_pusher_config,model_evaluation_artifact=model_evaluation_artifact)
            return mp.initiate_model_pushing()
        except Exception as e:
            raise ThyroidException(e,sys) from e                

    def start_pipeline(self)->None:
        try:
            logging.info("Starting Thyroid Prediction Pipeline")
            model_pusher_artifact=self.start_model_pushing()
            logging.info("Thyroid pipeline ran successfully")
        except Exception as e:
            raise ThyroidException(e,sys) from e       

    def __del__(self)->None:
        logging.info(f"{':'*20}PIPELINE LOG ENDED{':'*20}")         