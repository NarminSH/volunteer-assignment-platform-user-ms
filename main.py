
from datetime import datetime
import os.path
from typing import List
import shutil
import numpy as np
from sqlalchemy import inspect, text
import pandas as pd
import uvicorn
from fastapi import FastAPI, Depends, File, UploadFile, status, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from users import models
from users.database import engine, SessionLocal
from users.crud import get_user, get_users
from users import models
from fastapi.responses import FileResponse
from fastapi import APIRouter
from sqlalchemy.sql import text


URL_PREFIX = os.getenv('URL_PREFIX')


app = FastAPI(docs_url=f'{URL_PREFIX}/docs',openapi_url=f'{URL_PREFIX}/openapi.json')

prefix_router = APIRouter(prefix=f"{URL_PREFIX}")


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


@prefix_router.get('/volunteer-fields')
def read_fields():
    columns = [column.name for column in inspect(models.Volunteers).c]
    return columns


@prefix_router.get('/volunteer-fields-new')
def read_fields():
    field_names_obj = {
    "candidate_id": {
        "type": "input",
        "field_type": "int",
        "value_options": []
        },
    "residence_country": {
        "type": "select",
        "field_type": "string",
        "value_options": ["AF", "AL", "DZ", "AS","AD", "AO", "AI", "AQ",
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
    "UY", "UZ", "VU", "VE", "VN", "VG", "VI", "WF", "EH", "YE", "ZM", "ZW", "AX"] }, 
    "nationality": {
        "type": "select",
        "field_type": "string",
        "value_options": ["AF", "AL", "DZ", "AS","AD", "AO", "AI", "AQ",
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
    "UY", "UZ", "VU", "VE", "VN", "VG", "VI", "WF", "EH", "YE", "ZM", "ZW", "AX"]
        },
    "gender": {
            "type": "select",
            "value_type": "string",
            "value_options": ["Male", "Female"]
        },
    "dob": {
            "type": "input",
            "value_type": "date",
            "value_options": []
        },
    "age":{
        "type": "input",
        "value_type": "int",
        "value_options": []
    },
    "delivery_score": {
            "type": "select",
            "value_type": "int",
            "value_options": [1,2,3,4,5]
        },
    "current_occupation": {
            "type": "select",
            "value_type": "string",
            "value_options": ["Student", "Employed", "Unemployed", "Retired", "Other"]
        },
    "qatari_driving_lisence": {
            "type": "select",
            "value_type": "string",
            "value_options": ["Yes", "No", " "]
        },
    "driving_license_type": {
            "type": "select",
            "value_type": "string",
            "value_options": ["Car", "Motorcycle", "Minibus (up to 8 people)", "Bus (over 8 people)"]
        },
    "international_accommodation": {
            "type": "select",
            "value_type": "string",
            "value_options": ["Stay in a Hotel, Hostel or Apartment Rental", "Stay with friends or family"]
        },
    "medical_condition": {
            "type": "input",
            "value_type": "string",
            "value_options": []
        },
    "disability": {
            "type": "select",
            "value_type": "string",
            "value_options": ["Yes", "No", "Prefer not to say"]
        },
    "disability_type": {
            "type": "select",
            "value_type": "string",
            "value_options": ["a wheelchair user", "a person with limited mobility (non-wheelchair user)", "blind/partially", 
"deaf/hard of hearing", "a person with mental ill health", "other (if other, please specify)", "prefer not to say"]
        },
    "disability_others": {
            "type": "input",
            "value_type": "string",
            "value_options": []
        },
    "social_worker": {
            "type": "select",
            "value_type": "string",
            "value_options": ["Yes", "No", "I don't need support"]
        },
    "dietary_requirement": {
            "type": "select",
            "value_type": "string",
            "value_options": ["Yes", "No"]
        },
    "special_dietary": {
            "type": "select",
            "value_type": "string",
            "value_options": ["Celery and products thereof", "Cereals containing gluten and products thereof", "Crustaceans and products thereof", 
    "Eggs and products thereof", "Fish and products thereof", "Lupin and products thereof", "Milk and products thereof (including lactose)", 
    "Molluscs and products thereof", "Mustard and products thereof",
    "Nuts i.e. almond, hazelnuts, walnuts, cashews, pecan nuts, Brazil nuts, pistachio nuts, macadamia/ Queensland nuts and products thereof", 
    "Peanuts and products thereof", "Sesame seeds and products thereof", "Soybeans and products thereof", 
    "Sulphur dioxide and sulphites at concentrations of more than 10 mg/kg or 10 mg/litre", "Others"]
        },
    "alergies_other": {
            "type": "input",
            "value_type": "string",
            "value_options": []
        },
    "covid_19_vaccinated": {
            "type": "select",
            "value_type": "string",
            "value_options": ["Yes", "No"]
        },
    "final_dose_date": {
            "type": "input",
            "value_type": "string",
            "value_options": []
        },
    "education": {
            "type": "select",
            "value_type": "string",
            "value_options": ["Masters/post graduate degree", "Secondary/High School", "Undergraduate degree", "Doctorate", "Other", "Primary"]
        },
    "area_of_study": {
            "type": "input",
            "value_type": "string",
            "value_options": []
        },
    "english_level": {
            "type": "select",
            "value_type": "string",
            "value_options": ["Strong", "Good", "Poor"]
        },
    "english_fluency_level": {
            "type": "select",
            "value_type": "string",
            "value_options": ["Native", "Fluent", "Intermediate", "Beginner", "I don't speak English"]
        },
    "arabic_fluency_level": {
            "type": "select",
            "value_type": "string",
            "value_options": ["Native", "Fluent", "Intermediate", "Beginner", "I don't speak Arabic"]
        },
        "language": {
            "type": "select",
            "value_type": "string",
            "value_options": ["Bosnian-Serbian", "Chinese", "Croatian", "Danish", "Dutch", "French", "German", 
    "Greek", "Icelandic", "Italian", "Japanese", "Korean", "Polish", "Portuguese", "Russian", "Serbian", "Spanish", 
    "Swedish", "Other (Please specify in the text box below)"]
        },
        "language_fluency_level": {
            "type": "select",
            "value_type": "string",
            "value_options": ["Intermediate", "Beginner"]
        },
    "additional_language_1": {
            "type": "select",
            "value_type": "string",
            "value_options": ["Bosnian-Serbian", "Chinese", "Croatian", "Danish", "Dutch", "French", "German", 
    "Greek", "Icelandic", "Italian", "Japanese", "Korean", "Polish", "Portuguese", "Russian", "Serbian", "Spanish", 
    "Swedish", "Other (Please specify in the text box below)"]
        },
    "additional_language_1_fluency_level": {
            "type": "select",
            "value_type": "string",
            "value_options": ["Intermediate", "Beginner"]
        },
    "additional_language_2": {
            "type": "select",
            "value_type": "string",
            "value_options": ["Bosnian-Serbian", "Chinese", "Croatian", "Danish", "Dutch", "French", "German", 
    "Greek", "Icelandic", "Italian", "Japanese", "Korean", "Polish", "Portuguese", "Russian", "Serbian", "Spanish", 
    "Swedish", "Other (Please specify in the text box below)"]
        },
    "additional_language_2_fluency_level": {
            "type": "select",
            "value_type": "string",
            "value_options": ["Intermediate", "Beginner"]
        },
    "additional_language_3": {
            "type": "select",
            "value_type": "string",
            "value_options": ["Bosnian-Serbian", "Chinese", "Croatian", "Danish", "Dutch", "French", "German", 
    "Greek", "Icelandic", "Italian", "Japanese", "Korean", "Polish", "Portuguese", "Russian", "Serbian", "Spanish", 
    "Swedish", "Other (Please specify in the text box below)"]
        },
    "additional_language_3_fluency_level": {
            "type": "select",
            "value_type": "string",
            "value_options": ["Intermediate", "Beginner"]
        },
    "additional_language_4":{
            "type": "select",
            "value_type": "string",
            "value_options": ["Bosnian-Serbian", "Chinese", "Croatian", "Danish", "Dutch", "French", "German", 
    "Greek", "Icelandic", "Italian", "Japanese", "Korean", "Polish", "Portuguese", "Russian", "Serbian", "Spanish", 
    "Swedish", "Other (Please specify in the text box below)"]
        },
    "additional_language_4_fluency_level": {
            "type": "select",
            "value_type": "string",
            "value_options": ["Intermediate", "Beginner"]
        },
    "other_languages": {
            "type": "input",
            "value_type": "string",
            "value_options": []
        },
    "describe_your_it_skills" : {
            "type": "select",
            "value_type": "string",
            "value_options": ["Expert", "Advanced", "Intermediate", "Basic"]
        },
    "interpretation_experience": {
            "type": "select",
            "value_type": "string",
            "value_options": ["Yes (Non-certified)", "No", "Yes (Certified)"]
        },
    "interpretation_language": {
            "type": "input",
            "value_type": "string",
            "value_options": []
        },
    "skill":{
        "type": "select",
            "value_type": "string",
            "value_options": ["Ability to handle difficult situations", "Adaptability", "Communication & interpersonal skills", 
    "Conflict resolution", "Customer services", "Event management", "IT skills", "Leadership skills", 
    "Mentoring skills & training others", "Multilingual", "Multitasking", "Organisation", "Problem-solving", 
    "Project management", "Public speaking", "Relationship building", "Reporting", "Research", "Social media", 
    "Teamwork", "Time management", "Volunteer management", "Human Rights"]
    },
    "skill_1": {
            "type": "select",
            "value_type": "string",
            "value_options": ["Ability to handle difficult situations", "Adaptability", "Communication & interpersonal skills", 
    "Conflict resolution", "Customer services", "Event management", "IT skills", "Leadership skills", 
    "Mentoring skills & training others", "Multilingual", "Multitasking", "Organisation", "Problem-solving", 
    "Project management", "Public speaking", "Relationship building", "Reporting", "Research", "Social media", 
    "Teamwork", "Time management", "Volunteer management", "Human Rights"]
        },
    "skill_2": {
            "type": "select",
            "value_type": "string",
            "value_options": ["Ability to handle difficult situations", "Adaptability", "Communication & interpersonal skills", 
    "Conflict resolution", "Customer services", "Event management", "IT skills", "Leadership skills", 
    "Mentoring skills & training others", "Multilingual", "Multitasking", "Organisation", "Problem-solving", 
    "Project management", "Public speaking", "Relationship building", "Reporting", "Research", "Social media", 
    "Teamwork", "Time management", "Volunteer management", "Human Rights"]
        },
    "skill_3": {
            "type": "select",
            "value_type": "string",
            "value_options": ["Ability to handle difficult situations", "Adaptability", "Communication & interpersonal skills", 
    "Conflict resolution", "Customer services", "Event management", "IT skills", "Leadership skills", 
    "Mentoring skills & training others", "Multilingual", "Multitasking", "Organisation", "Problem-solving", 
    "Project management", "Public speaking", "Relationship building", "Reporting", "Research", "Social media", 
    "Teamwork", "Time management", "Volunteer management", "Human Rights"]
        },
    "skill_4": {
            "type": "select",
            "value_type": "string",
            "value_options": ["Ability to handle difficult situations", "Adaptability", "Communication & interpersonal skills", 
    "Conflict resolution", "Customer services", "Event management", "IT skills", "Leadership skills", 
    "Mentoring skills & training others", "Multilingual", "Multitasking", "Organisation", "Problem-solving", 
    "Project management", "Public speaking", "Relationship building", "Reporting", "Research", "Social media", 
    "Teamwork", "Time management", "Volunteer management", "Human Rights"]
        },
    "skill_5": {
            "type": "select",
            "value_type": "string",
            "value_options": ["Ability to handle difficult situations", "Adaptability", "Communication & interpersonal skills", 
    "Conflict resolution", "Customer services", "Event management", "IT skills", "Leadership skills", 
    "Mentoring skills & training others", "Multilingual", "Multitasking", "Organisation", "Problem-solving", 
    "Project management", "Public speaking", "Relationship building", "Reporting", "Research", "Social media", 
    "Teamwork", "Time management", "Volunteer management", "Human Rights"]
        },
    "skill_6": {
            "type": "select",
            "value_type": "string",
            "value_options": ["Ability to handle difficult situations", "Adaptability", "Communication & interpersonal skills", 
    "Conflict resolution", "Customer services", "Event management", "IT skills", "Leadership skills", 
    "Mentoring skills & training others", "Multilingual", "Multitasking", "Organisation", "Problem-solving", 
    "Project management", "Public speaking", "Relationship building", "Reporting", "Research", "Social media", 
    "Teamwork", "Time management", "Volunteer management", "Human Rights"]
        },
    "previous_volunteer": {
            "type": "select",
            "value_type": "string",
            "value_options": ["Yes", "No"]
        },
    "volunteer_experience": {
            "type": "select",
            "value_type": "string",
            "value_options": ["My first volunteering experience", "Customer services", "Supporting people with disabilities", 
    "Supporting vulnerable people", "Transport", "Spectator services", "Fan Zones", "Hospitality", "Medical Services", 
    "Supporting Youth Programmes", "Catering", "Operations or Logistics, Ticketing", 
    "IT", "Administration", "Accreditation", "Broadcasting/TV operations", "Media", "Marketing", "Logistics", 
    "Accommodation", "Protocol & guest management", "Team services", "Anti-doping", "Brand protection", "Match organisation", 
    "Opening/closing ceremonies", "Safety & security", "Sustainability", "Technical services", 'Welcome ceremonies/award ceremonies', 
    'Other', 'Volunteer Management', 'Venue Management', "Refereeing"]
        },
    "other_volunteer_experience": {
            "type": "input",
            "value_type": "string",
            "value_options": []
        },
    "participated_event_type": {
            "type": "select",
            "value_type": "string",
            "value_options": ["Community events", "Corporate events (conference, congress…)", 
    "FIFA World Cup", "Music festival", "National/region sport competitions", "Summer Olympic Games / Paralympic Games", 
    "Winter Olympic Games / Paralympic Games", "World championship/world cup", "World Expo", "Others", 
    "Continental games", "Football continental competition", "Youth Olympic Games"]
        },
    "event_type_other": {
            "type": "input",
            "value_type": "string",
            "value_options": []
        },
    'preferred_volunteer_role': {
            "type": "select",
            "value_type": "string",
            "value_options": ["I don't have a preference", "Access Management", "Accessibility", "Accreditation",
     "Arrivals and Departures", "Catering", "Ceremonies", "Communications", "Competition Management",
    "Event Promotion", "Fan Zones", "FIFA Fan Fests", "Guest Management and Protocol", "Health & Safety", 
    "Hospitality", "IT", "Language Services", "Last Mile", "Legal (Brand Protection)", "Marketing", 
    "Media Operations", "Medical Services & Doping Control", "Protocol & Guest Management", "Security", 
    "Spectator Services", "Sustainability", "Team and Referee Services", "Workforce Management", "Ticketing", 
    "Transport", "Venue Management", "Workers Welfare", "Corniche Activation", "Fan ID Project", 
    "Broadcasting / TV Operations", "Logistics", "Youth Programme"]
        },
    'are_you_interested_in_a_leadership_role': {
            "type": "select",
            "value_type": "string",
            "value_options": ["Yes", "No", " "]
        },
    'leadership_experience': {
            "type": "input",
            "value_type": "string",
            "value_options": []
        },
    'relevant_experience': {
            "type": "input",
            "value_type": "string",
            "value_options": []
        },
    'ceremonies_yes_no': {
            "type": "select",
            "value_type": "string",
            "value_options": ["Yes", "No"]
        },
    'cast_yes_no' : {
            "type": "select",
            "value_type": "string",
            "value_options": ["Yes", "No", " "]
        },
    'cast_options': {
            "type": "select",
            "value_type": "string",
            "value_options": ["Event production", "Hair & Makeup", "Costumes / Fashion", 
    "Scenic / Stage management", "Props", "Audio equipment"]
        },
    'why_interested_in_fifa': {
            "type": "select",
            "value_type": "string",
            "value_options": ["I have experience in volunteering/enjoy volunteering", "I want to visit Qatar", 
    "I want to give back to Qatar", "I love/am passionate about football", "I want to meet new people", 
    "I want to learn new skills", "I want to be part of one of the biggest sporting events"]
        },
    'rearrange_schedule': {
            "type": "select",
            "value_type": "string",
            "value_options": ["Yes", "No"]
        },
    'international_volunteer': {
            "type": "select",
            "value_type": "string",
            "value_options": ["Local", "International"]
        },
    'collaboration_score' : {
            "type": "select",
            "value_type": "int",
            "value_options": [1,2,3,4,5]
        },
    'motivation_score' : {
            "type": "select",
            "value_type": "int",
            "value_options": [1,2,3,4,5]
        },
    'fwc_availability_pre_tournament_one': {
            "type": "select",
            "value_type": "string",
            "value_options": ["Yes", "No"]
        },
    'fwc_availability_pre_tournament_two': {
            "type": "select",
            "value_type": "string",
            "value_options":["Yes", "No"]
        },
    'availability_during_tournament': {
            "type": "select",
            "value_type": "string",
            "value_options": ["Yes", "No"]
        },
    'daily_availability_shift_morning': {
            "type": "select",
            "value_type": "string",
            "value_options": ["Yes", "No"]
        },
    'daily_availability_shift_afternoon': {
            "type": "select",
            "value_type": "string",
            "value_options": ["Yes", "No"]
        },
    'daily_availability_shift_evening': {
            "type": "select",
            "value_type": "string",
            "value_options": ["Yes", "No"]
        },
    'daily_availability_shift_overnight': {
            "type": "select",
            "value_type": "string",
            "value_options": ["Yes", "No"]
        },
    'under_18': {
            "type": "select",
            "value_type": "string",
            "value_options": ["Yes", "No"]
        },
    'special_group': {
            "type": "select",
            "value_type": "string",
            "value_options": ["Kuwait", "Oman", "Qatar", "Saudi Arabia"]
        },
    'municipality_address' : {
            "type": "select",
            "value_type": "string",
            "value_options": ["Doha", "Al Daayen", "Al Khor", "Al Wakrah", "Al Rayyan", "Al Shahaniya", "Umm Salal", "Al Shamal"]
        },
    'previous_role_offer': [],
    'pioneer': {
            "type": "select",
            "value_type": "string",
            "value_options": ["Yes", "No"]
        },
    'checkpoint': {
            "type": "select",
            "value_type": "string",
            "value_options": ["4.1.1 Interview Passed [Local - English]", "4.2.1 Interview Passed [International - English]"]
        },
    'reasonable_adjustments': {
            "type": "input",
            "value_type": "string",
            "value_options": []
        },
    'event_experience': {
            "type": "input",
            "value_type": "string",
            "value_options": []
        },
    'passion_score': {
            "type": "select",
            "value_type": "int",
            "value_options": [1,2,3,4,5]
        },
    'commitment_score': {
            "type": "select",
            "value_type": "int",
            "value_options": [1,2,3,4,5]
        },
    'team_leader_experience': {
            "type": "select",
            "value_type": "string",
            "value_options": ["Work", "University", "Volunteering", "Sport Events", None]
        },
    'team_leader_qualities': {
            "type": "select",
            "value_type": "string",
            "value_options": ["Communication", "Team Work", "Positivity", "Diplomatic", 
    "Support", "Motivation", "Punctual", "Trustworthy", "Responsible", "Active Listening"]
        },

    'team_leader_recommendation': {
            "type": "select",
            "value_type": "string",
            "value_options": ["Yes", "Maybe", "No"]
        },

    'availability': {
            "type": "select",
            "value_type": "string",
            "value_options": ["Understands need to plan schedule", "Already planned leave", 
    "Requires release letter from employer", "States will attend shift after work", 
    "Does not appear to understand shift requirement/commitment"],
    'experience_recommendation': ["N/A", "Access Management", "Accessibility", 
    "Accreditation", "Arrivals and Departures", "Catering", "Cleaning & Waste", 
    "Communications", "Competition Management", "Event Promotion", "Event Transport", 
    "Fan Zones", "Guest Operations", "Health & Safety", "Hospitality", "IT", "Language Services",
    "Legal", "Marketing Rights Delivery", "Media Operations", "Medical Services & Doping Control", 
    "Referee Services", "Q22 Visitor Experience", "Referee Services", "Signage", "Spectator Services", 
    "Sustainability", "Team Services", "Ticketing", "TV Operations", "Venue Management", "Workforce Management", 
    "Last Mile", "Marketing", "Security", "Testing & Ticketing Support"]
        },
    'soft_skills': {
            "type": "select",
            "value_type": "string",
            "value_options": ["Adaptability", "Attention to detail", "Communication & Interpersonal", "Creativity", 
    "Customer Service", "Decision Making", "Empathy", "Multitasking", "Positive Attitude", "Self-Motivated", 
    "Time Management", "Patience", "Work ethic", "Conflict Resolution", None]
        },

    'technical_skills': {
            "type": "select",
            "value_type": "string",
            "value_options": ["HR / Interview", "IT (Systems & Software Proficiency)", "Editorial (Typing & Writing)", 
    "Problem-solving (Critical Thinking)", "Trouble Shooting", "Event management", "Leadership skills", 
    "Mentoring skills & training others", "Multilingual", "Multitasking", "Organisation & planning", 
    "Project management", "Public speaking", "Time management", "Teamwork", "Reporting", "Research", 
    "Volunteer management", None]
        },
    'recommend_as_volunteer': {
            "type": "select",
            "value_type": "string",
            "value_options": ["Yes", "No"]
        },
    'rejection_justification': {
            "type": "select",
            "value_type": "string",
            "value_options": ["Attitude", "Poor Communication", "No motivation shown", 
    "Interest in watching matches only", "Inappropriate comments", "Lack of commitment", 
    "No understanding of volunteering role and responsibilities", "Unable to respond to Questions", "Poor availability"]
        },
    'interview_notes': {
            "type": "input",
            "value_type": "string",
            "value_options": []
        },
    'why_rejected_candidate':{
            "type": "input",
            "value_type": "string",
            "value_options": []
        },
    'role_offer_id' : {
            "type": "input",
            "value_type": "int",
            "value_options": []
        },
    'status': {
            "type": "select",
            "value_type": "string",
            "value_options": ["Assigned", "Pending", "Accepted", "Confirmed", "Complete", 
            "Declined", "Removed", "Expired", "Waitlist Offered", "Waitlist Accepted", 
            "Waitlist Declined", "Pre-assigned", "Not Approved", "Waitlist Assigned"]
        },
    'partner_code': {
            "type": "input",
            "value_type": "int",
            "value_options": []
        }
    }
    return field_names_obj




