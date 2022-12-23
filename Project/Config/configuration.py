from Project.Exception.exception import ThyroidException
from Project.Logger.logging import logging
from Project.Constants.constants import *
from Project.Entity.configentity import *
import os,sys
from Project.Helper_functions.helper import read_yaml_file

class Configuration:

    def __init__(self,config_file_path:str,time_stamp:str=get_current_time_stamp())->None:
        try:
            self.config_info=read_yaml_file(file_path=config_file_path)
            self.time_stamp=time_stamp
        except Exception as e:
            raise ThyroidException(e,sys) from e

    def get_data_ingestion_config(self)->Data_Ingestion_Entity:
        try:
            pipeline_entity=self.get_training_pipeline_config()
            data_ingestion_config_info=self.config_info[DATA_INGESTION_CONFIG_KEY]
            artifact_dir=os.path.join(pipeline_entity.training_pipeline_artifact_dir,DATA_INGESTION_ARTIFACT_DIR_KEY,self.time_stamp)
            raw_dir=os.path.join(artifact_dir,data_ingestion_config_info[DATA_INGESTION_RAW_DATA_DIR_KEY])
            train_dir=os.path.join(artifact_dir,data_ingestion_config_info[DATA_INGESTION_INGESTED_DATA_DIR_KEY],data_ingestion_config_info[DATA_INGESTION_INGESTED_TRAIN_DIR_KEY])
            test_dir=os.path.join(artifact_dir,data_ingestion_config_info[DATA_INGESTION_INGESTED_DATA_DIR_KEY],data_ingestion_config_info[DATA_INGESTION_INGESTED_TEST_DIR_KEY])
            os.makedirs(raw_dir,exist_ok=True)
            os.makedirs(train_dir,exist_ok=True)
            os.makedirs(test_dir,exist_ok=True)
            data_ingestion_entity=Data_Ingestion_Entity(
                data_download_url=data_ingestion_config_info[DATA_INGESTION_DOWNLOAD_URL_KEY], 
                raw_data_dir=raw_dir,
                train_dir=train_dir, 
                test_dir=test_dir
            )
            logging.info(f"Data Ingestion Configuration:{data_ingestion_entity}")
            return data_ingestion_entity
        except Exception as e:
            raise ThyroidException(e,sys) from e

    def get_data_validation_config(self)->Data_Validation_Entity:
        try:
            pipeline_entity=self.get_training_pipeline_config()
            data_validation_config_info=self.config_info[DATA_VALIDATION_CONFIG_KEY]
            artifact_dir=os.path.join(pipeline_entity.training_pipeline_artifact_dir,DATA_VALIDATION_ARTIFACT_DIR_KEY,self.time_stamp)
            schema_file_path=os.path.join(ROOT_DIR,data_validation_config_info[DATA_VALIDATION_SCHEMA_DIR_KEY],data_validation_config_info[DATA_VALIDATION_SCHEMA_FILE_NAME_KEY])
            report_file_path=os.path.join(artifact_dir,data_validation_config_info[DATA_VALIDATION_REPORT_FILE_NAME_KEY])
            report_page_file_path=os.path.join(artifact_dir,data_validation_config_info[DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY])
            os.makedirs(os.path.dirname(schema_file_path),exist_ok=True)
            os.makedirs(os.path.dirname(report_file_path),exist_ok=True)
            os.makedirs(os.path.dirname(report_page_file_path),exist_ok=True)
            data_validation_entity=Data_Validation_Entity(
                schema_file_path=schema_file_path, 
                report_file_path=report_file_path, 
                report_page_file_path=report_page_file_path
            )
            logging.info(f"Data Validation Configuration:{data_validation_entity}")
            return data_validation_entity
        except Exception as e:
            raise ThyroidException(e,sys) from e

    def get_data_transformation_config(self)->Data_Transfomation_Entity:
        try:
            pipeline_entity=self.get_training_pipeline_config()
            data_transformation_config_info=self.config_info[DATA_TRANSFORMATION_CONFIG_KEY]
            artifact_dir=os.path.join(pipeline_entity.training_pipeline_artifact_dir,DATA_TRANSFORMATION_ARTIFACT_DIR_KEY,self.time_stamp)
            transformed_train_dir=os.path.join(artifact_dir,data_transformation_config_info[DATA_TRANSFORMATION_TRANSFORMED_DIR_KEY],data_transformation_config_info[DATA_TRANSFORMATION_TRANSFORMED_TRAIN_DIR_KEY])
            transformed_test_dir=os.path.join(artifact_dir,data_transformation_config_info[DATA_TRANSFORMATION_TRANSFORMED_DIR_KEY],data_transformation_config_info[DATA_TRANSFORMATION_TRANSFORMED_TEST_DIR_KEY])
            preprocessed_object_file_path=os.path.join(artifact_dir,data_transformation_config_info[DATA_TRANSFORMATION_PREPROCESSING_DIR_KEY],data_transformation_config_info[DATA_TRANSFORMATION_PREPROCESSED_OBJECT_FILE_NAME_KEY])
            os.makedirs(os.path.dirname(preprocessed_object_file_path),exist_ok=True)
            os.makedirs(transformed_train_dir,exist_ok=True)
            os.makedirs(transformed_test_dir,exist_ok=True)
            data_transformation_entity=Data_Transfomation_Entity(
                transformed_train_dir=transformed_train_dir, 
                transformed_test_dir=transformed_test_dir, 
                preprocessed_object_file_path=preprocessed_object_file_path
            )
            logging.info(f"Data Transformation Configuration:{data_transformation_entity}")
            return data_transformation_entity
        except Exception as e:
            raise ThyroidException(e,sys) from e

    def get_model_trainer_config(self)->Model_Trainer_Entity:
        try:
            pipeline_entity=self.get_training_pipeline_config()
            model_trainer_config_info=self.config_info[MODEL_TRAINER_CONFIG_KEY]
            artifact_dir=os.path.join(pipeline_entity.training_pipeline_artifact_dir,MODEL_TRAINER_ARTIFACT_DIR_KEY,self.time_stamp)
            model_file_path=os.path.join(artifact_dir,model_trainer_config_info[MODEL_TRAINER_TRAINED_MODEL_DIR_KEY],model_trainer_config_info[MODEL_TRAINER_MODEL_FILE_NAME_KEY])
            model_config_file_path=os.path.join(ROOT_DIR,model_trainer_config_info[MODEL_TRAINER_MODEL_CONFIG_DIR_KEY],model_trainer_config_info[MODEL_TRAINER_MODEL_CONFIG_FILE_NAME_KEY])
            os.makedirs(os.path.dirname(model_file_path),exist_ok=True)
            os.makedirs(os.path.dirname(model_config_file_path),exist_ok=True)
            model_trainer_entity=Model_Trainer_Entity(
                model_config_file_path=model_config_file_path, 
                base_accuracy=model_trainer_config_info[MODEL_TRAINER_BASE_ACCURACY_KEY], 
                trained_model_file_path=model_file_path
            )
            logging.info(f"Model Trainer Configuration:{model_trainer_entity}")
            return model_trainer_entity
        except Exception as e:
            raise ThyroidException(e,sys) from e

    def get_model_evaluation_config(self)->Model_Evaluation_Entity:
        try:
            pipeline_entity=self.get_training_pipeline_config()
            model_evaluation_config_info=self.config_info[MODEL_EVALUATION_CONFIG_KEY]
            artifact_dir=os.path.join(pipeline_entity.training_pipeline_artifact_dir,MODEL_EVALUATION_ARTIFACT_DIR)
            model_evaluation_file_path=os.path.join(artifact_dir,model_evaluation_config_info[MODEL_EVALUATION_FILE_NAME_KEY])
            os.makedirs(os.path.dirname(model_evaluation_file_path),exist_ok=True)
            model_evaluation_entity=Model_Evaluation_Entity(
                model_evaluation_file_path=model_evaluation_file_path,
                time_stamp=self.time_stamp
            )
            logging.info(f"Model Evaluation Configuration:{model_evaluation_entity}")
            return model_evaluation_entity
        except Exception as e:
            raise ThyroidException(e,sys) from e

    def get_model_pusher_config(self)->Model_Pusher_Entity:
        try:
            time_stamp=self.time_stamp
            model_pusher_config=self.config_info[MODEL_PUSHER_CONFIG_KEY]
            export_dir_path=os.path.join(model_pusher_config[MODEL_PUSHER_EXPORT_DIR],time_stamp)
            os.makedirs(export_dir_path)
            model_pusher_entity=Model_Pusher_Entity(
                saved_model_path=export_dir_path
            )
            logging.info(f"Exported Model Configuration:{model_pusher_entity}")
            return model_pusher_entity
        except Exception as e:
            raise ThyroidException(e,sys) from e 

    def get_training_pipeline_config(self)->Training_Pipeline_Entity:
        try:
            training_pipeline_config_info=self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            artifact_dir=os.path.join(ROOT_DIR,training_pipeline_config_info[TRAINING_PIPELINE_NAME_KEY],training_pipeline_config_info[TRAINING_PIPELINE_ARTIFACT_DIR_KEY])
            os.makedirs(artifact_dir,exist_ok=True)
            training_pipeline_entity=Training_Pipeline_Entity(
                pipeline_name=training_pipeline_config_info[TRAINING_PIPELINE_NAME_KEY], 
                training_pipeline_artifact_dir=artifact_dir
            )
            logging.info(f"Training Pipeline Info:{training_pipeline_entity}")
            return training_pipeline_entity
        except Exception as e:
            raise ThyroidException(e,sys) from e                                   