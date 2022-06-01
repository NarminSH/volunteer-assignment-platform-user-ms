
from datetime import datetime
import os.path
from typing import List
import shutil
import numpy as np
from sqlalchemy import inspect, or_, text
import pandas as pd
import uvicorn
from fastapi import FastAPI, Depends, File, UploadFile, status, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from users import models
from users.database import engine, SessionLocal
from users.crud import get_user, filter_users, get_users
from users import models
from fastapi.responses import FileResponse

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



@app.get('/volunteer-fields')
def read_fields():
    field_names_obj = {
    "candidate_id": [],
    "residence_country": [], 
    "nationality": ["AF", "AL", "DZ", "AS","AD", "AO", "AI", "AQ",
    "AG", "AR",'AU' ,'AM' ,'AW' ,'AT' ,'AZ' ,'BS' ,'BH' ,'BD',  'BB', 'BY', 
    'BE', 'BZ', 'BJ', 'BM', 'BT', 'BO', 'BQ', 'BA', 'BW', 'BV', 'BR', 'IO', 
    'BN', "BG", "BF", "BI", "CV", "KH", "CM", "CA", "KY", "CF", "TD", "CL", 
    "CN", "CX", "CC", "CO", "KM", "CD", "CG", "CK", "CR", "HR", "CU", "CW", 
    "CY", "CZ", "CI", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "GQ", "ER", 
    "EE", "SZ", "ET", "FK", "FO", "FJ", "FI", "FR", "GF", "PF", "TF", "GA", 
    "GM", "GE", "DE", "GH", "GI", "GR", "GL", "GD", "GP", "GU", "GT", "GG", 
    "GN", "GW", "GY", "HT", "HM", "VA", "HN", "HK", "HU", "IS", "IN", "ID", 
    "IR", "IQ", "IE", "IM", "IL", "IT", "JM", "JP", "JE", "JO", "KZ", "KE", 
    "KI", "KP", "KR", "KW", "KG", "LA", "LV", "LB", "LS", "LR", "LY", "LI", 
    "LT", "LU", "MO", "MG", "MW", "MY", "MV", "ML", "MT", "MH", "MQ", "MR", 
    "MU", "YT", "MX", "FM", "MD", "MC", "MN", "ME", "MS", "MA", "MZ", "MM", 
    "NA", "NR", "NP", "NL", "NC", "NZ", "NI", "NE", "NG", "NU", "NF", "MP", 
    "NO", "OM", "PK", "PW", "PS", "PA", "PG", "PY", "PE", "PH", "PN", "PL", 
    "PT", "PR", "QA", "MK", "RO", "RU", "RW", "RE", "BL", "SH", "KN", "LC", 
    "MF", "PM", "VC", "WS", "SM", "ST", "SA", "SN", "RS", "SC", "SL", "SG", 
    "SX", "SK", "SI", "SB", "SO", "ZA", "GS", "SS", "ES", "LK", "SD", "SR", 
    "SJ", "SE", "CH", "SY", "TW", "TJ", "TZ", "TH", "TL", "TG", "TK", "TO", 
    "TT", "TN", "TR", "TM", "TC", "TV", "UG", "UA", "AE", "GB", "UM", "US", 
    "UY", "UZ", "VU", "VE", "VN", "VG", "VI", "WF", "EH", "YE", "ZM", "ZW", "AX"],
    "gender": ["Male", "Female"],
    "dob": [],
    "delivery_score": [1,2,3,4,5]  ,
    "current_occupation": ["Student", "Employed", "Unemployed", "Retired", "Other"],
    "qatari_driving_lisence": ["Yes", "No", " "],
    "driving_license_type": ["Car", "Motorcycle", "Minibus (up to 8 people)", "Bus (over 8 people)"],
    "international_accommodation": ["Stay in a Hotel, Hostel or Apartment Rental", "Stay with friends or family"],
    "medical_condition": [],
    "disability": ["Yes", "No", "Prefer not to say"],
    "disability_type": ["a wheelchair user", "a person with limited mobility (non-wheelchair user)", "blind/partially", 
"deaf/hard of hearing", "a person with mental ill health", "other (if other, please specify)", "prefer not to say"],
    "disability_others": [],
    "social_worker": ["Yes", "No", "I don't need support"],
    "dietary_requirement": ["Yes", "No"],
    "special_dietary": ["Celery and products thereof", "Cereals containing gluten and products thereof", "Crustaceans and products thereof", 
    "Eggs and products thereof", "Fish and products thereof", "Lupin and products thereof", "Milk and products thereof (including lactose)", 
    "Molluscs and products thereof", "Mustard and products thereof",
    "Nuts i.e. almond, hazelnuts, walnuts, cashews, pecan nuts, Brazil nuts, pistachio nuts, macadamia/ Queensland nuts and products thereof", 
    "Peanuts and products thereof", "Sesame seeds and products thereof", "Soybeans and products thereof", 
    "Sulphur dioxide and sulphites at concentrations of more than 10 mg/kg or 10 mg/litre", "Others"],
    "alergies_other": [],
    "covid_19_vaccinated": ["Yes", "No"],
    "final_dose_date": [],
    "education": ["Masters/post graduate degree", "Secondary/High School", "Undergraduate degree", "Doctorate", "Other", "Primary"],
    "area_of_study": [],
    "english_level": ["Strong", "Good", "Poor"],
    "english_fluency_level": ["Native", "Fluent", "Intermediate", "Beginner", "I don't speak English"],
    "arabic_fluency_level": ["Native", "Fluent", "Intermediate", "Beginner", "I don't speak Arabic"],
    "additional_language_1": ["Bosnian-Serbian", "Chinese", "Croatian", "Danish", "Dutch", "French", "German", 
    "Greek", "Icelandic", "Italian", "Japanese", "Korean", "Polish", "Portuguese", "Russian", "Serbian", "Spanish", 
    "Swedish", "Other (Please specify in the text box below)"],
    "additional_language_1_fluency_level": ["Intermediate", "Beginner"],
    "additional_language_2": ["Bosnian-Serbian", "Chinese", "Croatian", "Danish", "Dutch", "French", "German", 
    "Greek", "Icelandic", "Italian", "Japanese", "Korean", "Polish", "Portuguese", "Russian", "Serbian", "Spanish", 
    "Swedish", "Other (Please specify in the text box below)"],
    "additional_language_2_fluency_level": ["Intermediate", "Beginner"],
    "additional_language_3": ["Bosnian-Serbian", "Chinese", "Croatian", "Danish", "Dutch", "French", "German", 
    "Greek", "Icelandic", "Italian", "Japanese", "Korean", "Polish", "Portuguese", "Russian", "Serbian", "Spanish", 
    "Swedish", "Other (Please specify in the text box below)"],
    "additional_language_3_fluency_level": ["Intermediate", "Beginner"],
    "additional_language_4": ["Bosnian-Serbian", "Chinese", "Croatian", "Danish", "Dutch", "French", "German", 
    "Greek", "Icelandic", "Italian", "Japanese", "Korean", "Polish", "Portuguese", "Russian", "Serbian", "Spanish", 
    "Swedish", "Other (Please specify in the text box below)"],
    "additional_language_4_fluency_level": ["Intermediate", "Beginner"],
    "other_languages": [],
    "describe_your_it_skills" : ["Expert", "Advanced", "Intermediate", "Basic"],
    "interpretation_experience": ["Yes (Non-certified)", "No", "Yes (Certified)"],
    "interpretation_language": [],
    "skill_1": ["Ability to handle difficult situations", "Adaptability", "Communication & interpersonal skills", 
    "Conflict resolution", "Customer services", "Event management", "IT skills", "Leadership skills", 
    "Mentoring skills & training others", "Multilingual", "Multitasking", "Organisation", "Problem-solving", 
    "Project management", "Public speaking", "Relationship building", "Reporting", "Research", "Social media", 
    "Teamwork", "Time management", "Volunteer management", "Human Rights"],
    "skill_2": ["Ability to handle difficult situations", "Adaptability", "Communication & interpersonal skills", 
    "Conflict resolution", "Customer services", "Event management", "IT skills", "Leadership skills", 
    "Mentoring skills & training others", "Multilingual", "Multitasking", "Organisation", "Problem-solving", 
    "Project management", "Public speaking", "Relationship building", "Reporting", "Research", "Social media", 
    "Teamwork", "Time management", "Volunteer management", "Human Rights"],
    "skill_3": ["Ability to handle difficult situations", "Adaptability", "Communication & interpersonal skills", 
    "Conflict resolution", "Customer services", "Event management", "IT skills", "Leadership skills", 
    "Mentoring skills & training others", "Multilingual", "Multitasking", "Organisation", "Problem-solving", 
    "Project management", "Public speaking", "Relationship building", "Reporting", "Research", "Social media", 
    "Teamwork", "Time management", "Volunteer management", "Human Rights"],
    "skill_4": ["Ability to handle difficult situations", "Adaptability", "Communication & interpersonal skills", 
    "Conflict resolution", "Customer services", "Event management", "IT skills", "Leadership skills", 
    "Mentoring skills & training others", "Multilingual", "Multitasking", "Organisation", "Problem-solving", 
    "Project management", "Public speaking", "Relationship building", "Reporting", "Research", "Social media", 
    "Teamwork", "Time management", "Volunteer management", "Human Rights"],
    "skill_5": ["Ability to handle difficult situations", "Adaptability", "Communication & interpersonal skills", 
    "Conflict resolution", "Customer services", "Event management", "IT skills", "Leadership skills", 
    "Mentoring skills & training others", "Multilingual", "Multitasking", "Organisation", "Problem-solving", 
    "Project management", "Public speaking", "Relationship building", "Reporting", "Research", "Social media", 
    "Teamwork", "Time management", "Volunteer management", "Human Rights"],
    "skill_6": ["Ability to handle difficult situations", "Adaptability", "Communication & interpersonal skills", 
    "Conflict resolution", "Customer services", "Event management", "IT skills", "Leadership skills", 
    "Mentoring skills & training others", "Multilingual", "Multitasking", "Organisation", "Problem-solving", 
    "Project management", "Public speaking", "Relationship building", "Reporting", "Research", "Social media", 
    "Teamwork", "Time management", "Volunteer management", "Human Rights"],
    "previous_volunteer": ["Yes", "No"],
    "volunteer_experience": ["My first volunteering experience", "Customer services", "Supporting people with disabilities", 
    "Supporting vulnerable people", "Transport", "Spectator services", "Fan Zones", "Hospitality", "Medical Services", 
    "Supporting Youth Programmes", "Catering", "Operations or Logistics, Ticketing", 
    "IT", "Administration", "Accreditation", "Broadcasting/TV operations", "Media", "Marketing", "Logistics", 
    "Accommodation", "Protocol & guest management", "Team services", "Anti-doping", "Brand protection", "Match organisation", 
    "Opening/closing ceremonies", "Safety & security", "Sustainability", "Technical services", 'Welcome ceremonies/award ceremonies', 'Other', 'Volunteer Management', 'Venue Management', "Refereeing"],
    "other_volunteer_experience": [],
    "participated_event_type": ["Community events", "Corporate events (conference, congress…)", 
    "FIFA World Cup", "Music festival", "National/region sport competitions", "Summer Olympic Games / Paralympic Games", 
    "Winter Olympic Games / Paralympic Games", "World championship/world cup", "World Expo", "Others", 
    "Continental games", "Football continental competition", "Youth Olympic Games"],
    "event_type_other": [],
    'preferred_volunteer_role': ["I don't have a preference", "Access Management", "Accessibility", "Accreditation",
     "Arrivals and Departures", "Catering", "Ceremonies", "Communications", "Competition Management",
    "Event Promotion", "Fan Zones", "FIFA Fan Fests", "Guest Management and Protocol", "Health & Safety", 
    "Hospitality", "IT", "Language Services", "Last Mile", "Legal (Brand Protection)", "Marketing", 
    "Media Operations", "Medical Services & Doping Control", "Protocol & Guest Management", "Security", 
    "Spectator Services", "Sustainability", "Team and Referee Services", "Workforce Management", "Ticketing", 
    "Transport", "Venue Management", "Workers Welfare", "Corniche Activation", "Fan ID Project", 
    "Broadcasting / TV Operations", "Logistics", "Youth Programme"],
    'are_you_interested_in_a_leadership_role': ["Yes", "No", " "],
    'leadership_experience': [],
    'relevant_experience': [],
    'ceremonies_yes_no': ["Yes", "No"],
    'cast_yes_no' : ["Yes", "No", " "],
    'cast_options': ["Event production", "Hair & Makeup", "Costumes / Fashion", 
    "Scenic / Stage management", "Props", "Audio equipment"],
    'why_interested_in_fifa': ["I have experience in volunteering/enjoy volunteering", "I want to visit Qatar", 
    "I want to give back to Qatar", "I love/am passionate about football", "I want to meet new people", 
    "I want to learn new skills", "I want to be part of one of the biggest sporting events"],
    'rearrange_schedule': ["Yes", "No"],
    'international_volunteer': ["Local", "International"],
    'collaboration_score' : [1,2,3,4,5],
    'motivation_score' : [1,2,3,4,5],
    'fwc_availability_pre_tournament_one': ["Yes", "No", " "],
    'fwc_availability_pre_tournament_two': ["Yes", "No", " "],
    'availability_during_tournament': ["Yes", "No", " "],
    'daily_availability_shift_morning': ["Yes", "No", " "],
    'daily_availability_shift_afternoon': ["Yes", "No", " "],
    'daily_availability_shift_evening': ["Yes", "No", " "],
    'daily_availability_shift_overnight': ["Yes", "No", " "],
    'under_18': ["Yes", "No", " "],
    'special_group': ["Kuwait", "Oman", "Qatar", "Saudi Arabia"],
    'municipality_address' : ["Doha", "Al Daayen", "Al Khor", "Al Wakrah", "Al Rayyan", "Al Shahaniya", "Umm Salal", "Al Shamal"],
    'previous_role_offer': [],
    'pioneer': ["Yes", "No", " "],
    'checkpoint': ["4.1.1 Interview Passed [Local - English]", "4.2.1 Interview Passed [International - English]"],
    'reasonable_adjustments': [],
    'event_experience': [],
    'passion_score': [1,2,3,4,5, " "],
    'commitment_score': [1,2,3,4,5, " "],
    'team_leader_experience': ["Work", "University", "Volunteering", "Sport Events", None],
    'team_leader_qualities': ["Communication", "Team Work", "Positivity", "Diplomatic", 
    "Support", "Motivation", "Punctual", "Trustworthy", "Responsible", "Active Listening"],

    'team_leader_recommendation': ["Yes", "Maybe", "No", " "],

    'availability': ["Understands need to plan schedule", "Already planned leave", 
    "Requires release letter from employer", "States will attend shift after work", 
    "Does not appear to understand shift requirement/commitment"],
    'experience_recommendation': ["N/A", "Access Management", "Accessibility", 
    "Accreditation", "Arrivals and Departures", "Catering", "Cleaning & Waste", 
    "Communications", "Competition Management", "Event Promotion", "Event Transport", 
    "Fan Zones", "Guest Operations", "Health & Safety", "Hospitality", "IT", "Language Services",
    "Legal", "Marketing Rights Delivery", "Media Operations", "Medical Services & Doping Control", 
    "Referee Services", "Q22 Visitor Experience", "Referee Services", "Signage", "Spectator Services", 
    "Sustainability", "Team Services", "Ticketing", "TV Operations", "Venue Management", "Workforce Management", 
    "Last Mile", "Marketing", "Security", "Testing & Ticketing Support"],
    'soft_skills': ["Adaptability", "Attention to detail", "Communication & Interpersonal", "Creativity", 
    "Customer Service", "Decision Making", "Empathy", "Multitasking", "Positive Attitude", "Self-Motivated", 
    "Time Management", "Patience", "Work ethic", "Conflict Resolution", None],

    'technical_skills': ["HR / Interview", "IT (Systems & Software Proficiency)", "Editorial (Typing & Writing)", 
    "Problem-solving (Critical Thinking)", "Trouble Shooting", "Event management", "Leadership skills", 
    "Mentoring skills & training others", "Multilingual", "Multitasking", "Organisation & planning", 
    "Project management", "Public speaking", "Time management", "Teamwork", "Reporting", "Research", 
    "Volunteer management", None],
    'recommend_as_volunteer': ["Yes", "No"],
    'rejection_justification': ["Attitude", "Poor Communication", "No motivation shown", 
    "Interest in watching matches only", "Inappropriate comments", "Lack of commitment", 
    "No understanding of volunteering role and responsibilities", "Unable to respond to Questions", "Poor availability"],
    'interview_notes': [],
    'why_rejected_candidate': [],
    'role_offer_id' : [],
    'status': ["Assigned", "Pending", "Accepted", "Confirmed", "Complete", 
    "Declined", "Removed", "Expired", "Waitlist Offered", "Waitlist Accepted", 
    "Waitlist Declined", "Pre-assigned", "Not Approved", "Waitlist Assigned"]
    }
    return field_names_obj




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


        if requirement == 'Requirement' and operator=='Operator': #if page has just opened
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
                        elif operator == "not":
                            if (getattr(user, requirement)) != value:
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
    



