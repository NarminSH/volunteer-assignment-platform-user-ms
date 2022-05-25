
from datetime import datetime
import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from users.database import Base


class StatusEnum(enum.Enum):
    Assign = "Assigned"
    Waitlist = "Waitlisted"
    Free = "Free"


class Volunteers(Base):
    __tablename__ = "volunteers"

    candidate_id = Column(Integer, primary_key=True, index=True, nullable=False)
    # nationality = Column(String)
    # country_of_residence = Column(String)
    full_name = Column(String)
    checkpoint = Column(String) #?
    gender_for_accreditation = Column(String)
    dob = Column(String)
    delivery_score = Column(Integer)
    current_occupation = Column(String)
    it_skills = Column(String)
    driving_license_type = Column(String)
    residence_country = Column(String)
    accommodation_in_qatar = Column(String)
    disability_yes_no = Column(String)
    disability_type = Column(String)
    covid_19_vaccinated = Column(String)
    education_fwc = Column( String)
    education_speciality = Column(String)
    area_of_study = Column(String)
    english_fluency_level = Column(String)
    arabic_fluency_level = Column(String)
    additional_language_1 = Column( String)
    additional_language_1_fluency_level = Column( String)
    additional_language_2 = Column( String)
    additional_language_2_fluency_level = Column(String)
    additional_language_3 = Column( String)
    additional_language_3_fluency_level = Column( String)
    additional_language_4 = Column( String)
    additional_language_4_fluency_level = Column( String)
    describe_your_it_skills = Column(String)
    skill_1 = Column( String)
    skill_2 = Column(String)
    skill_3 = Column( String)
    skill_4 = Column(String)    
    skill_5 = Column( String)
    skill_6 = Column(String)
    volunteer_experience = Column(String)
    preferred_volunteer_role = Column( String)
    have_wheelchair = Column(String)
    driving_license = Column(String)
    fwc_are_you_interested_in_a_leadership_role = Column(String)
    fwc_leadership_experience = Column(String)
    ceremonies_yes_no = Column(String)
    cast_yes_no = Column(String)
    certified_translator = Column(String)
    certified_translator_language = Column( String)
    collaboration_score = Column(Integer)
    cast_options = Column(String)
    motivation_score = Column(Integer)
    pioneer = Column(String)
    international_volunteer = Column(String)
    fwc_what_is_availability = Column(String)
    availability_during_tournament = Column( String)
    daily_availability_shift_morning = Column(String)
    daily_availability_shift_afternoon = Column(String)
    daily_availability_shift_night = Column(String)
    daily_availability_shift_overnight = Column(String)
    group_interview = Column(String)
    municipality_address = Column(String) 
    role_offer_id = Column(Integer)
    status = Column(Enum(StatusEnum), default=StatusEnum.Free.name)
    created_at = Column(DateTime)
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime)
    updated_at = Column(DateTime)



# class Histories(Base):
#     __tablename__ = "histories"

#     id = Column(Integer, primary_key=True, index=True, nullable=False)
#     user_id = Column(Integer)
#     status = Column(String)
#     role_offer_id = Column(String)
#     created_at = Column(DateTime, default=datetime.now())
