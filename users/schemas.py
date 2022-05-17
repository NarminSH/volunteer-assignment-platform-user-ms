from typing import List, Optional
from pydantic import BaseModel


class Volunteers(BaseModel):
    id: Optional[int] = None
    candidate_id: Optional[int] = None
    full_name: Optional[str] = None
    checkpoint :Optional[str] = None
    gender_for_accreditation: Optional[str] = None
    dob: Optional[str] = None
    delivery_score: Optional[str] = None
    current_occupation: Optional[str] = None
    it_skills: Optional[str] = None
    driving_license_type: Optional[str] = None
    residence_country: Optional[str] = None
    accommodation_in_qatar: Optional[str] = None
    disability_yes_no: Optional[str] = None
    disability_type: Optional[str] = None
    covid_19_vaccinated: Optional[str] = None
    education_fwc: Optional[str] = None
    education_speciality: Optional[str] = None
    area_of_study: Optional[str] = None
    english_fluency_level: Optional[str] = None
    arabic_fluency_level: Optional[str] = None
    additional_language_1: Optional[str] = None
    additional_language_1_fluency_level: Optional[str] = None
    additional_language_2: Optional[str] = None
    additional_language_2_fluency_level: Optional[str] = None
    additional_language_3: Optional[str] = None
    additional_language_3_fluency_level: Optional[str] = None
    additional_language_4: Optional[str] = None
    additional_language_4_fluency_level: Optional[str] = None
    describe_your_it_skills: Optional[str] = None
    skill_1: Optional[str] = None
    skill_2: Optional[str] = None
    skill_3: Optional[str] = None
    skill_4: Optional[str] = None
    skill_5: Optional[str] = None
    skill_6: Optional[str] = None
    volunteer_experience: Optional[str] = None
    preferred_volunteer_role: Optional[str] = None
    have_wheelchair: Optional[str] = None
    driving_license: Optional[str] = None
    fwc_are_you_interested_in_a_leadership_role: Optional[str] = None
    fwc_leadership_experience: Optional[str] = None
    ceremonies_yes_no: Optional[str] = None
    cast_yes_no: Optional[str] = None
    certified_translator: Optional[str] = None
    certified_translator_language: Optional[str] = None
    collaboration_score: Optional[str] = None
    cast_options: Optional[str] = None
    motivation_score: Optional[str] = None
    pioneer: Optional[str] = None
    international_volunteer: Optional[str] = None
    fwc_what_is_availability: Optional[str] = None
    availability_during_tournament: Optional[str] = None
    daily_availability_shift_morning: Optional[str] = None
    daily_availability_shift_afternoon: Optional[str] = None
    daily_availability_shift_night: Optional[str] = None
    group_interview: Optional[str] = None
    municipality_address: Optional[str] = None 
    role_offer_id: Optional[str] = None


class FilterUser(BaseModel):
    requirement: Optional[str] = None
    operator: Optional[str] = None
    value: Optional[str] = None


class FilterList(BaseModel):
    users: List[FilterUser]


class UserCreate(BaseModel):
    gender_for_accreditation: Optional[str] = None
    dob: Optional[str] = None
    current_occupation: Optional[str] = None
    country: Optional[str] = None
    