@app.post('/import-users-data')
def import_data(background_task: BackgroundTasks,file: UploadFile = File(...), db: Session = Depends(get_db)):
    background_task.add_task(check_role, db=db, background_task=background_task)
    file_name = file.filename
    print(file_name)

    all_users_in_excel = []
    with open(f'{file.filename}', "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print("got1 here")
    print(datetime.now())
    data = pd.read_excel(file_name, index_col=None)
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

    all_candidate_ids_in_db = db.scalars(db.query(models.Volunteers.candidate_id)).all()

    print(datetime.now(), 'after all')
 
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
                "why_rejected_candidate": key["Explain us why you have rejected the candidate in detail"],
                "status": key["Role Offer Status"],
                "municipality_address" : key["Municipality Address"], 
                "created_at": datetime.now()
                }
                saved_users.append(new_user)
                if len(saved_users) == 100:
                    print(datetime.now(), "saving 100 user")
                    db.bulk_insert_mappings(models.Volunteers, saved_users)
                    print(datetime.now(), 'before committing 100 user')
                    db.commit()
                    print(datetime.now(), 'finished saving 100 user')
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
                "why_rejected_candidate": key["Explain us why you have rejected the candidate in detail"],
                "status": key["Role Offer Status"],
                "municipality_address" : key["Municipality Address"],
                "updated_at": datetime.now()
                }
                updated_users.append(update_user)
        # if saved_users != []:
        #     print(datetime.now(), "saving")
        #     db.bulk_insert_mappings(models.Volunteers, saved_users)
        #     print(datetime.now())
        #     db.commit()
        #     print(datetime.now())
        if updated_users != []:
            print("updated users")
            print(datetime.now())
            print(len(updated_users), "length of updated users before bulk updating")
            db.bulk_update_mappings(models.Volunteers, updated_users)
            print(datetime.now(), "before committing updated users")
            db.commit()
            print(datetime.now(), "saved updated users")
    else:
        return { "statusCode": status.HTTP_400_BAD_REQUEST, "value": "DuplicateID", "message": duplicate_ids_excel}



