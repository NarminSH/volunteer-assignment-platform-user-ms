from operator import or_
from sqlalchemy import inspect, or_
import pandas as pd
import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from users import models
from users.database import engine, SessionLocal
from users.crud import get_user, filter_users, get_users
from users import schemas

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)
 


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get('/volunteers')
def read_volunteers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@app.get('/volunteers/{user_id}')
def read_volunteer(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db=db, user_id=user_id)
    return user    



@app.post('/filter-volunteers')
def filter_volunteers(data: schemas.FilterList, db: Session = Depends(get_db)):
    matched_users = []
    print(data.users, 'query over here..........')
    for i in data.users: 
        field = i.field
        operator = i.operator
        value = i.value
        user = filter_users(db, field=field, operator=operator, value=value)
        if user != [] and user is not None:
            if user not in matched_users:
                matched_users.append(user)
                print(matched_users, "...all matching users")
    return matched_users


@app.get('/volunteer-fields')
def read_fields():
    columns = [column.name for column in inspect(models.Volunteers).c]
    return columns


@app.get('/free-volunteers')
def filter_free_users(db: Session = Depends(get_db)):
    users = db.query(models.Volunteers).filter(models.Volunteers.status == "Free").all()
    return users
    


@app.get('/occupied-volunteers')
def filter_occupied_users(db: Session = Depends(get_db)):
    users = db.query(models.Volunteers).filter(or_(models.Volunteers.status == "Assign", models.Volunteers.status == "Waitlist")).all()
    return users



