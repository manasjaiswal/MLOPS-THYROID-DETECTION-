from Project.Exception.exception import ThyroidException
from Project.Logger.logging import logging
import os,sys
from Project.Entity.configentity import Data_Ingestion_Entity
from Project.Entity.artifactentity import DataIngestionArtifact
from six.moves import urllib
from Project.Helper_functions.helper import reading_csv_file
from sklearn.model_selection import StratifiedShuffleSplit
import pandas as pd
import numpy as np

class DataIngestion:

    def __init__(self,data_ingestion_config:Data_Ingestion_Entity):
        try:
            logging.info(f"{':'*20}DATA INGESTION LOG STARTED{':'*20}")
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise ThyroidException(e,sys) from e

    def downloading_data_file(self)->str:
        """
        This function downloads the data from url 
        and copies in the raw data folder
        """
        try:
            raw_data_dir=self.data_ingestion_config.raw_data_dir
            download_url=self.data_ingestion_config.data_download_url
            download_path=os.path.join(raw_data_dir,os.path.basename(download_url))
            logging.info(f"Downloading data from {download_url} to file_path {download_path}")
            urllib.request.urlretrieve(url=download_url,filename=download_path)
            logging.info(f"Downloaded Successfully")
            return download_path
        except Exception as e:
            raise ThyroidException(e,sys) from e        

    def splitting_train_and_test(self):
        """
        This function splits the data from the 
        raw data folder into train and test datsets and stores it in
        the respective folders
        """
        try:
            download_path=self.downloading_data_file()
            data=reading_csv_file(file_path=download_path)
            #renaming columns 
            data.rename(columns={0:'age',1:'sex',2:'On_thyroxine',3:'QThroxine',4:'medication',5:'sick',6:'pregnant',7:'surgery',8:'I131_treatment',9:'Qhypo',10:'Qhyper',11:'Lithium',12:'Goitre',13:'Tumor',14:'Hypopitutary',15:'psch',16:'TSH_BOOL',17:'TSH',18:'T3_BOOL',19:'T3',20:'TT4_BOOL',21:'TT4',22:'T4U_BOOL',23:'T4U',24:'FTI_BOOL',25:'FTI',26:'TBG_BOOL',27:'TBG',28:'source',29:'class'},inplace=True)                     
            #split
            data['age_groups']=pd.cut(
                data["age"].fillna(np.mean(data['age'])),
                bins=[0,20,40,60,80,np.inf],
                labels=[1,2,3,4,5]
            )
            logging.info("Splitting data into train and test")
            split=StratifiedShuffleSplit(n_splits=1,test_size=0.2,random_state=42) 
            
            for train_idx,test_idx in split.split(data,data['age_groups']):
                strat_train_set=data.loc[train_idx].drop(columns='age_groups')
                strat_test_set=data.loc[test_idx].drop(columns='age_groups')

            logging.info(f"Splitting completed train has {len(strat_train_set)} records and test has {len(strat_test_set)} records")
            logging.info("Copying data from splits into train and test file paths ")

            train_file_path=os.path.join(self.data_ingestion_config.train_dir,os.path.basename(download_path))
            test_file_path=os.path.join(self.data_ingestion_config.test_dir,os.path.basename(download_path))
            
            strat_train_set.to_csv(train_file_path)
            strat_test_set.to_csv(test_file_path)
            
            data_ingestion_artifact=DataIngestionArtifact(
               train_file_path=train_file_path, 
               test_file_path=test_file_path, 
               is_ingested=True, 
               message="data-ingestion-done" 
            )
            logging.info(f"Data Ingestion Artifact:{data_ingestion_artifact}")
            return data_ingestion_artifact

        except Exception as e:
            raise ThyroidException(e,sys) from e

    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            return self.splitting_train_and_test()
        except Exception as e:
            raise ThyroidException(e,sys) from e  

    def __del__(self):
        logging.info(f"{':'*20}DATA INGESTION LOG COMPLETED{':'*20}")          