@app.get('/record-history')
def record_history(db: Session = Depends(get_db)):
    updated_users = []
    users_db = db.query(models.Volunteers).all()
    history_db = db.query(models.Histories).all() 
    history_db_ids = db.scalars(db.query(models.Histories.user_id)).all()
    new_users = []
    existing_candidate_ids = [] #bcz user_id is not unique in history table there can be several objects with same ids, append and check to be unique

    
    print('record-history before for loop')
    print(len(users_db))
    print(len(history_db))
    for user in users_db:
        if user.candidate_id in history_db_ids:
            for history in history_db:
                if user.candidate_id == history.user_id and user.candidate_id not in existing_candidate_ids:
                    descending = db.query(models.Histories).filter(models.Histories.user_id == user.candidate_id).order_by(models.Histories.id.desc())
                    last_item = descending.first()
                    if user.status != last_item.status:
                        print(user.status, last_item.status)
                        existing_candidate_ids.append(user.candidate_id)
                        updated_user = {
                            "user_id": user.candidate_id,
                            "status": user.status,
                            "role_offer_id": user.role_offer_id,
                            "created_at": datetime.now()
                        }
                        updated_users.append(updated_user)
        else:
            new_user = {
            "user_id": user.candidate_id,
            "status": user.status,
            "role_offer_id": user.role_offer_id,
            "created_at": datetime.now()
            }
            new_users.append(new_user)
            print('else statement')
    if new_users != []:
        print('new users in saving record-history', len(new_users))
        db.bulk_insert_mappings(models.Histories, new_users)
        db.commit() 
        print("committed in record history ")
    if updated_users != []:
        print('updating users in saving record-history', len(updated_users))
        db.bulk_insert_mappings(models.Histories, updated_users)
        db.commit()

    print('finished recording history')




