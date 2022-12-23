from datetime import datetime
import os

def get_current_time_stamp():
    return f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"

LOG_DIR='thyroid_logs'

ROOT_DIR=os.getcwd()
#Pipeline related constants

TRAINING_PIPELINE_CONFIG_KEY="training_pipeline_config"
TRAINING_PIPELINE_ARTIFACT_DIR_KEY="artifact_dir"
TRAINING_PIPELINE_NAME_KEY="pipeline_name"


DATA_INGESTION_CONFIG_KEY="data_ingestion_config"
DATA_INGESTION_ARTIFACT_DIR_KEY="data_ingestion"
DATA_INGESTION_DOWNLOAD_URL_KEY="dataset_download_url"
DATA_INGESTION_RAW_DATA_DIR_KEY="raw_data_dir"
DATA_INGESTION_INGESTED_DATA_DIR_KEY="ingested_dir"
DATA_INGESTION_INGESTED_TRAIN_DIR_KEY="ingested_train_dir"
DATA_INGESTION_INGESTED_TEST_DIR_KEY="ingested_test_dir"

DATA_VALIDATION_CONFIG_KEY="data_validation_config"
DATA_VALIDATION_SCHEMA_DIR_KEY="schema_dir"
DATA_VALIDATION_SCHEMA_FILE_NAME_KEY="schema_file_name"
DATA_VALIDATION_REPORT_FILE_NAME_KEY="report_file_name"
DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY="report_page_file_name"
DATA_VALIDATION_ARTIFACT_DIR_KEY="data_validation"

DATA_TRANSFORMATION_CONFIG_KEY="data_transformation_config"
DATA_TRANSFORMATION_ARTIFACT_DIR_KEY="data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DIR_KEY="transformed_dir"
DATA_TRANSFORMATION_TRANSFORMED_TRAIN_DIR_KEY="transformed_train_dir"
DATA_TRANSFORMATION_TRANSFORMED_TEST_DIR_KEY="transformed_test_dir"
DATA_TRANSFORMATION_PREPROCESSING_DIR_KEY="preprocessing_dir"
DATA_TRANSFORMATION_PREPROCESSED_OBJECT_FILE_NAME_KEY="preprocessed_object_file_name"

MODEL_TRAINER_CONFIG_KEY="model_trainer_config"
MODEL_TRAINER_ARTIFACT_DIR_KEY="model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR_KEY="trained_model_dir"
MODEL_TRAINER_MODEL_FILE_NAME_KEY="model_file_name"
MODEL_TRAINER_BASE_ACCURACY_KEY="base_accuracy"
MODEL_TRAINER_MODEL_CONFIG_DIR_KEY="model_config_dir"
MODEL_TRAINER_MODEL_CONFIG_FILE_NAME_KEY="model_config_file_name"

MODEL_EVALUATION_CONFIG_KEY="model_evaluation_config"
MODEL_EVALUATION_FILE_NAME_KEY="model_evaluation_file_name"
MODEL_EVALUATION_ARTIFACT_DIR="model_evaluation"

MODEL_PUSHER_CONFIG_KEY="model_pusher_config"
MODEL_PUSHER_EXPORT_DIR="model_export_dir"

SCHEMA_CATEGORICAL_COLUMNS_KEY="categorical_columns"
SCHEMA_CATEGORIES_KEY="categories"
SCHEMA_NUMERICAL_COLUMNS_KEY="numerical_columns"
SCHEMA_TARGET_COLUMN_KEY="target_column"
SCHEMA_TARGET_COLUMN_CATEGORIES_KEY="class_categories"

#Feature related informations
COLUMN_CAT_SEX="sex"
COLUMN_CAT_QUERRY_THYROXINE="On_thyroxine"
COLUMN_CAT_ON_THROXINE="QThroxine"
COLUMN_CAT_ON_MEDICATION="medication"
COLUMN_CAT_SICK="sick"
COLUMN_CAT_PREGNANT="pregnant"
COLUMN_CAT_SURGERY="surgery"
COLUMN_CAT_I131_TREATMENT="I131_treatment"
COLUMN_CAT_QUERRY_HYPO="Qhypo"
COLUMN_CAT_QUERRY_HYPER="Qhyper"
COLUMN_CAT_LITHIUM="Lithium"
COLUMN_CAT_GOITRE="Goitre"
COLUMN_CAT_TUMOR="Tumor"
COLUMN_CAT_HYPOPITUTARY="Hypopitutary"
COLUMN_CAT_PSCH="psch"
COLUMN_CAT_TSH="TSH_BOOL"
COLUMN_CAT_T3="T3_BOOL"
COLUMN_CAT_TT4="TT4_BOOL"
COLUMN_CAT_T4U="T4U_BOOL"
COLUMN_CAT_FTI="FTI_BOOL"
COLUMN_CAT_TBG="TBG_BOOL"
COLUMN_CAT_SOURCE="source"
COLUMN_NUM_AGE="age"
COLUMN_NUM_TSH="TSH"
COLUMN_NUM_T3="T3"
COLUMN_NUM_TT4="TT4"
COLUMN_NUM_T4U="T4U"
COLUMN_NUM_FTI="FTI"
COLUMN_NUM_TBG="TBG"
COLUMN_TARGET_COLUMN="class"

IMBALANCY_TOLERANCE_LIMIT=70


#ModelTraining related constants
GRID_SEARCH_KEY="grid_search"
MODULE_KEY="module"
CLASS_KEY="class"
PARAM_KEY="params"
MODEL_SELECTION_KEY="model_selection"
SEARCH_PARA_GRID_KEY="search_param_grid"

TOLERANCE_LIMIT=0.08

#Model evaluation related constants
BEST_MODEL_KEY="best model"
HISTORY_KEY="history"
MODEL_PATH_KEY="model_path"

EXPERIMENT_DIR_NAME="experiment"
EXPERIMENT_FILE_NAME="experiment.csv"


#Classification if need arises, 1 is taken as default
F_BETA_VALUE=1


CONFIG_FILE_PATH=os.path.join(ROOT_DIR,"config/config.yaml")
SCHEMA_FILE_PATH=os.path.join(ROOT_DIR,"config/schema.yaml")