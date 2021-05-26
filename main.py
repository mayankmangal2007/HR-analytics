
import uvicorn
from fastapi import FastAPI
from model import model_input
import pickle
import pandas as pd

app = FastAPI()
pickle_in = open("classifier.pkl","rb")
classifier=pickle.load(pickle_in)

@app.get('/')
def index():
    return{'message':'Welcome'}

@app.get('/Welcome')
def get_name(name: str):
    return{'Welcome {}'.format(name)}

@app.post('/predict')
def predict_promotion(data:model_input):
    data = data.dict()
    
    no_of_trainings=data['no_of_trainings']
    previous_year_rating=data['previous_year_rating']
    length_of_service=data['length_of_service']
    KPIs_met_80 = data['KPIs_met_80']
    awards_won=data['awards_won']
    avg_training_score=data['avg_training_score']
    
    department=data['department']
    education = data['education']
    gender = data['gender']
    region = data['region']
    recruitment_channel = data['recruitment_channel']
    age = data['age']
    
    department_cols = ['department_Analytics', 'department_Finance', 'department_HR', 'department_Legal', 'department_Operations', 'department_Procurement', 
                       'department_R&D', 'department_Sales & Marketing', 'department_Technology']
    
    education_cols = ["education_Bachelor's", 'education_Below Secondary', "education_Master's & above"]
    
    gender_cols = ['gender_f','gender_m']
    
    region_cols = ['region_region_1', 'region_region_10', 'region_region_11', 'region_region_12', 'region_region_13', 'region_region_14', 
                   'region_region_15', 'region_region_16', 'region_region_17', 'region_region_18', 'region_region_19', 'region_region_2', 
                   'region_region_20', 'region_region_21', 'region_region_22', 'region_region_23', 'region_region_24', 'region_region_25', 
                   'region_region_26', 'region_region_27', 'region_region_28', 'region_region_29', 'region_region_3', 'region_region_30', 
                   'region_region_31', 'region_region_32', 'region_region_33', 'region_region_34', 'region_region_4', 'region_region_5', 
                   'region_region_6', 'region_region_7', 'region_region_8', 'region_region_9']
    
    recruitment_cols = ['recruitment_channel_other', 'recruitment_channel_referred', 'recruitment_channel_sourcing']
    
    age_cols = ['age_20', 'age_30', 'age_40']
    
    def field_new(field, cols, col_prefix):
        my_dict = dict.fromkeys(cols,0)
        my_dict[col_prefix+'_'+str(field)]=1
        return(my_dict)
    
    dept_columns = field_new(department, department_cols, 'department')
    education_columns = field_new(education, education_cols, 'education')
    gender_columns = field_new(gender, gender_cols, 'gender')
    region_columns = field_new(region, region_cols, 'region')
    recruitment_columns = field_new(recruitment_channel, recruitment_cols, 'recruitment_channel')
    age_columns = field_new(age, age_cols, 'age')
    
    all_cols = ['no_of_trainings', 'previous_year_rating', 'length_of_service', 'KPIs_met_80', 'awards_won', 'avg_training_score']
    
    test = pd.DataFrame(columns=all_cols)
    test.loc[0,'no_of_trainings'] = no_of_trainings
    test.loc[0,'previous_year_rating'] = previous_year_rating
    test.loc[0,'length_of_service'] = length_of_service
    test.loc[0,'KPIs_met_80'] = KPIs_met_80
    test.loc[0,'awards_won'] = awards_won
    test.loc[0,'avg_training_score'] = avg_training_score
    
    extra_cols = pd.concat([pd.DataFrame(dept_columns, index=[0]), 
               pd.DataFrame(education_columns, index=[0]),
               pd.DataFrame(gender_columns, index=[0]),
               pd.DataFrame(region_columns, index=[0]),
               pd.DataFrame(recruitment_columns, index=[0]),
               pd.DataFrame(age_columns, index=[0])],axis=1)
    
    test_final = pd.concat([test, extra_cols],axis=1)
    test_final = test_final.astype('float')
    
    prediction = classifier.predict(test_final)
    
    if(prediction[0]==0):
        prediction="Will not be promoted! Sorry!"
    else:
        prediction="Congratulation! You will be promoted."
    
    return {'prediction': prediction}


if __name__== '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)