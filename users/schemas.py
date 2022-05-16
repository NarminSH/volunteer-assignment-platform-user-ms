from typing import List
from pydantic import BaseModel


class Volunteer(BaseModel):
    id: int
    first_name: str
    last_name: str
    picture: str
    email: str
    phone: str
    nationality: str
    country_issued: str
    gender_for_accreditation: str
    dob: str
    current_occupation: str
    id_document_type: str
    qid_number: str
    id_document_expiry_date_q22: str
    passport_number: str
    id_document_expiry_date: str
    id_document_country_of_issue: str
    passport_expiry_date: str
    passport_type: str
    qatari_driving_license: str
    driving_license_type: str
    country: str
    international_accommodation_preference: str
    medical_conditions: str
    disability_yes_no: str
    disability_type: str
    disability_others: str
    social_worker_caregiver_support: str
    dietary_requirement_identification: str
    special_dietary_options: str
    alergies_other: str
    covid_19_vaccinated: str
    vaccine_type_multi_select: str
    final_vaccine_dose_date: str
    education_onechoice: str
    area_of_study: str
    english_fluency_level: str
    arabic_fluency_level: str
    additional_language_1: str
    additional_language_1_fluency_level: str
    additional_language_2: str
    additional_language_2_fluency_level: str
    additional_language_3: str
    additional_language_3_fluency_level: str
    additional_language_4: str
    additional_language_4_fluency_level: str
    languages_other: str
    interpretation_and_translation_experience: str
    certified_translator_language: str
    describe_your_it_skills: str
    skill_1: str
    skill_2: str
    skill_3: str
    skill_4: str
    skill_5: str
    skill_6: str
    previous_volunteering_experience: str
    volunteer_experience: str
    other_role: str
    events_type_participations: str
    other_event_type: str
    volunteer_hours_yearly: str
    preferred_functional_area: str
    fwc_are_you_interested_in_a_leadership_role: str
    fwc_leadership_experience: str
    work_experience: str
    ceremonies_yes_no: str
    cast_yes_no: str
    cast_options: str
    motivation_to_volunteer_at_fwc: str
    leave_or_arrange: str
    local__international_volunteer: str
    language_path_english__arabic: str
    fwc_availability_pre_tournament_stage_one: str
    fwc_availability_pre_tournament_stage_two: str
    availability_during_tournament: str
    daily_availability_shift_morning: str
    daily_availability_shift_afternoon: str
    daily_availability_shift_night: str
    daily_availability_shift_overnight: str
    candidate_under_18: str
    special_groups_international: str
    municipality_address: str


class FilterUser(BaseModel):
    field: str
    operator: str
    value: str


class FilterList(BaseModel):
    users: List[FilterUser]


class UserCreate(BaseModel):
    gender_for_accreditation: str
    dob: str
    current_occupation: str
    country: str
    