@prefix_router.get('/volunteers')
def read_volunteers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users



@prefix_router.get('/volunteers/{user_id}')
def read_volunteer(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db=db, user_id=user_id)
    return user    


@prefix_router.post('/filter-volunteers')
def filter_volunteers(filter_list: List, page_number: int = 1, page_size:int = 10, db: Session = Depends(get_db)):
    print(filter_list)

    start = (page_number-1) * page_size
    end = start + page_size

    final_where_statement = ""
    for filter_index, filter in enumerate(filter_list):
        print(filter_index, filter)
        requirement = filter["requirement_name"]
        
        operators_dict = {
            "equal":"=",
            "not equal": "!=",
            "contains": "ILIKE",
            ">": ">",
            "<": "<",
            ">=": ">=",
            "<=": "<="
        }

        if filter["value"] == [] and filter["operator"] == "equal" and requirement == "skill":
            final_where_statement += f"((skill_1 IS NULL) or (skill_2 IS NULL) or (skill_3 IS NULL) or (skill_4 IS NULL) or (skill_5 IS NULL) or (skill_6 IS NULL))"

        if filter["value"] == [] and filter["operator"] ==  "not equal" and requirement == "skill": 
            final_where_statement += f"((skill_1 IS NOT NULL) or (skill_2 IS NOT NULL) or (skill_3 IS NOT NULL) or (skill_4 IS NOT NULL) or (skill_5 IS NOT NULL) or (skill_6 IS NOT NULL))"

        if filter["value"] == [] and filter["operator"] == "equal" and requirement == "language":
            final_where_statement += f"((additional_language_1 IS NULL) or (additional_language_2 IS NULL) or (additional_language_3 IS NULL) or (additional_language_4 IS NULL))"

        if filter["value"] == [] and filter["operator"] ==  "not equal" and requirement == "language": 
            final_where_statement += f"((additional_language_1 IS NOT NULL) or (additional_language_2 IS NOT NULL) or (additional_language_3 IS NOT NULL) or (additional_language_4 IS NOT NULL))"
        
        if filter["value"] == [] and filter["operator"] ==  "not equal" and requirement == "language_fluency_level": 
            final_where_statement += f"((additional_language_1_fluency_level IS NOT NULL) or (additional_language_2_fluency_level IS NOT NULL) or (additional_language_3_fluency_level IS NOT NULL) or (additional_language_4_fluency_level IS NOT NULL))"

        if filter["value"] == [] and filter["operator"] == "equal" and (requirement != "skill" and requirement != "language" and requirement != "language_fluency_level"):
            final_where_statement += f"({requirement} IS NULL)"

        if filter["value"] == [] and filter["operator"] == "not equal" and (requirement != "skill" and requirement != "language" and requirement != "language_fluency_level"):
            final_where_statement += f"({requirement} IS NOT NULL)"

        if filter["value"] != []:
            single_where_statement = ""
            single_where_statement += "("
            for index, val in enumerate(filter["value"]):
                operator = operators_dict[filter["operator"]]
                if "don't" in val:
                    val = val.replace("don't", "don''t")
                
                if requirement == "skill":
                    unique_skills = ["skill_1", "skill_2", "skill_3", "skill_4", "skill_5", "skill_6"]
                    for index_req, req in enumerate(unique_skills):
                        single_where_statement += f"{req} {operator} '{val}' "
                        if index_req != len(unique_skills)-1:
                            single_where_statement += " or "
                        if index_req == len(unique_skills)-1 and index != len(filter["value"])-1:
                            single_where_statement += " or "

                if requirement == "language":
                    unique_languages = ["additional_language_1", "additional_language_2", "additional_language_3", "additional_language_4"]
                    for index_lan, lan in enumerate(unique_languages):
                        single_where_statement += f"{lan} {operator} '{val}'"
                        if index_lan != len(unique_languages)-1:
                            single_where_statement += " or "
                        if index_lan == len(unique_languages)-1 and index != len(filter["value"])-1:
                            single_where_statement += " or "
                
                if requirement == "language_fluency_level":
                    unique_fluency_levels = ["additional_language_1_fluency_level", "additional_language_2_fluency_level", "additional_language_3_fluency_level", "additional_language_4_fluency_level"]
                    for index_fluency, fluency in enumerate(unique_fluency_levels):
                        single_where_statement += f"{fluency} {operator} '{val}'"
                        if index_fluency != len(unique_fluency_levels)-1:
                            single_where_statement += " or "
                        if index_fluency == len(unique_fluency_levels)-1 and index != len(filter["value"])-1:
                            single_where_statement += " or "
                
                if requirement != "skill" and requirement != "language" and requirement != "language_fluency_level":
                    single_where_statement += f"{requirement} {operator} '{val}'"
                    if index != len(filter["value"])-1:
                        single_where_statement += " or "
            single_where_statement += ")"
            final_where_statement += single_where_statement

        if filter_index != len(filter_list)-1:
            final_where_statement += " and "  
    
    print(final_where_statement, "finaq request to be executed")

    fin_req = f"WHERE {final_where_statement}" if final_where_statement != "" else ""

    users = db.query(models.Volunteers).from_statement(
    text(f"""SELECT * from volunteers {fin_req};""")).all()
    print(len(users), 'matched users count')

    response = {
        "data": users[start:end],
        "total_pages": len(users)
    }
    return response
    


