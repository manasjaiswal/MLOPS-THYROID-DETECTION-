import pandas as pd
from Project.Constants.constants import *

class ThyroidData:

    def __init__(self,
                sex,
                On_thyroxine,
                QThroxine,
                medication,
                sick,
                pregnant,
                surgery,
                I131_treatment,
                Qhypo,
                Qhyper,
                Lithium,
                Goitre,
                Tumor,
                Hypopitutary,
                psch,
                TSH_BOOL,
                T3_BOOL,
                TT4_BOOL,
                T4U_BOOL,
                FTI_BOOL,
                TBG_BOOL,
                source,
                age,
                TSH,
                T3,
                TT4,
                T4U,
                FTI,
                TBG
                ):
        self.sex=sex
        self.On_thyroxine=On_thyroxine
        self.QThroxine=QThroxine
        self.medication=medication
        self.sick=sick
        self.pregnant=pregnant
        self.surgery=surgery
        self.I131_treatment=I131_treatment
        self.Qhypo=Qhypo
        self.Qhyper=Qhyper
        self.Lithium=Lithium
        self.Goitre=Goitre
        self.Tumor=Tumor
        self.Hypopitutary=Hypopitutary
        self.psch=psch
        self.TSH_BOOL=TSH_BOOL
        self.T3_BOOL=T3_BOOL
        self.TT4_BOOL=TT4_BOOL
        self.T4U_BOOL=T4U_BOOL
        self.FTI_BOOL=FTI_BOOL
        self.TBG_BOOL=TBG_BOOL
        self.source=source
        self.age=age
        self.TSH=TSH
        self.T3=T3
        self.TT4=TT4
        self.T4U=T4U
        self.FTI=FTI
        self.TBG=TBG

    def get_thyroid_input_data_as_dict(self)->dict:
        d={
        COLUMN_NUM_AGE:[self.age],
        COLUMN_CAT_SEX:[self.sex],
        COLUMN_CAT_ON_THROXINE:[self.On_thyroxine],
        COLUMN_CAT_QUERRY_THYROXINE:[self.QThroxine],
        COLUMN_CAT_ON_MEDICATION:[self.medication],
        COLUMN_CAT_SICK:[self.sick],
        COLUMN_CAT_PREGNANT:[self.pregnant],
        COLUMN_CAT_SURGERY:[self.surgery],
        COLUMN_CAT_I131_TREATMENT:[self.I131_treatment],
        COLUMN_CAT_QUERRY_HYPO:[self.Qhypo],
        COLUMN_CAT_QUERRY_HYPER:[self.Qhyper],
        COLUMN_CAT_LITHIUM:[self.Lithium],
        COLUMN_CAT_GOITRE:[self.Goitre],
        COLUMN_CAT_TUMOR:[self.Tumor],
        COLUMN_CAT_HYPOPITUTARY:[self.Hypopitutary],
        COLUMN_CAT_PSCH:[self.psch],
        COLUMN_CAT_TSH:[self.TSH_BOOL],
        COLUMN_NUM_TSH:[self.TSH],
        COLUMN_CAT_T3:[self.T3_BOOL],
        COLUMN_NUM_T3:[self.T3],
        COLUMN_CAT_TT4:[self.TT4_BOOL],
        COLUMN_NUM_TT4:[self.TT4],
        COLUMN_CAT_T4U:[self.T4U_BOOL],
        COLUMN_NUM_T4U:[self.T4U],
        COLUMN_CAT_FTI:[self.FTI_BOOL],
        COLUMN_NUM_FTI:[self.FTI],
        COLUMN_CAT_TBG:[self.TBG_BOOL],
        COLUMN_NUM_TBG:[self.TBG],
        COLUMN_CAT_SOURCE:[self.source], 
        }
        return d

    def get_thyroid_input_dataframe(self)->pd.DataFrame:
        d=self.get_thyroid_input_data_as_dict()
        dataframe=pd.DataFrame(data=d)
        return dataframe

        