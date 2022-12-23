#Pipeline related input entities
from collections import namedtuple

Data_Ingestion_Entity=namedtuple('DataIngestion',["data_download_url","raw_data_dir","train_dir","test_dir"])

Data_Validation_Entity=namedtuple('DataValidation',["schema_file_path","report_file_path","report_page_file_path"])

Data_Transfomation_Entity=namedtuple('DataTransformation',["transformed_train_dir","transformed_test_dir","preprocessed_object_file_path"])

Model_Trainer_Entity=namedtuple('ModelTrainer',["model_config_file_path","base_accuracy","trained_model_file_path"])

Model_Evaluation_Entity=namedtuple('ModelEvaluation',["model_evaluation_file_path","time_stamp"])

Model_Pusher_Entity=namedtuple('ModelPusher',['saved_model_path'])

Training_Pipeline_Entity=namedtuple('TrainingPipeline',["pipeline_name","training_pipeline_artifact_dir"])