@prefix_router.post('/import-users-data/')
def import_data(email:str, background_task: BackgroundTasks, file: UploadFile = File(...), db: Session = Depends(get_db)):

    background_task.add_task(check_role, db=db)
    background_task.add_task(record_history, db=db, email=email)
    
    file_name = file.filename
    print(file_name)

    all_users_in_excel = []
    with open(f'{file.filename}', "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print("got1 here")
    print(datetime.now())
    data = pd.read_excel(file_name, index_col=None)
    volunteer_data = data.astype(object).replace(np.nan, None)
    print('finished replacing none to null values in import', datetime.now())

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
    print(len(all_candidate_ids_in_db), 'all candidates in db')

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
                "age": key["age"],
                "partner_code": key["Partner / Affiliation Code"],
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
                "why_rejected_candidate": key["Explain us why you have rejected the candidate in detail"],
                "status": key["Role Offer Status"],
                "municipality_address" : key["Municipality Address"],
                "age": key["age"],
                "partner_code": key["Partner / Affiliation Code"],
                "updated_at": datetime.now()
                }
                updated_users.append(update_user)
        if saved_users != []:
            print(len(saved_users), "length of saved users before bulk saving")
            print(datetime.now(), "saving")
            db.bulk_insert_mappings(models.Volunteers, saved_users)
            print(datetime.now(), 'before committing saved users')
            db.commit()
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



