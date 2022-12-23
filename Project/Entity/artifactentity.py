#Pipeline related artifacts 
from collections import namedtuple

DataIngestionArtifact=namedtuple('DataIngestionArtifact',['train_file_path','test_file_path','is_ingested','message'])

DataValidationArtifact=namedtuple('DataValidationArtifact',['report_file_path','imbalancy_percent','schema_file_path','file_existence','report_page_file_path','data_drift','outliers','nan_values','schema_validation','is_validated'])

DataTransformationArtifact=namedtuple('DataTransformationArtifact',['transformed_train_path','transformed_test_path','transformed_object_file_path','is_transformed'])

ModelTrainerArtifact=namedtuple('ModelTrainerArtifact',['best_model_name','model_object','trained_model_file_path','model_accuracy','model_fbeta_score','train_acc','test_acc','is_trained'])

ModelEvaluationArtifact=namedtuple('ModelEvaluationArtifact',['model_evaluation_file_path','is_evaluated','model_in_production','trained_model','trained_model_file_path'])

ModelPusherArtifact=namedtuple('ModelPusherArtifact',['saved_model_file_path'])