@app.get('/export-volunteers')
def export_volunteers(db: Session = Depends(get_db)):
    ids = []
    statuses = []
    role_offers = []
    col1 = "id"
    col2 = "status"
    col3 = "role_offer_id"

    users = db.query(models.Volunteers).from_statement(
    text("""SELECT candidate_id, status, role_offer_id from volunteers;""")).all()

    for user in users:
        print(user.status)
        if user.status is not None:
            print(user.candidate_id, user.status, user.role_offer_id, "All users in export data")
            ids.append(user.candidate_id)
            statuses.append(user.status)
            role_offers.append(user.role_offer_id)

    data = pd.DataFrame({col1:ids,col2:statuses,col3:role_offers})

    data.to_excel('files/export_data.xlsx', sheet_name='sheet1', index=False)

    file_exists = os.path.exists('files/export_data.xlsx')
    
    if file_exists:
        file_path = 'files/export_data.xlsx'
        print('file exists, returning export file in export-volunteers')
        return FileResponse(file_path, filename="export_data.xlsx", media_type="xlsx")
    return { "statusCode": status.HTTP_404_NOT_FOUND, "value": "notexist"}
    


@app.get('/check-role')
def check_role(background_task: BackgroundTasks, db: Session = Depends(get_db)):

    print('inside check role func')

    background_task.add_task(record_history, db=db)

    updated_users = []
    all_users = db.query(models.Volunteers).all()
    for user in all_users:
        if user.status is None and user.role_offer_id is not None:
            print(user.candidate_id, 'candidate id in check role')
            update_user = {
            "candidate_id": user.candidate_id,
            "role_offer_id": None,
            "updated_at": datetime.now()
            }
            updated_users.append(update_user)


    if updated_users != []:
        print('checking role offer to match with statuses, updating length is', len(updated_users))
        db.bulk_update_mappings(models.Volunteers, updated_users)
        db.commit()
        print('committed updated users in check-role')

    print('checked all roles, users who have changes', len(updated_users))



@app.get('/user-history/{candidate_id}')
def read_user_history(candidate_id: int, db: Session = Depends(get_db)):
    histories = db.query(models.Histories).filter(models.Histories.user_id == candidate_id).all()
    return histories




if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)