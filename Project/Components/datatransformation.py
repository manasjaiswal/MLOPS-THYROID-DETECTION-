from Project.Entity.configentity import Data_Transfomation_Entity
from Project.Entity.artifactentity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact
from Project.Exception.exception import ThyroidException
from Project.Logger.logging import logging
import os,sys
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator,TransformerMixin
from sklearn.preprocessing import StandardScaler
from Project.Constants.constants import *
from Project.Helper_functions.helper import read_yaml_file,saving_numpy_array_data,saving_object
import re
from imblearn.over_sampling import RandomOverSampler

class NumTransformer(BaseEstimator,TransformerMixin):
    def __init__(self,columns,numerical_columns=None):
        self.columns=columns
        self.numerical_columns=numerical_columns

    def fit(self,X,y=None):
        return self

    def transform(self,X,y=None):
        try:
            dataset=pd.DataFrame(X,columns=self.columns)
            for feature in self.numerical_columns:
                dataset[feature]=dataset[feature].astype('float')
                dataset[feature]=dataset[feature].fillna(np.mean(dataset[feature]))
            #dataset.dropna(thresh=round(len(dataset)*0.9),inplace=True,axis=1)
            dataset.drop(columns=COLUMN_NUM_TBG,inplace=True)    
            return dataset
        except Exception as e:
            raise ThyroidException(e,sys) from e            

class CatTransformer(BaseEstimator,TransformerMixin):
    
    def __init__(self,columns=None,cat_columns=None):
        self.columns=columns
        self.cat_columns=cat_columns
    def fit(self,X,y=None):
        return self 

    def transform(self,X,y=None):
        try:       
            dataset=pd.DataFrame(X,columns=self.columns)
            dataset[COLUMN_TARGET_COLUMN]=y
            #dataset[COLUMN_TARGET_COLUMN]=data[COLUMN_TARGET_COLUMN].apply(lambda x:re.sub(r"\.\W\d+","",x))
            categorical_columns=self.cat_columns
          # numerical_columns=[feature for feature in self.columns if feature not in categorical_columns]
            d={}
            for feature in categorical_columns:
                e={}
                i=dataset.groupby(feature).groups
                for j in i.keys():
                    e[j]=len(i[j]) 
                e ={key: val for key, val in sorted(e.items(), key = lambda ele: ele[1],reverse=True)}      
                d[feature]=list(e.keys())[0]
            for feature in categorical_columns:
                dataset[feature]=dataset[feature].fillna(d[feature])
            for feature in categorical_columns:
                a=list(dataset.groupby(feature).groups.keys())
                c={}
                j=0
                for i in a:
                    c[i]=j
                    j+=1
                dataset[feature]=dataset[feature].map(c)                        
            return dataset.drop(columns=COLUMN_TARGET_COLUMN)
        except Exception as e:
            raise ThyroidException(e,sys) from e   


