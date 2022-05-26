
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
        id_value = i["id"]
        if id_value not in all_ids_excel:
            all_ids_excel.append(id_value)
        else:
            if id_value not in duplicate_ids_excel:
                duplicate_ids_excel.append(id_value)

    print(datetime.now(), 'before all')
    users = db.query(models.Volunteers).all()
    print(datetime.now(), 'after all')
    print(len(users), 'all users in db')
    all_candidate_ids_in_db = []
    for user in users:
        all_candidate_ids_in_db.append(user.candidate_id)

    print(datetime.now())
    saved_users = []
    updated_users = []    
    if duplicate_ids_excel == []: 
        for key in all_users_in_excel:
            candidate_id = key["id"]
            if candidate_id not in all_candidate_ids_in_db:
                new_user = {
                "candidate_id": candidate_id,
                "residence_country": key["Country of Residence"],
                "nationality": key["Nationality"],
                "checkpoint": key["checkpoint"],
                "gender": key["Candidate - Gender"],
                "dob": key["Date of birth"],    
                "current_occupation": key["current_occupation"],
                "qatari_driving_lisence": key["Candidate - Qatari Driving License"],    
                "driving_license_type": key["Candidate - Qatar Driving License Type"],  
                "international_accommodation": key["Candidate - International Accommodation Preference"],   
                "medical_condition": key["Candidate - Medical Conditions"],     
                "disability": key["Candidate - Disability"],    
                "disability_type": key["Candidate - Disability type"],   
                "disability_others": key["Candidate - Disability Others"],     
                "social_worker": key["Candidate - Social Worker / Caregiver Support"],     
                "dietary_requirement": key["Candidate - Dietary requirement Identification"],   
                "special_dietary": key["Candidate - Special Dietary Options"],   
                "alergies_other": key["Alergies other"],    
                "covid_19_vaccinated": key["COVID-19 Vaccinated"],   
                "final_dose_date": key["Final Vaccine Dose Date"],   
                "education": key["Candidate - Education"],
                "area_of_study": key["Area of Study"],
                "english_level": key["English Fluency"]   ,
                "english_fluency_level": key["English Fluency Level"],     
                "arabic_fluency_level": key["Arabic Fluency Level"],  
                "additional_language_1": key["Additional Language 1"],
                "additional_language_1_fluency_level": key["Additional Language 1 Fluency Level"],
                "additional_language_2": key["Additional Language 2"],
                "additional_language_2_fluency_level": key["Additional Language 2 Fluency Level"], 
                "additional_language_3": key["Additional Language 3"],
                "additional_language_3_fluency_level": key["Additional Language 3 Fluency Level"],
                "additional_language_4": key["Additional Language 4"],
                "additional_language_4_fluency_level": key["Additional Language 4 Fluency Level"],
                "other_languages": key["Other languages"],
                "interpretation_experience": key["Interpretation Experience"],
                "interpretation_language": key["Interpretation Language Experience?"],
                "delivery_score": key["Delivering Amazing Score"],
                "describe_your_it_skills": key["Describe your IT skills"],
                "skill_1": key["Skill 1"],
                "skill_2": key["Skill 2"],
                "skill_3": key["Skill 3"],
                "skill_4": key["Skill 4"],
                "skill_5" : key["Skill 5"],
                "skill_6" : key["Skill 6"],
                "previous_volunteer": key["Have you volunteered previously?"],
                "volunteer_experience" :  key["What function have you supported during your past volunteering experiences?"],
                "other_volunteer_experience": key["Other Volunteer Experience"],
                "participated_event_type": key["Which type event have you participated in?"],
                "event_type_other": key["Event Type Other"],
                "preferred_volunteer_role" : key["Do you have a preferred volunteer function?"],
                "are_you_interested_in_a_leadership_role" : key["are you interested in a leadership role"],
                "leadership_experience":  key["Please provide examples of past leadership experience"],
                "relevant_experience": key["Any relevant experience you would like to share to support your application?"],
                "ceremonies_yes_no" : key["Would you like to be involved in a ceremonies role?"],
                "cast_yes_no" : key["Are you interested to be part of a ceremonies cast?"],
                "collaboration_score" : key["Collaboration Score"],
                "cast_options" : key["Do you have experience or interest in any of these subjects?"],
                "why_interested_in_fifa": key["Why are you interested in volunteering for the FIFA World Cup 2022?"],
                "rearrange_schedule": key["Are you prepared to take leave or rearrange your schedule to commit to the minimum of ten days?"],
                "international_volunteer": key["Local / International Volunteer"],
                "fwc_availability_pre_tournament_one": key["FWC availability pre tournament stage one Alfa"],
                "fwc_availability_pre_tournament_two": key["FWC availability pre tournament stage Two Alfa"],
                "motivation_score" : key["Motivation Score"],
                "pioneer" : key["Pioneer"], 
                "availability_during_tournament" : key["Availability during tournament Alfa"],
                "daily_availability_shift_morning" : key["Daily availability shift morning Alfa"],
                "daily_availability_shift_afternoon" : key["Daily availability shift afternoon Alfa"],
                "daily_availability_shift_evening" : key["Daily availability shift evening Alfa"],
                "daily_availability_shift_overnight" : key["Daily availability shift overnight Alfa"],
                "under_18": key["Under 18"],
                "special_group": key["Special Groups [International]"],
                "previous_role_offer": key["FAC Previous Role offer"],
                "reasonable_adjustments": key["reasonable adjustments"],
                "event_experience": key["Previous Event Experience"],
                "passion_score": key["Passion & Excitement Score"],
                "commitment_score": key["Commitment to Success Score"],
                "team_leader_experience": key["Team Leader Experience"],
                "team_leader_qualities": key["Team Leader Qualities"],
                "team_leader_recommendation": key["Team Leader Recommendation"],
                "availability": key["Availability"],
                "experience_recommendation": key["FA Experience Recommendation"],
                "soft_skills": key["Soft Skills Demonstrated"],
                "technical_skills": key["Technical Skills"],
                "recommend_as_volunteer": key["Recommend as Q22 Volunteer"],
                "rejection_justification": key["Rejection Justification"],
                "interview_notes": key["Interview Notes / Comments"],
                "interview_name": key["Interviewer Name"],
                "why_rejected_candidate": key["Explain us why you have rejected the candidate in detail"],
                "role_offer_status": key["Role Offer Status"],
                "municipality_address" : key["Municipality Address"], 
                "created_at": datetime.now()
                }
                saved_users.append(new_user)
            else:
                update_user = {
                "candidate_id": candidate_id,
                "residence_country": key["Country of Residence"],
                "nationality": key["Nationality"],
                "checkpoint": key["checkpoint"],
                "gender": key["Candidate - Gender"],
                "dob": key["Date of birth"],    
                "current_occupation": key["current_occupation"],
                "qatari_driving_lisence": key["Candidate - Qatari Driving License"],    
                "driving_license_type": key["Candidate - Qatar Driving License Type"],  
                "international_accommodation": key["Candidate - International Accommodation Preference"],   
                "medical_condition": key["Candidate - Medical Conditions"],     
                "disability": key["Candidate - Disability"],    
                "disability_type": key["Candidate - Disability type"],   
                "disability_others": key["Candidate - Disability Others"],     
                "social_worker": key["Candidate - Social Worker / Caregiver Support"],     
                "dietary_requirement": key["Candidate - Dietary requirement Identification"],   
                "special_dietary": key["Candidate - Special Dietary Options"],   
                "alergies_other": key["Alergies other"],    
                "covid_19_vaccinated": key["COVID-19 Vaccinated"],   
                "final_dose_date": key["Final Vaccine Dose Date"],   
                "education": key["Candidate - Education"],
                "area_of_study": key["Area of Study"],
                "english_level": key["English Fluency"]   ,
                "english_fluency_level": key["English Fluency Level"],     
                "arabic_fluency_level": key["Arabic Fluency Level"],  
                "additional_language_1": key["Additional Language 1"],
                "additional_language_1_fluency_level": key["Additional Language 1 Fluency Level"],
                "additional_language_2": key["Additional Language 2"],
                "additional_language_2_fluency_level": key["Additional Language 2 Fluency Level"], 
                "additional_language_3": key["Additional Language 3"],
                "additional_language_3_fluency_level": key["Additional Language 3 Fluency Level"],
                "additional_language_4": key["Additional Language 4"],
                "additional_language_4_fluency_level": key["Additional Language 4 Fluency Level"],
                "other_languages": key["Other languages"],
                "interpretation_experience": key["Interpretation Experience"],
                "interpretation_language": key["Interpretation Language Experience?"],
                "delivery_score": key["Delivering Amazing Score"],
                "describe_your_it_skills": key["Describe your IT skills"],
                "skill_1": key["Skill 1"],
                "skill_2": key["Skill 2"],
                "skill_3": key["Skill 3"],
                "skill_4": key["Skill 4"],
                "skill_5" : key["Skill 5"],
                "skill_6" : key["Skill 6"],
                "previous_volunteer": key["Have you volunteered previously?"],
                "volunteer_experience" :  key["What function have you supported during your past volunteering experiences?"],
                "other_volunteer_experience": key["Other Volunteer Experience"],
                "participated_event_type": key["Which type event have you participated in?"],
                "event_type_other": key["Event Type Other"],
                "preferred_volunteer_role" : key["Do you have a preferred volunteer function?"],
                "are_you_interested_in_a_leadership_role" : key["are you interested in a leadership role"],
                "leadership_experience":  key["Please provide examples of past leadership experience"],
                "relevant_experience": key["Any relevant experience you would like to share to support your application?"],
                "ceremonies_yes_no" : key["Would you like to be involved in a ceremonies role?"],
                "cast_yes_no" : key["Are you interested to be part of a ceremonies cast?"],
                "collaboration_score" : key["Collaboration Score"],
                "cast_options" : key["Do you have experience or interest in any of these subjects?"],
                "why_interested_in_fifa": key["Why are you interested in volunteering for the FIFA World Cup 2022?"],
                "rearrange_schedule": key["Are you prepared to take leave or rearrange your schedule to commit to the minimum of ten days?"],
                "international_volunteer": key["Local / International Volunteer"],
                "fwc_availability_pre_tournament_one": key["FWC availability pre tournament stage one Alfa"],
                "fwc_availability_pre_tournament_two": key["FWC availability pre tournament stage Two Alfa"],
                "motivation_score" : key["Motivation Score"],
                "pioneer" : key["Pioneer"], 
                "availability_during_tournament" : key["Availability during tournament Alfa"],
                "daily_availability_shift_morning" : key["Daily availability shift morning Alfa"],
                "daily_availability_shift_afternoon" : key["Daily availability shift afternoon Alfa"],
                "daily_availability_shift_evening" : key["Daily availability shift evening Alfa"],
                "daily_availability_shift_overnight" : key["Daily availability shift overnight Alfa"],
                "under_18": key["Under 18"],
                "special_group": key["Special Groups [International]"],
                "previous_role_offer": key["FAC Previous Role offer"],
                "reasonable_adjustments": key["reasonable adjustments"],
                "event_experience": key["Previous Event Experience"],
                "passion_score": key["Passion & Excitement Score"],
                "commitment_score": key["Commitment to Success Score"],
                "team_leader_experience": key["Team Leader Experience"],
                "team_leader_qualities": key["Team Leader Qualities"],
                "team_leader_recommendation": key["Team Leader Recommendation"],
                "availability": key["Availability"],
                "experience_recommendation": key["FA Experience Recommendation"],
                "soft_skills": key["Soft Skills Demonstrated"],
                "technical_skills": key["Technical Skills"],
                "recommend_as_volunteer": key["Recommend as Q22 Volunteer"],
                "rejection_justification": key["Rejection Justification"],
                "interview_notes": key["Interview Notes / Comments"],
                "interview_name": key["Interviewer Name"],
                "why_rejected_candidate": key["Explain us why you have rejected the candidate in detail"],
                "role_offer_status": key["Role Offer Status"],
                "municipality_address" : key["Municipality Address"],
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
            print(datetime.now(), "before committing updated users")
            db.commit()
            print(datetime.now(), "saved updated users")
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
                if user.status.name != history.status:
                    user = {
                        "user_id": user.candidate_id,
                        "status": user.status.name,
                        "role_offer_id": user.role_offer_id
                    }
                    users.append(user)
    print(len(users))
    db.bulk_insert_mappings(models.Histories, users)
    db.commit()


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)