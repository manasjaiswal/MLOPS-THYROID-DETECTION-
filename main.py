from Project.Config.configuration import Configuration
from Project.Helper_functions.helper import read_yaml_file,loading_object
import os
from Project.Entity.thyroidpredictor import ThyroidData
from Project.Pipeline.pipeline import Pipeline
from Project.Constants.constants import *
from flask import Flask,render_template,request,url_for

app=Flask(__name__)

@app.route('/',methods=["GET"])
def home():
    context={
                'INPUT_DATA':None,
                'RESULT':None
            }
    return render_template('home.html',context=context)

@app.route('/predict',methods=["GET","POST"])
def predict():
    try:
        if request.method=="POST":
            context={
                'INPUT_DATA':None,
                'RESULT':None
            }
            sex=str(request.form['sex'])
            On_thyroxine=str(request.form['On_thyroxine'])
            QThroxine=str(request.form['QThroxine'])
            medication=str(request.form['medication'])
            sick=str(request.form['sick'])
            pregnant=str(request.form['pregnant'])
            surgery=str(request.form['surgery'])
            I131_treatment=str(request.form['I131_treatment'])
            Qhypo=str(request.form['Qhypo'])
            Qhyper=str(request.form['Qhyper'])
            Lithium=str(request.form['Lithium'])
            Goitre=str(request.form['Goitre'])
            Tumor=str(request.form['Tumor'])
            Hypopitutary=str(request.form['Hypopitutary'])
            psch=str(request.form['psch'])
            TSH_BOOL=str(request.form['TSH_BOOL'])
            T3_BOOL=str(request.form['T3_BOOL'])
            TT4_BOOL=str(request.form['TT4_BOOL'])
            T4U_BOOL=str(request.form['T4U_BOOL'])
            FTI_BOOL=str(request.form['FTI_BOOL'])
            TBG_BOOL=str(request.form['TBG_BOOL'])
            source=str(request.form['source'])
            age=float(request.form['age'])
            TSH=float(request.form['TSH'])
            T3=float(request.form['T3'])
            TT4=float(request.form['TT4'])
            T4U=float(request.form['T4U'])
            FTI=float(request.form['FTI'])
            TBG=float(request.form['TBG'])

            thyroid_data=ThyroidData(
                sex=sex, 
                On_thyroxine=On_thyroxine, 
                QThroxine=QThroxine, 
                medication=medication, 
                sick=sick, 
                pregnant=pregnant, 
                surgery=surgery, 
                I131_treatment=I131_treatment, 
                Qhypo=Qhypo, 
                Qhyper=Qhyper, 
                Lithium=Lithium, 
                Goitre=Goitre, 
                Tumor=Tumor, 
                Hypopitutary=Hypopitutary, 
                psch=psch, 
                TSH_BOOL=TSH_BOOL, 
                T3_BOOL=T3_BOOL, 
                TT4_BOOL=TT4_BOOL, 
                T4U_BOOL=T4U_BOOL, 
                FTI_BOOL=FTI_BOOL, 
                TBG_BOOL=TBG_BOOL, 
                source=source, 
                age=age, 
                TSH=TSH, 
                T3=T3, 
                TT4=TT4, 
                T4U=T4U, 
                FTI=FTI, 
                TBG=TBG
            )
            data_dict=thyroid_data.get_thyroid_input_data_as_dict()
            dataframe=thyroid_data.get_thyroid_input_dataframe()
            co=Configuration(config_file_path=CONFIG_FILE_PATH)
            eval_file_path=co.get_model_evaluation_config().model_evaluation_file_path
            di=read_yaml_file(file_path=eval_file_path)
            model=loading_object(file_path=di[MODEL_PATH_KEY])
            result=model.predict(dataframe)[0]
            schema=read_yaml_file(file_path=SCHEMA_FILE_PATH)
            category_dict=schema[SCHEMA_TARGET_COLUMN_CATEGORIES_KEY]
            rev_category_dict={}
            for key,value in category_dict.items():
                rev_category_dict[value]=key
            result_text=rev_category_dict[result]
            context['INPUT_DATA']=data_dict
            context['RESULT']=result_text

            return render_template('home.html',context=context)
    except Exception as e:
        raise(e)

if __name__ == "__main__":
    app.run(debug=True)