@app.get('/import-users-data')
def import_data(db: Session = Depends(get_db)):
    all_users_in_db = []
    all_users_in_excel = []
    users = get_users(db, skip=0, limit=100)
    # result_dict = [u.__dict__ for u in users]
    # print(result_dict)
    # for user in users:
    #     print(user._asdict())
        # print(all_users_in_db)
    # all_users_in_db.append(users)
    # data = pd.read_excel('assignment-data.xlsx', index_col=None)
    # for name in data.iterrows():  
    #     new_user_from_excel = name[1].to_dict()
    #     all_users_in_excel.append(new_user_from_excel)
    #     excel_dob = new_user_from_excel['Candidate - Date of Birth']
        # print(excel_dob)
        # for key, value in new_user_from_excel.items():
        #     if key == 'Candidate - ID':
        #         user = get_user(db=db, user_id=value)
        #         if user and user not in all_users_in_db:
        #             if user.dob == excel_dob:
        #                 # print('they are equal')
        #                 all_users_in_db.append(user)
        #             else:
        #                 # print('not equal')
        #                 return "dobs aren't matching"
        #         else:
        #             pass
                    # created_user = models.Volunteers(key=key)
                    # db.add(created_user)
                    # db.commit()
                    # db.refresh(created_user)
                    # return created_user
        # print(all_users_in_excel)      
    # print(all_users_in_db)         
    print("................................")
    print("................................")        
    # volunteers_df = pd.DataFrame(data)
    # volunteers_df["Candidate - ID"]=volunteers_df["Candidate - ID"].astype(str)
    # for d in range(len(data)):
    #     user_id = volunteers_df['Candidate - ID'].values[d]
    #     user = get_user(db=db, user_id=user_id)
    #     dob = pd.DataFrame(data, columns= ['Candidate - Date of Birth']).values[d]
    #     dobby = pd.DataFrame(data, columns= ['Candidate - Date of Birth'])
    #     print(dob, 'numpy', type(dob))
    #     print(dobby, 'string', type(dobby))
    #     if not user:
    #         created_user = models.Volunteers(id=user_id, gender_for_accreditation = pd.DataFrame(data, columns= ['Candidate - Gender Qatar']).values[d],
    #     dob = pd.DataFrame(data, columns= ['Candidate - Date of Birth']).values[d],
    #     current_occupation = pd.DataFrame(data, columns= ['Candidate - Current occupation']).values[d],
    #     id_document_country_of_issue = pd.DataFrame(data, columns= ['Candidate - ID']).values[d],
    #     driving_license_type = pd.DataFrame(data, columns= ["Candidate - Driver's Licence"]).values[d],
    #     country = pd.DataFrame(data, columns= ['Candidate - Country of Residence']).values[d],
    #     international_accommodation_preference = pd.DataFrame(data, columns= ['Candidate - FWC F&F Accommodation in Qatar']).values[d],
    #     disability_yes_no = pd.DataFrame(data, columns= ['Candidate - Disability']).values[d],
    #     disability_type = pd.DataFrame(data, columns= ['Candidate - Disability type']).values[d],
    #     covid_19_vaccinated = pd.DataFrame(data, columns= ['Candidate - COVID-19 Vaccinated?']).values[d],
    #     education_onechoice = pd.DataFrame(data, columns= ['Candidate - Education FWC']).values[d],
    #     area_of_study = pd.DataFrame(data, columns= ['Candidate - Education speciality']).values[d],
    #     english_fluency_level = pd.DataFrame(data, columns= ['Candidate - English Fluency Level']).values[d],
    #     arabic_fluency_level = pd.DataFrame(data, columns= ['Candidate - Arabic Fluency Level']).values[d])
    #         db.add(created_user)
    #         db.commit()
    #         db.refresh(created_user)
    #         print(created_user.id)
    #         print(created_user, '........')
    #         all_users_in_db.append(created_user)
    #         return all_users_in_db
    # volunteers_df["Candidate - Gender Qatar"] = volunteers_df["Candidate - Gender Qatar"].astype(str)
    # gender_for_accreditation = pd.DataFrame(data, columns= ['Candidate - Gender Qatar'])
    # dob = pd.DataFrame(data, columns= ['Candidate - Date of Birth'])
    # current_occupation = pd.DataFrame(data, columns= ['Candidate - Current occupation'])
    # id_document_country_of_issue = pd.DataFrame(data, columns= ['Candidate - ID'])
    # driving_license_type = pd.DataFrame(data, columns= ["Candidate - Driver's Licence"])
    # country = pd.DataFrame(data, columns= ['Candidate - Country of Residence'])
    # international_accommodation_preference = pd.DataFrame(data, columns= ['Candidate - FWC F&F Accommodation in Qatar'])
    # disability_yes_no = pd.DataFrame(data, columns= ['Candidate - Disability'])
    # disability_type = pd.DataFrame(data, columns= ['Candidate - Disability type'])
    # covid_19_vaccinated = pd.DataFrame(data, columns= ['Candidate - COVID-19 Vaccinated?'])
    # education_onechoice = pd.DataFrame(data, columns= ['Candidate - Education FWC'])
    # area_of_study = pd.DataFrame(data, columns= ['Candidate - Education speciality'])
    # english_fluency_level = pd.DataFrame(data, columns= ['Candidate - English Fluency Level'])
    # arabic_fluency_level = pd.DataFrame(data, columns= ['Candidate - Arabic Fluency Level'])
    # additional_language_1 = pd.DataFrame(data, columns= ['Candidate - Additional Language 1'])
    # additional_language_1_fluency_level = pd.DataFrame(data, columns= ['Candidate - Additional Language 1 Fluency Level'])
    # additional_language_2 = pd.DataFrame(data, columns= ['Candidate - Additional Language 2'])
    # additional_language_2_fluency_level = pd.DataFrame(data, columns= ['Candidate - Additional Language 2 Fluency Level'])
    # additional_language_3 = pd.DataFrame(data, columns= ['Candidate - Additional Language 3'])
    # additional_language_3_fluency_level = pd.DataFrame(data, columns= ['Candidate - Additional Language 3 Fluency Level'])
    # additional_language_4 = pd.DataFrame(data, columns= ['Candidate - Additional Language 4'])
    # additional_language_4_fluency_level = pd.DataFrame(data, columns= ['Candidate - Additional Language 4 Fluency Level'])
    # certified_translator_language = pd.DataFrame(data, columns= ['Candidate - Certified Translator Language'])
    # describe_your_it_skills = pd.DataFrame(data, columns= ['Candidate - Describe your IT skills'])
    # skill_1 = pd.DataFrame(data, columns= ['Candidate - Skill 1'])
    # skill_2 = pd.DataFrame(data, columns= ['Candidate - Skill 2'])
    # skill_3 = pd.DataFrame(data, columns= ['Candidate - Skill 3'])
    # skill_4 = pd.DataFrame(data, columns= ['Candidate - Skill 4'])
    # skill_5 = pd.DataFrame(data, columns= ['Candidate - Skill 5'])
    # skill_6 = pd.DataFrame(data, columns= ['Candidate - Skill 6'])
    # previous_volunteering_experience = pd.DataFrame(data, columns= ['Candidate - Which volunteer role(s) have you performed?'])
    # volunteer_experience = pd.DataFrame(data, columns= ['Candidate - Do you have volunteering experience?'])
    # fwc_are_you_interested_in_a_leadership_role = pd.DataFrame(data, columns= ['Candidate - FWC Are you interested in a leadership role? (The data you provide will be used as a reference; other roles may be assigned)'])
    # fwc_leadership_experience = pd.DataFrame(data, columns= ['Candidate - FWC Leadership Experience'])
    # ceremonies_yes_no = pd.DataFrame(data, columns= ['Candidate - Ceremonies yes no'])
    # cast_yes_no = pd.DataFrame(data, columns= ['Candidate - Cast yes no'])
    # cast_options = pd.DataFrame(data, columns= ['Candidate - Cast options'])
    # motivation_to_volunteer_at_fwc = pd.DataFrame(data, columns= ['Candidate - Motivation Score'])
    # availability_during_tournament = pd.DataFrame(data, columns= ['Candidate - Availability during tournament Alfa'])
    # daily_availability_shift_morning = pd.DataFrame(data, columns= ['Candidate - Daily availability shift morning Alfa'])
    # daily_availability_shift_afternoon = pd.DataFrame(data, columns= ['Candidate - Daily availability shift afternoon Alfa'])
    # daily_availability_shift_night = pd.DataFrame(data, columns= ['Candidate - Daily availability shift evening Alfa'])
    # daily_availability_shift_overnight = pd.DataFrame(data, columns= ['Candidate - Daily availability shift overnight Alfa'])
    # municipality_address = pd.DataFrame(data, columns= ['Candidate - Municipality (Address)']) 

    

    # if not user:
    #     created_user = create_user(db=db, user_id=user_id, gender_for_accreditation=pd.DataFrame(data, columns= ['Candidate - Gender Qatar']),
    #     dob=pd.DataFrame(data, columns= ['Candidate - Date of Birth']),
    #     current_occupation=pd.DataFrame(data, columns= ['Candidate - Current occupation']),
    #     id_document_country_of_issue=pd.DataFrame(data, columns= ['Candidate - ID']),
    #     driving_license_type=pd.DataFrame(data, columns= ["Candidate - Driver's Licence"]), country=country,international_accommodation_preference=international_accommodation_preference,
    #     disability_yes_no=disability_yes_no,disability_type=disability_type, covid_19_vaccinated=covid_19_vaccinated,
    #     education_onechoice=education_onechoice,area_of_study=area_of_study,
    #     english_fluency_level=english_fluency_level, arabic_fluency_level=arabic_fluency_level,
    #     additional_language_1=additional_language_1,additional_language_1_fluency_level=additional_language_1_fluency_level,
    #     additional_language_2= additional_language_2,additional_language_2_fluency_level=additional_language_2_fluency_level,
    #     additional_language_3=additional_language_3,additional_language_3_fluency_level=additional_language_3_fluency_level,
    #     additional_language_4=additional_language_4,additional_language_4_fluency_level=additional_language_4_fluency_level,
    #     certified_translator_language=certified_translator_language, describe_your_it_skills=describe_your_it_skills,
    #     skill_1=skill_1,skill_2=skill_2,skill_3=skill_3,skill_4=skill_4,skill_5=skill_5,skill_6=skill_6,
    #     previous_volunteering_experience=previous_volunteering_experience,volunteer_experience=volunteer_experience,
    #     fwc_are_you_interested_in_a_leadership_role=fwc_are_you_interested_in_a_leadership_role,
    #     fwc_leadership_experience=fwc_leadership_experience,
    #     ceremonies_yes_no=ceremonies_yes_no,cast_yes_no=cast_yes_no,cast_options=cast_options,
    #     motivation_to_volunteer_at_fwc=motivation_to_volunteer_at_fwc,availability_during_tournament=availability_during_tournament,
    #     daily_availability_shift_morning=daily_availability_shift_morning, 
    #     daily_availability_shift_afternoon=daily_availability_shift_afternoon,
    #     daily_availability_shift_night=daily_availability_shift_night, municipality_address=municipality_address,
    #     daily_availability_shift_overnight=daily_availability_shift_overnight)
    #     return created_user
    # else:
    #     raise HTTPException(status_code=400, detail="User already exists")
    
    #     candidate_id = pd.DataFrame(data, columns= ['Candidate - ID'], index=[d]).values[0]
    #     print(type(candidate_id), 'candidate id')
    #     stringifi = candidate_id.tostring()
        # print(stringifi)
        # user_id = int(stringifi)
        # print(type(user_id), 'user id type')
        

    # user = get_user(db=db, user_id=user_id )
    



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)