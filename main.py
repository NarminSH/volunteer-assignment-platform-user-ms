
from datetime import datetime
from typing import List
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
from users import models
import math

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
def filter_volunteers(filter_list: List, page_number: int = 1, page_size:int = 10, db: Session = Depends(get_db)):
    matched_users = []
    filtered_users = []
    last_users = []
    print(filter_list)

    start = (page_number-1) * page_size
    end = start + page_size

    # for filter in fil
        # all_users = get_users(db=db)
        # print(len(all_users), "filter_list does not contain anything")
        # print(math.ceil(len(all_users) / page_size))
        # response = {
        #     "data": all_users[start:end],
        #     "total_pages": math.ceil(len(all_users) / page_size)
        # }
        # return response

    for filter in filter_list:
        requirement = filter["requirement_name"]
        operator = filter["operator"]


        if requirement == 'Requirement' and operator=='Operator': #if page just opened
            all_users = get_users(db=db)
            response = {
            "data": all_users[start:end],
            "total_pages": len(all_users)
            }
            return response
        
        if requirement=='language' and operator == '=':
            for value in filter["value"]:
                users = db.query(models.Volunteers).filter(or_(models.Volunteers.additional_language_1 == value, 
                models.Volunteers.additional_language_2 == value, models.Volunteers.additional_language_3 == value,
                models.Volunteers.additional_language_4 == value)).all()
                matched_users.append(users)

        if requirement=='language' and operator == 'contains':
            for value in filter["value"]:
                users = db.query(models.Volunteers).filter(or_(models.Volunteers.additional_language_1.contains(value), 
                models.Volunteers.additional_language_2.contains(value), models.Volunteers.additional_language_3.contains(value),
                models.Volunteers.additional_language_4.contains(value))).all()
                matched_users.append(users)
        
        if requirement=='language_fluency_level' and operator=='=':
            for value in filter["value"]:
                users = db.query(models.Volunteers).filter(or_(models.Volunteers.additional_language_1_fluency_level == value, 
                models.Volunteers.additional_language_2_fluency_level == value, models.Volunteers.additional_language_3_fluency_level == value,
                models.Volunteers.additional_language_4_fluency_level == value)).all()
                matched_users.append(users)

        if requirement=='language_fluency_level' and operator=='contains':
            for value in filter["value"]:
                users = db.query(models.Volunteers).filter(or_(models.Volunteers.additional_language_1_fluency_level.contains(value), 
                models.Volunteers.additional_language_2_fluency_level.contains(value), models.Volunteers.additional_language_3_fluency_level.contains(value),
                models.Volunteers.additional_language_4_fluency_level.contains(value))).all()
                matched_users.append(users)

        if requirement=='skill' and operator=='=':
            print('I am here skill = if')
            for value in filter["value"]:
                users = db.query(models.Volunteers).filter(or_(models.Volunteers.skill_1 == value, 
                models.Volunteers.skill_2 == value, models.Volunteers.skill_3 == value,
                models.Volunteers.skill_4 == value, models.Volunteers.skill_5 == value,
                models.Volunteers.skill_6 == value)).all()
                matched_users.append(users)
        

        if requirement=='skill' and operator=='contains':
            print('I am here skill contains if')
            for value in filter["value"]:
                users = db.query(models.Volunteers).filter(or_(models.Volunteers.skill_1.contains(value), 
                models.Volunteers.skill_2.contains(value), models.Volunteers.skill_3.contains(value),
                models.Volunteers.skill_4.contains(value), models.Volunteers.skill_5.contains(value),
                models.Volunteers.skill_6.contains(value))).all()
                matched_users.append(users)

        if matched_users != [] and requirement != "skill" and requirement != "language" and requirement != 'language_fluency_level' :
            print("first if")
            print(matched_users)
            for users in matched_users:
                if users != []:
                    for one_user in users: 
                        filtered_users.append(one_user)

            for value in filter["value"]: #second loop to get all values, otherwise will always get last value
                for user in filtered_users:
                        print("Value is", value, " inside for loop")
                        if operator == "=":
                            if (getattr(user, requirement) == value):
                                if user not in last_users:
                                    last_users.append(user)
                        elif operator == "contains":
                            print("elif operator contains second loop")
                            if value in (getattr(user, requirement)):
                                if user not in last_users:
                                    last_users.append(user)
                        elif operator == ">":
                            print('second loop operator >', (getattr(user, requirement)))
                            if (getattr(user, requirement)) > value:
                                if user not in last_users:
                                    last_users.append(user)
                                    print('appended')
                        elif operator == "<":
                            print('second loop operator <', (getattr(user, requirement)))
                            if (getattr(user, requirement)) < value:
                                if user not in last_users:
                                    last_users.append(user)
                                    print('appended')
                        elif operator == "<=":
                            if (getattr(user, requirement)) <= value:
                                if user not in last_users:
                                    last_users.append(user)
                        elif operator == ">=":
                            if (getattr(user, requirement)) >= value:
                                if user not in last_users:
                                    last_users.append(user)
                print(len(last_users), 'len last') 

        if requirement != "skill" and requirement != "language" and requirement != 'language_fluency_level':
            print("second if")
            if len(filter["value"]) > 1 and len(matched_users) == 0: #check len match users so it won't send request to db again if it is not empty
                for value in filter["value"]:
                    users = filter_users(db, requirement=requirement, operator=operator, value=value) 
                    print(len(users), 'last users when value length is more than one')
                    matched_users.append(users)   

        if requirement != "skill" and requirement != "language" and requirement != 'language_fluency_level' and len(filter["value"])==1 and len(matched_users) == 0:
            value = filter["value"][0]
            users = filter_users(db, requirement=requirement, operator=operator, value=value)
            matched_users.append(users)
            print(len(users), 'length of users when value length is 1')



    if filtered_users == [] and matched_users != []: #if filter is only language, skill or fluency_level
        for users in matched_users:
            for one_user in users: 
                filtered_users.append(one_user)
        response = {
            "data": filtered_users[start:end],
            "total_pages": len(filtered_users) 
        }
        return response
    else:
        print("returning last users list in else statement", len(last_users))
        response = {
            "data": last_users[start:end],
            "total_pages": len(last_users)
        }
        return response
    


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

    print("got1 here")
    print(datetime.now())
    data = pd.read_excel("assignment-data.xlsx", index_col=None)
    volunteer_data = data.astype(object).replace(np.nan, None)

    print("got2 here")
    for name in volunteer_data.iterrows():  
        new_user_from_excel = name[1].to_dict()
        all_users_in_excel.append(new_user_from_excel)
    
    print(datetime.now(), "for candidate ids")
    all_ids_excel = []
    duplicate_ids_excel = []
    for i in all_users_in_excel:
        id_value = i["Candidate - ID"]
        if id_value not in all_ids_excel:
            all_ids_excel.append(id_value)
        else:
            if id_value not in duplicate_ids_excel:
                duplicate_ids_excel.append(id_value)

    print(datetime.now(), 'before all')
    users = db.query(models.Volunteers).all()
    print(datetime.now(), 'after all')
    all_candidate_ids_in_db = []
    for user in users:
        all_candidate_ids_in_db.append(user.candidate_id)

    print(datetime.now())
    saved_users = []
    updated_users = []    
    if duplicate_ids_excel == []: 
        for key in all_users_in_excel:
            candidate_id = key["Candidate - ID"]
            if candidate_id not in all_candidate_ids_in_db:
                new_user = {
                "candidate_id": candidate_id,
                "full_name": key["Candidate - Full Name"],
                "checkpoint": key["Candidate - Checkpoint"],
                "additional_language_1": key["Candidate - Additional Language 1"],
                "additional_language_2": key["Candidate - Additional Language 2"],
                "additional_language_2_fluency_level": key["Candidate - Additional Language 2 Fluency Level"], 
                "additional_language_3": key["Candidate - Additional Language 3"],
                "additional_language_3_fluency_level": key["Candidate - Additional Language 3 Fluency Level"],
                "additional_language_4": key["Candidate - Additional Language 4"],
                "additional_language_4_fluency_level": key["Candidate - Additional Language 4 Fluency Level"],
                "gender_for_accreditation": key["Candidate - Gender Qatar"],
                "dob": key["Candidate - Date of Birth"],
                "delivery_score": key["Candidate - Delivering Amazing Score"],
                "current_occupation": key["Candidate - Current occupation"],
                "it_skills": key["Candidate - Describe your IT skills"],
                "driving_license": key["Candidate - Driver's Licence"],
                "residence_country": key["Candidate - Country of Residence"],
                "accommodation_in_qatar":  key["Candidate - FWC F&F Accommodation in Qatar"],
                "disability_yes_no": key["Candidate - Disability"],
                "disability_type": key["Candidate - Disability type"],
                "covid_19_vaccinated": key["Candidate - COVID-19 Vaccinated?"],
                "education_fwc": key["Candidate - Education FWC"],
                "education_speciality": key["Candidate - Education speciality"],
                "area_of_study": key["Candidate - Area of Study"],
                "english_fluency_level": key["Candidate - English Fluency Level"],
                "arabic_fluency_level": key["Candidate - Arabic Fluency Level"],
                "describe_your_it_skills": key["Candidate - Describe your IT skills"],
                "skill_1": key["Candidate - Skill 1"],
                "skill_2": key["Candidate - skill 2"],
                "skill_3": key["Candidate - Skill 3"],
                "skill_4": key["Candidate - Skill 4"],
                "skill_5" : key["Candidate - Skill 5"],
                "skill_6" : key["Candidate - Skill 6"],
                "volunteer_experience" :  key["Candidate - Do you have volunteering experience?"],
                "preferred_volunteer_role" : key["Candidate - Do you have a preferred volunteer role?"],
                "have_wheelchair" : key["Candidate - Do you use a wheelchair?"],
                "fwc_are_you_interested_in_a_leadership_role" : key["Candidate - FWC Are you interested in a leadership role? (The data you provide will be used as a reference; other roles may be assigned)"],
                "fwc_leadership_experience":  key["Candidate - FWC Leadership Experience"],
                "ceremonies_yes_no" : key["Candidate - Ceremonies yes no"],
                "cast_yes_no" : key["Candidate - Cast yes no"],
                "certified_translator" : key["Candidate - Certified translator"],
                "certified_translator_language" : key["Candidate - Certified Translator Language"],
                "collaboration_score" : key["Candidate - Collaboration Score"],
                "cast_options" : key["Candidate - Cast options"],
                "motivation_score" : key["Candidate - Motivation Score"],
                "pioneer" : key["Candidate - Pioneer"],
                "international_volunteer" : key["Candidate - International Volunteer Yes/No"],
                "fwc_what_is_availability" : key["Candidate - FWC What is your availability?"],
                "availability_during_tournament" : key["Candidate - Availability  during tournament Alfa"],
                "daily_availability_shift_morning" : key["Candidate - Daily availability shift morning Alfa"],
                "daily_availability_shift_afternoon" : key["Candidate - Daily availability shift afternoon Alfa"],
                "daily_availability_shift_night" : key["Candidate - Daily availability shift evening Alfa"],
                "daily_availability_shift_overnight" : key["Candidate - Daily availability shift overnight Alfa"],
                "group_interview" :  key["Candidate - Group Interview Comment"],
                "municipality_address" : key["Candidate - Municipality (Address)"], 
                "created_at": datetime.now()
                }
                saved_users.append(new_user)
            else:
                update_user = {
                "candidate_id": candidate_id,
                "full_name": key["Candidate - Full Name"],
                "checkpoint": key["Candidate - Checkpoint"],
                "additional_language_1": key["Candidate - Additional Language 1"],
                "additional_language_2": key["Candidate - Additional Language 2"],
                "additional_language_2_fluency_level": key["Candidate - Additional Language 2 Fluency Level"], 
                "additional_language_3": key["Candidate - Additional Language 3"],
                "additional_language_3_fluency_level": key["Candidate - Additional Language 3 Fluency Level"],
                "additional_language_4": key["Candidate - Additional Language 4"],
                "additional_language_4_fluency_level": key["Candidate - Additional Language 4 Fluency Level"],
                "gender_for_accreditation": key["Candidate - Gender Qatar"],
                "dob": key["Candidate - Date of Birth"],
                "delivery_score": key["Candidate - Delivering Amazing Score"],
                "current_occupation": key["Candidate - Current occupation"],
                "it_skills": key["Candidate - Describe your IT skills"],
                "driving_license": key["Candidate - Driver's Licence"],
                "residence_country": key["Candidate - Country of Residence"],
                "accommodation_in_qatar":  key["Candidate - FWC F&F Accommodation in Qatar"],
                "disability_yes_no": key["Candidate - Disability"],
                "disability_type": key["Candidate - Disability type"],
                "covid_19_vaccinated": key["Candidate - COVID-19 Vaccinated?"],
                "education_fwc": key["Candidate - Education FWC"],
                "education_speciality": key["Candidate - Education speciality"],
                "area_of_study": key["Candidate - Area of Study"],
                "english_fluency_level": key["Candidate - English Fluency Level"],
                "arabic_fluency_level": key["Candidate - Arabic Fluency Level"],
                "describe_your_it_skills": key["Candidate - Describe your IT skills"],
                "skill_1": key["Candidate - Skill 1"],
                "skill_2": key["Candidate - skill 2"],
                "skill_3": key["Candidate - Skill 3"],
                "skill_4": key["Candidate - Skill 4"],
                "skill_5" : key["Candidate - Skill 5"],
                "skill_6" : key["Candidate - Skill 6"],
                "volunteer_experience" :  key["Candidate - Do you have volunteering experience?"],
                "preferred_volunteer_role" : key["Candidate - Do you have a preferred volunteer role?"],
                "have_wheelchair" : key["Candidate - Do you use a wheelchair?"],
                "fwc_are_you_interested_in_a_leadership_role" : key["Candidate - FWC Are you interested in a leadership role? (The data you provide will be used as a reference; other roles may be assigned)"],
                "fwc_leadership_experience":  key["Candidate - FWC Leadership Experience"],
                "ceremonies_yes_no" : key["Candidate - Ceremonies yes no"],
                "cast_yes_no" : key["Candidate - Cast yes no"],
                "certified_translator" : key["Candidate - Certified translator"],
                "certified_translator_language" : key["Candidate - Certified Translator Language"],
                "collaboration_score" : key["Candidate - Collaboration Score"],
                "cast_options" : key["Candidate - Cast options"],
                "motivation_score" : key["Candidate - Motivation Score"],
                "pioneer" : key["Candidate - Pioneer"],
                "international_volunteer" : key["Candidate - International Volunteer Yes/No"],
                "fwc_what_is_availability" : key["Candidate - FWC What is your availability?"],
                "availability_during_tournament" : key["Candidate - Availability  during tournament Alfa"],
                "daily_availability_shift_morning" : key["Candidate - Daily availability shift morning Alfa"],
                "daily_availability_shift_afternoon" : key["Candidate - Daily availability shift afternoon Alfa"],
                "daily_availability_shift_night" : key["Candidate - Daily availability shift evening Alfa"],
                "daily_availability_shift_overnight" : key["Candidate - Daily availability shift overnight Alfa"],
                "group_interview" :  key["Candidate - Group Interview Comment"],
                "municipality_address" : key["Candidate - Municipality (Address)"], 
                "updated_at": datetime.now()
                }
                updated_users.append(update_user)
        if saved_users != []:
            print(datetime.now(), "saving")
            db.bulk_insert_mappings(models.Volunteers, saved_users)
            print(datetime.now())
            db.commit()
            print(datetime.now())
        if updated_users != []:
            print("updated users")
            print(datetime.now())
            db.bulk_update_mappings(models.Volunteers, updated_users)
            db.commit()
    else:
        return { "status": status.HTTP_400_BAD_REQUEST, "result": "Duplicate ID", "message": duplicate_ids_excel}



@app.get('/record-history')
def record_history(db: Session = Depends(get_db)):
    users = []
    users_db = db.query(models.Volunteers).all()
    history_db = db.query(models.Histories).all() 
    for user in users_db:
        for history in history_db:
            if user.candidate_id == history.user_id:
                print(user.status.name, 'user')
                print(history.status, 'history')
                if user.status.name == history.status:
                    print('abcdfh')
    # user = {
    #     "user_id": "id",
    #     "status": "stat",
    #     "role_offer_id": "role_id"
    # }


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)