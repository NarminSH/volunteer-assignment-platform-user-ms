from sqlalchemy.orm import Session
from . import models

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Volunteers).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int):
    return db.query(models.Volunteers).filter(models.Volunteers.id == user_id).first()


def filter_users(db: Session, field, operator, value):
    print(field,operator, value, 'query get user filter func')

    if operator == '=':
        print('operator is =')
        return db.query(models.Volunteers).filter(getattr(models.Volunteers, field) == value).all()
    elif operator == '>':
        print('operator is >')
        return db.query(models.Volunteers).filter(getattr(models.Volunteers, field) > value).all()
    elif operator == '<':
        print('operator is <')
        return db.query(models.Volunteers).filter(getattr(models.Volunteers, field) < value).all()
    elif operator == '>=':
        print('operator is >=')
        return db.query(models.Volunteers).filter(getattr(models.Volunteers, field) >= value).all()
    elif operator == '<=':
        print('operator is <=')
        return db.query(models.Volunteers).filter(getattr(models.Volunteers, field) <= value).all()
    elif operator == 'contains':
        print('operator is contains')
        return db.query(models.Volunteers).filter(getattr(models.Volunteers, field).contains(value)).all()


def create_user(db: Session, user_id: str,   first_name : str,
    last_name : str,
    picture : str,
    email : str,
    phone : str,
    nationality : str,
    _country_issued : str,
    gender_for_accreditation : str,
    dob: str,
    current_occupation : str,
    id_document_type : str,
    qid_number : str,
    id_document_expiry_date_q22: str,
    passport_number : str,
    id_document_expiry_date: str,
    id_document_country_of_issue : str,
    passport_expiry_date : str,
    passport_type : str,
    qatari_driving_license: str,
    driving_license_type : str,
    country : str,
    international_accommodation_preference : str,
    medical_conditions : str,
    disability_yes_no: str,
    disability_type: str,
    disability_others : str,
    social_worker_caregiver_support : str,
    dietary_requirement_identification : str,
    special_dietary_options : str,
    alergies_other : str,
    covid_19_vaccinated : str,
    vaccine_type_multi_select : str,
    final_vaccine_dose_date : str,
    education_onechoice : str,
    area_of_study : str,
    english_fluency_level : str,
    arabic_fluency_level : str,
    additional_language_1 : str,
    additional_language_1_fluency_level : str,
    additional_language_2 : str,
    additional_language_2_fluency_level : str,
    additional_language_3 : str,
    additional_language_3_fluency_level : str,
    additional_language_4 : str,
    additional_language_4_fluency_level : str,
    languages_other : str,
    interpretation_and_translation_experience : str,
    certified_translator_language : str,
    describe_your_it_skills : str,
    skill_1 : str,
    skill_2 : str,
    skill_3 : str,
    skill_4 : str,
    skill_5 : str,
    skill_6 : str,
    previous_volunteering_experience : str,
    volunteer_experience : str,
    other_role : str,
    events_type_participations : str,
    other_event_type : str,
    volunteer_hours_yearly : str,
    preferred_functional_area : str,
    fwc_are_you_interested_in_a_leadership_role : str,
    fwc_leadership_experience : str,
    work_experience : str,
    ceremonies_yes_no: str,
    cast_yes_no : str,
    cast_options : str,
    motivation_to_volunteer_at_fwc : str,
    leave_or_arrange : str,
    local__international_volunteer : str,
    language_path_english__arabic : str,
    fwc_availability_pre_tournament_stage_one : str,
    fwc_availability_pre_tournament_stage_two : str,
    availability_during_tournament : str,
    daily_availability_shift_morning : str,
    daily_availability_shift_afternoon : str,
    daily_availability_shift_night : str,
    daily_availability_shift_overnight : str,
    candidate_under_18 : str,
    special_groups_international : str,
    municipality_address : str):


    new_user = models.Volunteers(id= user_id, first_name=first_name, last_name=last_name, picture=picture, email=email,
    phone=phone,nationality=nationality,_country_issued=_country_issued,gender_for_accreditation=gender_for_accreditation,
    dob=dob,current_occupation=current_occupation,id_document_type=id_document_type,qid_number=qid_number,
    id_document_expiry_date_q22=id_document_expiry_date_q22,passport_number=passport_number,
    id_document_expiry_date = id_document_expiry_date,
    id_document_country_of_issue = id_document_country_of_issue, passport_expiry_date = passport_expiry_date,
    passport_type = passport_type,
    qatari_driving_license = qatari_driving_license,
    driving_license_type = driving_license_type,
    country =country, international_accommodation_preference = international_accommodation_preference,
    medical_conditions = medical_conditions,
    disability_yes_no = disability_yes_no,
    disability_type = disability_type,
    disability_others =disability_others,
    social_worker_caregiver_support = social_worker_caregiver_support,
    dietary_requirement_identification = dietary_requirement_identification,
    special_dietary_options = special_dietary_options,
    alergies_other = alergies_other,
    covid_19_vaccinated =covid_19_vaccinated,
    vaccine_type_multi_select = vaccine_type_multi_select,
    final_vaccine_dose_date = final_vaccine_dose_date,
    education_onechoice = education_onechoice,
    area_of_study = area_of_study,
    english_fluency_level = english_fluency_level,
    arabic_fluency_level = arabic_fluency_level,
    additional_language_1 = additional_language_1,
    additional_language_1_fluency_level = additional_language_1_fluency_level,
    additional_language_2 = additional_language_2,
    additional_language_2_fluency_level = additional_language_2_fluency_level,
    additional_language_3 = additional_language_3,
    additional_language_3_fluency_level = additional_language_3_fluency_level,
    additional_language_4 = additional_language_4,
    additional_language_4_fluency_level = additional_language_4_fluency_level,
    languages_other = languages_other,
    interpretation_and_translation_experience = interpretation_and_translation_experience,
    certified_translator_language = certified_translator_language,
    describe_your_it_skills = describe_your_it_skills,
    skill_1 = skill_1,
    skill_2 = skill_2,
    skill_3 = skill_3,
    skill_4 = skill_4,
    skill_5 = skill_5,
    skill_6 = skill_6,
    previous_volunteering_experience = previous_volunteering_experience,
    volunteer_experience = volunteer_experience,
    other_role = other_role,
    events_type_participations = events_type_participations,
    other_event_type = other_event_type,
    volunteer_hours_yearly = volunteer_hours_yearly,
    preferred_functional_area = preferred_functional_area,
    fwc_are_you_interested_in_a_leadership_role = fwc_are_you_interested_in_a_leadership_role,
    fwc_leadership_experience = fwc_leadership_experience,
    work_experience = work_experience,
    ceremonies_yes_no = ceremonies_yes_no,
    cast_yes_no = cast_yes_no,
    cast_options = cast_options,
    motivation_to_volunteer_at_fwc = motivation_to_volunteer_at_fwc,
    leave_or_arrange = leave_or_arrange,
    local__international_volunteer = local__international_volunteer,
    language_path_english__arabic = language_path_english__arabic,
    fwc_availability_pre_tournament_stage_one = fwc_availability_pre_tournament_stage_one,
    fwc_availability_pre_tournament_stage_two = fwc_availability_pre_tournament_stage_two,
    availability_during_tournament = availability_during_tournament,
    daily_availability_shift_morning = daily_availability_shift_morning,
    daily_availability_shift_afternoon = daily_availability_shift_afternoon,
    daily_availability_shift_night = daily_availability_shift_night,
    daily_availability_shift_overnight = daily_availability_shift_overnight,
    candidate_under_18 = candidate_under_18,
    special_groups_international = special_groups_international,
    municipality_address = municipality_address )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user