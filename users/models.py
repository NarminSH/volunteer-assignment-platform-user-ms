
from datetime import datetime
import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, Text
from users.database import Base


# class StatusEnum(enum.Enum):
#     Assigned = "Assigned"
#     Pending = "Waitlisted"
#     Accepted = "Accepted"
#     Confirmed = "Confirmed"
#     Complete = "Complete"
#     Declined = "Declined"
#     Removed = "Removed"
#     Expired = "Expired"
#     Waitlist_offered = "Waitlist Offered"
#     Waitlist_accepted = "Waitlist Accepted"
#     Waitlist_declined = "Waitlist Declined"
#     Pre_assigned = "Pre-assigned"
#     Not_approved = "Not Approved"
#     Waitlist_assigned = "Waitlist Assigned"


#     class __metaclass__(type):
#         def __getattr__(self, name):
#             if name in self.values:
#                 return 'here'



class Volunteers(Base):
    __tablename__ = "volunteers"

    candidate_id = Column(Integer, primary_key=True, index=True, nullable=False)
    residence_country = Column(String)
    nationality = Column(String)
    gender = Column(String)
    dob = Column(String)
    delivery_score = Column(Integer) 
    current_occupation = Column(String)
    qatari_driving_lisence = Column(String)
    driving_license_type = Column(String)
    international_accommodation = Column(String)
    medical_condition = Column(String)
    disability = Column(String)
    disability_type = Column(String)
    disability_others = Column(String)
    social_worker = Column(String)
    dietary_requirement = Column(String)
    special_dietary = Column(String)
    alergies_other = Column(String)
    covid_19_vaccinated = Column(String)
    final_dose_date = Column(String)
    education = Column( String)
    area_of_study = Column(String)
    english_level = Column(String)
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
    other_languages = Column(String)
    describe_your_it_skills = Column(String) 
    interpretation_experience = Column(String)
    interpretation_language = Column(String)
    skill_1 = Column(String)
    skill_2 = Column(String)
    skill_3 = Column(String)
    skill_4 = Column(String)    
    skill_5 = Column(String)
    skill_6 = Column(String)
    previous_volunteer = Column(String)
    volunteer_experience = Column(String)
    other_volunteer_experience = Column(String)
    participated_event_type = Column(String)
    event_type_other = Column(String)
    preferred_volunteer_role = Column( String)
    are_you_interested_in_a_leadership_role = Column(String)
    leadership_experience = Column(String)
    relevant_experience = Column(Text)
    ceremonies_yes_no = Column(String)
    cast_yes_no = Column(String) 
    cast_options = Column(String)
    why_interested_in_fifa = Column(Text)
    rearrange_schedule = Column(String)
    international_volunteer = Column(String)
    collaboration_score = Column(Integer)
    motivation_score = Column(Integer)
    fwc_availability_pre_tournament_one = Column(String)
    fwc_availability_pre_tournament_two = Column(String)
    availability_during_tournament = Column(String)
    daily_availability_shift_morning = Column(String)
    daily_availability_shift_afternoon = Column(String)
    daily_availability_shift_evening = Column(String)
    daily_availability_shift_overnight = Column(String)
    under_18 = Column(String)
    special_group = Column(String)
    municipality_address = Column(String) 
    previous_role_offer = Column(String)
    pioneer = Column(String)
    checkpoint = Column(String)
    reasonable_adjustments = Column(String)
    event_experience = Column(String)
    passion_score = Column(String)
    commitment_score = Column(String)
    team_leader_experience = Column(String)
    team_leader_qualities = Column(String)
    team_leader_recommendation = Column(String)
    availability = Column(String)
    experience_recommendation = Column(String)
    soft_skills = Column(String)
    technical_skills = Column(String)
    recommend_as_volunteer = Column(String)
    rejection_justification = Column(String)
    interview_notes = Column(String)
    interview_name = Column(String)
    why_rejected_candidate = Column(String)
    role_offer_id = Column(Integer)
    status = Column(String)
    created_at = Column(DateTime)
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime)
    updated_at = Column(DateTime)



class Histories(Base):
    __tablename__ = "histories"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(Integer)
    status = Column(String)
    role_offer_id = Column(String)
    created_at = Column(DateTime, default=datetime.now())