class DataTransformation:

    def __init__(self,data_validation_artifact:DataValidationArtifact,data_ingestion_artifact:DataIngestionArtifact,data_transformation_config:Data_Transfomation_Entity):
        try:
            logging.info(f"{':'*20}DATA TRANSFORMATION LOG STARTED{':'*20}")            
            self.data_validation_artifact=data_validation_artifact
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_transformation_config=data_transformation_config
        except Exception as e:
            raise ThyroidException(e,sys) from e

    def configuration_for_transformers(self)->Pipeline:
        try:
            schema_info=read_yaml_file(file_path=self.data_validation_artifact.schema_file_path)
            train_data=pd.read_csv(self.data_ingestion_artifact.train_file_path,index_col=0)
            categorical_columns=schema_info[SCHEMA_CATEGORICAL_COLUMNS_KEY]
            numerical_columns=schema_info[SCHEMA_NUMERICAL_COLUMNS_KEY]
            columns=train_data.columns[:-1]

            tr1=ColumnTransformer([('categorical_column_transformer',CatTransformer(columns=columns,cat_columns=categorical_columns),list(range(len(columns))))])
            tr2=ColumnTransformer([('numerical_column_transformer',NumTransformer(columns=columns,numerical_columns=numerical_columns),list(range(len(columns))))])
            tr3=ColumnTransformer([('standardscaler',StandardScaler(),list(range(28)))])
        
            pipeline=Pipeline([('tr1',tr1),('tr2',tr2),('tr3',tr3)])
            return pipeline
        except Exception as e:
            raise ThyroidException(e,sys) from e       

    def data_transformation_steps(self)->DataTransformationArtifact:
        try:
            preprocessing=self.configuration_for_transformers()
            schema_info=read_yaml_file(self.data_validation_artifact.schema_file_path)
            logging.info("Reading training and testing files for data transformation")
            train_data=pd.read_csv(self.data_ingestion_artifact.train_file_path,index_col=0)
            test_data=pd.read_csv(self.data_ingestion_artifact.test_file_path,index_col=0)
            train_data[COLUMN_TARGET_COLUMN]=train_data[COLUMN_TARGET_COLUMN].apply(lambda x:re.sub(r"\.\W\d+","",x))
            test_data[COLUMN_TARGET_COLUMN]=test_data[COLUMN_TARGET_COLUMN].apply(lambda x:re.sub(r"\.\W\d+","",x))
            train_data[COLUMN_TARGET_COLUMN]=train_data[COLUMN_TARGET_COLUMN].map(schema_info[SCHEMA_TARGET_COLUMN_CATEGORIES_KEY])
            test_data[COLUMN_TARGET_COLUMN]=test_data[COLUMN_TARGET_COLUMN].map(schema_info[SCHEMA_TARGET_COLUMN_CATEGORIES_KEY])
            logging.info('Taking care of imbalancy of the if it exists')
            if self.data_validation_artifact.imbalancy_percent>IMBALANCY_TOLERANCE_LIMIT:
                ro=RandomOverSampler()
                X,y=ro.fit_resample(X=train_data.drop(columns=COLUMN_TARGET_COLUMN),y=train_data[COLUMN_TARGET_COLUMN])
                train_data=pd.concat([X,y],axis=1)
                logging.info(f"\nTarget Classes balanced as following:{y.value_counts()}")
            else:
                logging.info('No imbalancy exists')
            logging.info('Applying pipeline preprocessing steps on training data')
            train_input_array=preprocessing.fit_transform(X=train_data.drop(columns=COLUMN_TARGET_COLUMN),y=train_data[COLUMN_TARGET_COLUMN])
            logging.info('Applying pipeline preprocessing steps on testing data')
            test_input_array=preprocessing.transform(X=test_data.drop(columns=COLUMN_TARGET_COLUMN))
            logging.info('Preprocessing done succesfully')
            logging.info('Saving preprocessing object in preprocessing object file path')
            saving_object(file_path=self.data_transformation_config.preprocessed_object_file_path,ser_obj=preprocessing)
            logging.info('Preprocessing object saved succesfully')
            train_array=np.c_[train_input_array,train_data[COLUMN_TARGET_COLUMN]]
            test_array=np.c_[test_input_array,test_data[COLUMN_TARGET_COLUMN]]
            logging.info("Saving train and test transformed arrays into the transfromed test and train directories")
            transformed_train_file_path=os.path.join(self.data_transformation_config.transformed_train_dir,'train.npz')
            transformed_test_file_path=os.path.join(self.data_transformation_config.transformed_test_dir,'test.npz')
            saving_numpy_array_data(file_path=transformed_train_file_path,array=train_array)
            saving_numpy_array_data(file_path=transformed_test_file_path,array=test_array)
            logging.info('Transformed Training and Testing arrays saved succesfully')
            
            data_transformation_artifact=DataTransformationArtifact(
                transformed_train_path=transformed_train_file_path, 
                transformed_test_path=transformed_test_file_path, 
                transformed_object_file_path=self.data_transformation_config.preprocessed_object_file_path, 
                is_transformed=True
            )
            logging.info(f"Data Transformation Artifact:{data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise ThyroidException(e,sys) from e       
  
    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            return self.data_transformation_steps()
        except Exception as e:
            raise ThyroidException(e,sys) from e       

    def __del__(self):
        logging.info(f"{':'*20}DATA TRANSFORMATION LOG COMPLETED{':'*20}")