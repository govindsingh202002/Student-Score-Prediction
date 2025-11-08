from flask import Flask,request,render_template
from src.pipeline.prediction_pipeline import InputDataTransformation,PredictPipeline
import numpy as np
application=Flask(__name__)
app=application

@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='GET':
        return render_template('index.html',title='Home')
    else:
        data=InputDataTransformation(
        gender=str(request.form.get('gender')),
        race_ethnicity=str(request.form.get('race_ethnicity')),
        parental_level_of_education=request.form.get('parental_level_of_education'),
        lunch= str(request.form.get('lunch')),
        test_preparation_course= str(request.form.get('test_preparation_course')),
        reading_score= int(request.form.get('reading_score')),
        writing_score= int(request.form.get('writing_score'))
        )
        input_dataframe=data.get_input_data_as_dataframe()
        prediction_pipeline_obj=PredictPipeline()
        prediction=prediction_pipeline_obj.predict(input_dataframe)
        return render_template('index.html',results=np.round(prediction[0],2))

@app.route('/home')
def home():
    return render_template('index.html',title='Home')

@app.route('/about')
def about():
    return render_template('about.html',title="About")

if __name__=='__main__':
    app.run(debug=True)