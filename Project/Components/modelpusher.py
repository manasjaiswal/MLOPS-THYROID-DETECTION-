from Project.Exception.exception import ThyroidException
from Project.Logger.logging import logging
import os,sys
import shutil
from Project.Entity.artifactentity import ModelPusherArtifact,ModelEvaluationArtifact
from Project.Entity.configentity import Model_Pusher_Entity

class Model_Pusher:
    def __init__(self,model_pusher_config:Model_Pusher_Entity,model_evaluation_artifact:ModelEvaluationArtifact):
        try:
            logging.info(f"{':'*20}MODEL PUSHER LOG STARTED{':'*20}")
            self.model_pusher_config=model_pusher_config
            self.model_evaluation_artifact=model_evaluation_artifact
        except Exception as e:
            raise ThyroidException(e,sys) from e

    def initiate_model_pushing(self)->ModelPusherArtifact:
        try:
            trained_model_path=self.model_evaluation_artifact.trained_model_file_path
            export_dir=self.model_pusher_config.saved_model_path
            logging.info(f'Copying trained model from {trained_model_path} into the directory:{export_dir}')
            dst=shutil.copy(src=trained_model_path,dst=export_dir)
            logging.info(f'File successfully copied as : {dst}')
            model_pusher_artifact=ModelPusherArtifact(
                saved_model_file_path=dst
            )
            logging.info(f"Model Pusher Artifact:{model_pusher_artifact}")
            return model_pusher_artifact
        except Exception as e:
            raise ThyroidException(e,sys) from e 

    def __del__(self):
        logging.info(f"{':'*20}MODEL PUSHER LOG ENDED{':'*20}")               
        