
from datetime import datetime
import shutil
import numpy as np
from sqlalchemy import inspect, or_
import pandas as pd
import uvicorn
from fastapi import FastAPI, Depends, File, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from users import models
from users.database import engine, SessionLocal
from users.crud import get_user, filter_users, get_users
from users import schemas
from users import models

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
        requirement = i.requirement
        operator = i.operator
        value = i.value
        user = filter_users(db, requirement=requirement, operator=operator, value=value)
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




@app.post('/import-users-data')
def import_data(file: UploadFile = File(...), db: Session = Depends(get_db)):
    all_users_in_excel = []
    with open(f'{file.filename}', "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    data = pd.read_excel("assignment-data.xlsx", index_col=None)
    volunteer_data = data.astype(object).replace(np.nan, None)

    for name in volunteer_data.iterrows():  
        new_user_from_excel = name[1].to_dict()
        all_users_in_excel.append(new_user_from_excel)
    
    all_ids_excel = []
    duplicate_ids_excel = []
    for i in all_users_in_excel:
        id_value = i["Candidate - ID"]
        if id_value not in all_ids_excel:
            all_ids_excel.append(id_value)
        else:
            if id_value not in duplicate_ids_excel:
                duplicate_ids_excel.append(id_value)
            

    if duplicate_ids_excel == []: 
        for key in all_users_in_excel:
            candidate_id = key["Candidate - ID"]
            user = db.query(models.Volunteers).filter(models.Volunteers.candidate_id == candidate_id).first()
            if not user:
                new_user = models.Volunteers(candidate_id=key["Candidate - ID"], full_name=key["Candidate - Full Name"], 
                checkpoint=key["Candidate - Checkpoint"], additional_language_1=key["Candidate - Additional Language 1"],
                additional_language_1_fluency_level=key["Candidate - Additional Language 2"], 
                additional_language_2=key["Candidate - Additional Language 2"],
                additional_language_2_fluency_level=key["Candidate - Additional Language 2 Fluency Level"], 
                additional_language_3=key["Candidate - Additional Language 3"],
                additional_language_3_fluency_level=key["Candidate - Additional Language 3 Fluency Level"],
                additional_language_4=key["Candidate - Additional Language 4"],
                additional_language_4_fluency_level=key["Candidate - Additional Language 4 Fluency Level"],
                gender_for_accreditation = key["Candidate - Gender Qatar"],
                dob = key["Candidate - Date of Birth"],
                delivery_score = key["Candidate - Delivering Amazing Score"],
                current_occupation = key["Candidate - Current occupation"],
                it_skills = key["Candidate - Describe your IT skills"],
                driving_license = key["Candidate - Driver's Licence"],
                residence_country = key["Candidate - Country of Residence"],
                accommodation_in_qatar = key["Candidate - FWC F&F Accommodation in Qatar"],
                disability_yes_no = key["Candidate - Disability"],
                disability_type = key["Candidate - Disability type"],
                covid_19_vaccinated = key["Candidate - COVID-19 Vaccinated?"],
                education_fwc = key["Candidate - Education FWC"],
                education_speciality = key["Candidate - Education speciality"],
                area_of_study = key["Candidate - Area of Study"],
                english_fluency_level = key["Candidate - English Fluency Level"],
                arabic_fluency_level = key["Candidate - Arabic Fluency Level"],
                describe_your_it_skills = key["Candidate - Describe your IT skills"],
                skill_1 = key["Candidate - Skill 1"],
                skill_2 = key["Candidate - skill 2"],
                skill_3 = key["Candidate - Skill 3"],
                skill_4 = key["Candidate - Skill 4"],
                skill_5 = key["Candidate - Skill 5"],
                skill_6 = key["Candidate - Skill 6"],
                volunteer_experience = key["Candidate - Do you have volunteering experience?"],
                preferred_volunteer_role = key["Candidate - Do you have a preferred volunteer role?"],
                have_wheelchair = key["Candidate - Do you use a wheelchair?"],
                fwc_are_you_interested_in_a_leadership_role = key["Candidate - FWC Are you interested in a leadership role? (The data you provide will be used as a reference; other roles may be assigned)"],
                fwc_leadership_experience = key["Candidate - FWC Leadership Experience"],
                ceremonies_yes_no = key["Candidate - Ceremonies yes no"],
                cast_yes_no = key["Candidate - Cast yes no"],
                certified_translator = key["Candidate - Certified translator"],
                certified_translator_language = key["Candidate - Certified Translator Language"],
                collaboration_score = key["Candidate - Collaboration Score"],
                cast_options = key["Candidate - Cast options"],
                motivation_score = key["Candidate - Motivation Score"],
                pioneer = key["Candidate - Pioneer"],
                international_volunteer = key["Candidate - International Volunteer Yes/No"],
                fwc_what_is_availability = key["Candidate - FWC What is your availability?"],
                availability_during_tournament = key["Candidate - Availability  during tournament Alfa"],
                daily_availability_shift_morning = key["Candidate - Daily availability shift morning Alfa"],
                daily_availability_shift_afternoon = key["Candidate - Daily availability shift afternoon Alfa"],
                daily_availability_shift_night = key["Candidate - Daily availability shift evening Alfa"],
                daily_availability_shift_overnight = key["Candidate - Daily availability shift overnight Alfa"],
                group_interview = key["Candidate - Group Interview Comment"],
                municipality_address = key["Candidate - Municipality (Address)"], created_at=datetime.now())
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
            else:
                user.full_name = key["Candidate - Full Name"]
                user.candidate_id = key["Candidate - ID"]
                user.checkpoint=key["Candidate - Checkpoint"]
                user.additional_language_1 = key["Candidate - Additional Language 1"]
                user.additional_language_1_fluency_level=key["Candidate - Additional Language 2"]
                user.additional_language_2=key["Candidate - Additional Language 2"]
                user.additional_language_2_fluency_level=key["Candidate - Additional Language 2 Fluency Level"]
                user.additional_language_3=key["Candidate - Additional Language 3"]
                user.additional_language_3_fluency_level=key["Candidate - Additional Language 3 Fluency Level"]
                user.additional_language_4=key["Candidate - Additional Language 4"]
                user.additional_language_4_fluency_level=key["Candidate - Additional Language 4 Fluency Level"]
                user.gender_for_accreditation = key["Candidate - Gender Qatar"]
                user.dob = key["Candidate - Date of Birth"]
                user.delivery_score = key["Candidate - Delivering Amazing Score"]
                user.current_occupation = key["Candidate - Current occupation"]
                user.it_skills = key["Candidate - Describe your IT skills"]
                user.driving_license = key["Candidate - Driver's Licence"]
                user.residence_country = key["Candidate - Country of Residence"]
                user.accommodation_in_qatar = key["Candidate - FWC F&F Accommodation in Qatar"]
                user.disability_yes_no = key["Candidate - Disability"]
                user.disability_type = key["Candidate - Disability type"]
                user.covid_19_vaccinated = key["Candidate - COVID-19 Vaccinated?"]
                user.education_fwc = key["Candidate - Education FWC"]
                user.education_speciality = key["Candidate - Education speciality"]
                user.area_of_study = key["Candidate - Area of Study"]
                user.english_fluency_level = key["Candidate - English Fluency Level"]
                user.arabic_fluency_level = key["Candidate - Arabic Fluency Level"]
                user.describe_your_it_skills = key["Candidate - Describe your IT skills"]
                user.skill_1 = key["Candidate - Skill 1"]
                user.skill_2 = key["Candidate - skill 2"]
                user.skill_3 = key["Candidate - Skill 3"]
                user.skill_4 = key["Candidate - Skill 4"]
                user.skill_5 = key["Candidate - Skill 5"]
                user.skill_6 = key["Candidate - Skill 6"]
                user.volunteer_experience = key["Candidate - Do you have volunteering experience?"]
                user.preferred_volunteer_role = key["Candidate - Do you have a preferred volunteer role?"]
                user.have_wheelchair = key["Candidate - Do you use a wheelchair?"]
                user.fwc_are_you_interested_in_a_leadership_role = key["Candidate - FWC Are you interested in a leadership role? (The data you provide will be used as a reference; other roles may be assigned)"]
                user.fwc_leadership_experience = key["Candidate - FWC Leadership Experience"]
                user.ceremonies_yes_no = key["Candidate - Ceremonies yes no"]
                user.cast_yes_no = key["Candidate - Cast yes no"]
                user.certified_translator = key["Candidate - Certified translator"]
                user.certified_translator_language = key["Candidate - Certified Translator Language"]
                user.collaboration_score = key["Candidate - Collaboration Score"]
                user.cast_options = key["Candidate - Cast options"]
                user.motivation_score = key["Candidate - Motivation Score"]
                user.pioneer = key["Candidate - Pioneer"]
                user.international_volunteer = key["Candidate - International Volunteer Yes/No"]
                user.fwc_what_is_availability = key["Candidate - FWC What is your availability?"]
                user.availability_during_tournament = key["Candidate - Availability  during tournament Alfa"]
                user.daily_availability_shift_morning = key["Candidate - Daily availability shift morning Alfa"]
                user.daily_availability_shift_afternoon = key["Candidate - Daily availability shift afternoon Alfa"]
                user.daily_availability_shift_night = key["Candidate - Daily availability shift evening Alfa"]
                user.daily_availability_shift_overnight = key["Candidate - Daily availability shift overnight Alfa"]
                user.group_interview = key["Candidate - Group Interview Comment"]
                user.municipality_address = key["Candidate - Municipality (Address)"]
                user.updated_at = datetime.now()
                db.commit()
    else:
        return { "status": status.HTTP_400_BAD_REQUEST, "result": "Duplicate ID", "message": duplicate_ids_excel}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)