@prefix_router.get('/record-history')
def record_history(email: str, db: Session = Depends(get_db)):
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
                        existing_candidate_ids.append(user.candidate_id)
                        updated_user = {
                            "user_id": user.candidate_id,
                            "status": user.status,
                            "role_offer_id": user.role_offer_id,
                            "recorded_by": email,
                            "created_at": datetime.now()
                        }
                        updated_users.append(updated_user)
        else:
            new_user = {
            "user_id": user.candidate_id,
            "status": user.status,
            "role_offer_id": user.role_offer_id,
            "recorded_by": email,
            "created_at": datetime.now()
            }
            new_users.append(new_user)
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




@prefix_router.get('/export-volunteers')
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
    


@prefix_router.get('/check-role')
def check_role(db: Session = Depends(get_db)):

    print('inside check role func')


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



@prefix_router.get('/user-history/{candidate_id}')
def read_user_history(candidate_id: int, db: Session = Depends(get_db)):
    histories = db.query(models.Histories).filter(models.Histories.user_id == candidate_id).all()
    print(len(histories), "user-histories")
    return histories



@prefix_router.post('/report')
def reporting(report_list: dict, db: Session = Depends(get_db)):
    print(report_list, 'report list from front')
    template_name = report_list["template_name"]
    ro_columns = report_list["role_columns"]
    vol_columns = report_list["vol_columns"]
    ro_filters = report_list["role_filters"]
    vol_filters = report_list["vol_filters"]

    volunteer_columns = []
    role_columns = []
    all_cols = []
    final_statement = ""

    operators_dict = {
            "equal":"=",
            "not equal": "!=",
            "contains": "ILIKE",
            ">": ">",
            "<": "<",
            ">=": ">=",
            "<=": "<="
        }

    for vol in vol_columns:
        vs = f"volunteers.{vol}"
        volunteer_columns.append(vs)

    for role in ro_columns:
        rl = f"{role}.name"
        role_columns.append(rl)

    all_cols = volunteer_columns + role_columns
    print(all_cols)

    select_statement = "SELECT "
    final_where_statement = ""
    for col_index, col_value in enumerate(all_cols):
        select_statement += col_value
        if col_index != len(all_cols)-1:
            select_statement += ", "


    for vol_index, vol_filter in enumerate(vol_filters):
        requirement = vol_filter["requirement_name"]

        if vol_filter["value"] == [] and vol_filter["operator"] == "equal":
            final_where_statement += f"(volunteers.{requirement} IS NULL)"

        if vol_filter["value"] == [] and vol_filter["operator"] == "not equal":
            final_where_statement += f"(volunteers.{requirement} IS NOT NULL)"

        if vol_filter["value"] != []:
            single_where_statement = ""
            single_where_statement += "("
            for index, val in enumerate(vol_filter["value"]):
                operator = operators_dict[vol_filter["operator"]]
                if "don't" in val:
                    val = val.replace("don't", "don''t")
                
                if requirement == "skill":
                    unique_skills = ["skill_1", "skill_2", "skill_3", "skill_4", "skill_5", "skill_6"]
                    for index_req, req in enumerate(unique_skills):
                        single_where_statement += f"volunteers.{req} {operator} '{val}' "
                        if index_req != len(unique_skills)-1:
                            single_where_statement += " or "
                        if index_req == len(unique_skills)-1 and index != len(vol_filter["value"])-1:
                            single_where_statement += " or "

                if requirement == "language":
                    unique_languages = ["additional_language_1", "additional_language_2", "additional_language_3", "additional_language_4"]
                    for index_lan, lan in enumerate(unique_languages):
                        single_where_statement += f"volunteers.{lan} {operator} '{val}'"
                        if index_lan != len(unique_languages)-1:
                            single_where_statement += " or "
                        if index_lan == len(unique_languages)-1 and index != len(vol_filter["value"])-1:
                            single_where_statement += " or "
                
                if requirement == "language_fluency_level":
                    unique_fluency_levels = ["additional_language_1_fluency_level", "additional_language_2_fluency_level", "additional_language_3_fluency_level", "additional_language_4_fluency_level"]
                    for index_fluency, fluency in enumerate(unique_fluency_levels):
                        single_where_statement += f"volunteers.{fluency} {operator} '{val}'"
                        if index_fluency != len(unique_fluency_levels)-1:
                            single_where_statement += " or "
                        if index_fluency == len(unique_fluency_levels)-1 and index != len(vol_filter["value"])-1:
                            single_where_statement += " or "
                
                if requirement != "skill" and requirement != "language" and requirement != "language_fluency_level":
                    single_where_statement += f"volunteers.{requirement} {operator} '{val}'"
                    if index != len(vol_filter["value"])-1:
                        single_where_statement += " or "
            single_where_statement += ")"
            final_where_statement += single_where_statement

        if vol_index != len(vol_filters)-1:
            final_where_statement += " and "


    if vol_filters != [] and ro_filters != []:
        final_where_statement += " and "

    for role_index, role_filter in enumerate(ro_filters):

        requirement = role_filter["requirement_name"]

        if role_filter["value"] == [] and role_filter["operator"] == "equal":
            final_where_statement += f"({requirement}.name IS NULL)"

        if role_filter["value"] == [] and role_filter["operator"] == "not equal":
            final_where_statement += f"({requirement}.name IS NOT NULL)"

        if role_filter["value"] != []:
            single_where_statement = ""
            single_where_statement += "("
            for index, val in enumerate(role_filter["value"]):
                operator = operators_dict[role_filter["operator"]]
                if "don't" in val:
                    val = val.replace("don't", "don''t")
                                
                single_where_statement += f"{requirement}.name {operator} '{val}'"
                if index != len(role_filter["value"])-1:
                    single_where_statement += " or "
            single_where_statement += ")"
            final_where_statement += single_where_statement

        if role_index != len(ro_filters)-1:
            final_where_statement += " and "

    
    fin_req = f"WHERE {final_where_statement}" if final_where_statement != "" else ""

    join_statement = " From role_offers ro FULL JOIN  functional_area_types Entity on ro.functional_area_type_id = Entity.id FULL JOIN functional_areas Functional_Area on ro.functional_area_id = Functional_Area.id FULL JOIN job_titles Job_Title on ro.job_title_id = Job_Title.id FULL JOIN locations Location on ro.location_id = Location.id FULL JOIN volunteers on volunteers.role_offer_id = ro.id "
    final_statement = f"{select_statement}{join_statement}{fin_req}"
    print(final_statement, 'final statement in reporting')
        
    rows = engine.execute(text(final_statement))
    reported_users = []
    for row in rows:
        reported_users.append(row)
    
    data = pd.DataFrame(reported_users, columns=all_cols)
    data.to_excel(f'files/{template_name}.xlsx', sheet_name='sheet1', index=False)

    file_exists = os.path.exists(f'files/{template_name}.xlsx')
    
    if file_exists:
        file_path = f'files/{template_name}.xlsx'
        print('file exists, returning export file in export-volunteers')
        return FileResponse(file_path, filename=f"{template_name}.xlsx", media_type="xlsx")
    return { "statusCode": status.HTTP_404_NOT_FOUND, "value": "notexist"}
   




app.include_router(prefix_router)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)