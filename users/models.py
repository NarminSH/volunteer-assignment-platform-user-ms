import enum
from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, Enum
from users.database import Base


class StatusEnum(enum.Enum):
    Assign = "Assigned"
    Waitlist = "Waitlisted"
    Free = "Free"


class Volunteers(Base):
    __tablename__ = "volunteers"

    id = Column('Candidate - ID', Integer, primary_key=True, index=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    picture = Column(String)
    email = Column(String)
    phone = Column(String)
    nationality = Column(String)
    _country_issued = Column(String)
    gender_for_accreditation = Column('Candidate - Gender Qatar', String)
    dob = Column('Candidate - Date of Birth', Date)
    current_occupation = Column(String)
    id_document_type = Column(String)
    qid_number = Column(String)
    id_document_expiry_date_q22 = Column(Date)
    passport_number = Column(String)
    id_document_expiry_date = Column(Date)
    id_document_country_of_issue = Column(String)
    passport_expiry_date = Column(Date)
    passport_type = Column(String)
    qatari_driving_license = Column(Boolean)
    driving_license_type = Column(String)
    country = Column(String)
    international_accommodation_preference = Column(String)
    medical_conditions = Column(String)
    disability_yes_no = Column(Boolean)
    disability_type = Column(String)
    disability_others = Column(String)
    social_worker_caregiver_support = Column(String)
    dietary_requirement_identification = Column(String)
    special_dietary_options = Column(String)
    alergies_other = Column(String)
    covid_19_vaccinated = Column(String)
    vaccine_type_multi_select = Column(String)
    final_vaccine_dose_date = Column(String)
    education_onechoice = Column(String)
    area_of_study = Column(String)
    english_fluency_level = Column(String)
    arabic_fluency_level = Column(String)
    additional_language_1 = Column(String)
    additional_language_1_fluency_level = Column(String)
    additional_language_2 = Column(String)
    additional_language_2_fluency_level = Column(String)
    additional_language_3 = Column(String)
    additional_language_3_fluency_level = Column(String)
    additional_language_4 = Column(String)
    additional_language_4_fluency_level = Column(String)
    languages_other = Column(String)
    interpretation_and_translation_experience = Column(String)
    certified_translator_language = Column(String)
    describe_your_it_skills = Column(String)
    skill_1 = Column(String)
    skill_2 = Column(String)
    skill_3 = Column(String)
    skill_4 = Column(String)
    skill_5 = Column(String)
    skill_6 = Column(String)
    previous_volunteering_experience = Column(String)
    volunteer_experience = Column(String)
    other_role = Column(String)
    events_type_participations = Column(String)
    other_event_type = Column(String)
    volunteer_hours_yearly = Column(String)
    preferred_functional_area = Column(String)
    fwc_are_you_interested_in_a_leadership_role = Column(String)
    fwc_leadership_experience = Column(String)
    work_experience = Column(String)
    ceremonies_yes_no = Column(Boolean)
    cast_yes_no = Column(Boolean)
    cast_options = Column(String)
    motivation_to_volunteer_at_fwc = Column(String)
    leave_or_arrange = Column(String)
    local__international_volunteer = Column(String)
    language_path_english__arabic = Column(String)
    fwc_availability_pre_tournament_stage_one = Column(String)
    fwc_availability_pre_tournament_stage_two = Column(String)
    availability_during_tournament = Column(String)
    daily_availability_shift_morning = Column(String)
    daily_availability_shift_afternoon = Column(String)
    daily_availability_shift_night = Column(String)
    daily_availability_shift_overnight = Column(String)
    candidate_under_18 = Column(String)
    special_groups_international = Column(String)
    municipality_address = Column(String) 
    role_offer_id = Column(Integer)
    status = Column(Enum(StatusEnum), default="Free")
    created_at = Column(DateTime)
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime)
    updated_at = Column(DateTime)


