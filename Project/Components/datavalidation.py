from Project.Exception.exception import ThyroidException
from Project.Logger.logging import logging
import os,sys
import pandas as pd
import numpy as np
from Project.Entity.configentity import Data_Validation_Entity
from Project.Entity.artifactentity import DataIngestionArtifact,DataValidationArtifact
from Project.Helper_functions.helper import read_yaml_file
from Project.Constants.constants import *
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab
import json
import re

class DataValidation:

    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,data_validation_config:Data_Validation_Entity)->None:
        try:
            logging.info(f"{':'*20}DATA VALIDATION LOG STARTED{':'*20}")
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
        except Exception as e:
            raise ThyroidException(e,sys) from e

    def file_existence(self)->bool:
        try:
            train_presence=False
            train_presence=False
            if os.path.exists(self.data_ingestion_artifact.train_file_path):
                logging.info(f"Train_file_exists")
                train_presence=True
            else:
                logging.info(f"No train file present")

            if os.path.exists(self.data_ingestion_artifact.test_file_path):
                logging.info("Test file exists")
                test_presence=True
            else:
                logging.info(f"No test file present")

            if test_presence==True and train_presence==True:
                return True

            else:
                return False

        except Exception as e:
            raise ThyroidException(e,sys) from e 

    def schema_validation(self)->bool:
        try:
            schema_validation=True
            #reading schema file
            schema_file_content=read_yaml_file(file_path=self.data_validation_config.schema_file_path)
            train_data=pd.read_csv(self.data_ingestion_artifact.train_file_path,index_col=[0])
            #test_data=pd.read_csv(self.data_ingestion_artifact.test_file_path)
            #Checking Validation for train data only because test is splitted from it
            train_columns=train_data.columns
            numerical_columns=[feature for feature in train_columns if train_data[feature].dtype!='object']
            categorical_columns=[feature for feature in train_columns if feature not in numerical_columns]
            categorical_columns.remove('class')
            for feature in numerical_columns:
                if feature in schema_file_content[SCHEMA_NUMERICAL_COLUMNS_KEY]:
                    pass
                else:
                    logging.info(f" Numerical Feature {feature} is not present in schema")
                    schema_validation=False

            for feature in categorical_columns:
                if feature in schema_file_content[SCHEMA_CATEGORICAL_COLUMNS_KEY]:
                    categories=schema_file_content[SCHEMA_CATEGORIES_KEY][feature]
                    for category in list(train_data[feature].dropna().unique()):
                        if category in categories:
                            pass
                        else:
                            logging.info(f"Categorical feature:{feature} has no category:{category}")
                            schema_validation=False
                else:
                    logging.info(f" Categorical Feature {feature} is not present in schema")
                    schema_validation=False
            
            return schema_validation
        except Exception as e:
            raise ThyroidException(e,sys) from e 

    def outliers_detection(self)->bool:
        try:
            outlier_detector=False
            train_data=pd.read_csv(self.data_ingestion_artifact.train_file_path,index_col=[0])
            #test_data=pd.read_csv(self.data_ingestion_artifact.test_file_path)
            numerical_columns=[feature for feature in train_data.columns if train_data[feature].dtype!='object']
            for feature in numerical_columns:
                d=0
                arr=np.percentile(train_data[feature],[25,50,75])
                lf=arr[0]-1.5*(arr[2]-arr[0])
                uf=arr[2]+1.5*(arr[2]-arr[0])
                for element in train_data[feature].dropna():
                    if lf<element<uf:
                        pass
                    else:
                        d=1
                if d==1:
                    logging.info(f"Outliers detected in feature:{feature}")
                    outlier_detector=True
            return outlier_detector
        except Exception as e:
            raise ThyroidException(e,sys) from e 

    def checking_nan_values(self)->bool:
        try:
            nan_values_existence=False
            train_data=pd.read_csv(self.data_ingestion_artifact.train_file_path,index_col=[0])
            for feature in train_data.columns:
                #We are checking array of na and non na which will be True and False when unique is applied 
                #if set contains False  then NAN values are present
                if  True in set(train_data[feature].isna().unique()):
                    logging.info(f"Nan values present in feature:{feature}")
                    nan_values_existence=True    
                else:
                    pass                    
            return nan_values_existence
        except Exception as e:
            raise ThyroidException(e,sys) from e 

    def get_and_save_data_drift_report(self)->dict:
        try:
            profile = Profile(sections=[DataDriftProfileSection()])

            train_df=pd.read_csv(self.data_ingestion_artifact.train_file_path,index_col=[0])
            test_df=pd.read_csv(self.data_ingestion_artifact.test_file_path,index_col=[0])

            train_df.drop(columns='TBG',inplace=True)
            test_df.drop(columns='TBG',inplace=True)
            profile.calculate(train_df,test_df)

            report = json.loads(profile.json())

            report_file_path = self.data_validation_config.report_file_path

            with open(report_file_path,"w") as report_file:
                json.dump(report, report_file, indent=6)
            return report
        except Exception as e:
            raise ThyroidException(e,sys) from e

    def checking_imbalancy_of_data(self)->float:
        try:
            train_df=pd.read_csv(self.data_ingestion_artifact.train_file_path,index_col=0)
            train_df[COLUMN_TARGET_COLUMN]=train_df[COLUMN_TARGET_COLUMN].apply(lambda x:re.sub(r"\.\W\d+","",x))
            d=train_df[COLUMN_TARGET_COLUMN].value_counts().to_dict()
            li=sorted(d.items(),key=lambda x:x[1],reverse=True)
            a=0
            for i in range(len(li)):
                a+=li[i][1]
            fraction=li[0][1]/a
            logging.info(f'Imbalancy of the dataset={100*fraction}')
            return 100*fraction
        except Exception as e:
            raise ThyroidException(e,sys) from e

    def save_data_drift_report_page(self):
        try:
            dashboard = Dashboard(tabs=[DataDriftTab()])
            train_df=pd.read_csv(self.data_ingestion_artifact.train_file_path,index_col=[0])
            test_df=pd.read_csv(self.data_ingestion_artifact.test_file_path,index_col=[0])

            train_df.drop(columns='TBG',inplace=True)
            test_df.drop(columns='TBG',inplace=True)
            dashboard.calculate(train_df,test_df)

            report_page_file_path = self.data_validation_config.report_page_file_path

            dashboard.save(report_page_file_path)
        except Exception as e:
            raise ThyroidException(e,sys) from e

    def data_drift_validation(self)->bool:
        try:
            is_data_drift_found=False
            data_drift_json=self.get_and_save_data_drift_report()
            self.save_data_drift_report_page()
            return is_data_drift_found
        except Exception as e:
            raise ThyroidException(e,sys) from e                                

    def initiate_data_validation(self)-> DataValidationArtifact:
        try:
            file_existence=self.file_existence()
            schema_validation=self.schema_validation()
            outlier_detection=self.outliers_detection()
            nan_detection=self.checking_nan_values()
            data_drift_existence=self.data_drift_validation()
            imbalancy=self.checking_imbalancy_of_data()

            data_validation_artifact=DataValidationArtifact(
                report_file_path=self.data_validation_config.report_file_path, 
                report_page_file_path=self.data_validation_config.report_page_file_path, 
                schema_file_path=self.data_validation_config.schema_file_path,
                data_drift=data_drift_existence, 
                file_existence=file_existence,
                outliers=outlier_detection, 
                nan_values=nan_detection, 
                schema_validation=schema_validation, 
                imbalancy_percent=imbalancy,
                is_validated=True
            )
            logging.info(f"Data Validation Artifact:{data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise ThyroidException(e,sys) from e

    def __del(self):        
        logging.info(f"{':'*20}DATA VALIDATION LOG ENDED{':'*20}")