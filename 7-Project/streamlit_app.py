import streamlit  as st 
import pickle

st.write("""
# Attrition Prediction App
This app predicts if a employee will leave the company or not.
"""
)

st.markdown("""
<style>
.big-font {
    font-size:50px !important;
}
</style>
""", unsafe_allow_html=True)

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def load_model():
    model = 'models/pipeline.bin'

    with open(model, 'rb') as f_in:
        pipeline = pickle.load(f_in)

    return pipeline
pipeline = load_model()


business_travel = st.selectbox(
    'Business Travel',
    ('Travel_Frequently', 'Travel_Rarely', 'Non-Travel')
)

department = st.selectbox(
    'Department',
    ('Sales', 'Research & Development', 'Human Resources')
)
education_field = st.selectbox(
    'Education Field',
    ('Life Scienes', 'Medical', 'Marketing', 'Technical Degree', 'Human Resources', 'Other')
)
gender = st.selectbox(
    'Gender',
    ('Female', 'Male')
)

job_role = st.selectbox(
    'Job Role',
    ('Sales Executive', 'Research Scientist', 'Laboratory Technician',
    'Manufacturing Director', 'Healthcare', 'Representative',
    'Manager', 'Sales Representative', 'Research Director',
    'Human Resorces')
)

marital_status = st.selectbox(
    'Marital Status',
    ('Single', 'Married', 'Divorced')
)



# categorical = [
#     "BusinessTravel",
#     "Department",
#     "EducationField",
#     "Gender",
#     "JobRole",
#     "MaritalStatus",
# ]
# # Numerical data
# numerical = [
#     "Age",
#     "DailyRate",
#     "DistanceFromHome",
#     "Education",
#     "EnvironmentSatisfaction",
#     "HourlyRate",
#     "JobInvolvement",
#     "JobLevel",
#     "JobSatisfaction",
#     "MonthlyIncome",
#     "MonthlyRate",
#     "NumCompaniesWorked",
#     "Over18",
#     "OverTime",
#     "PercentSalaryHike",
#     "PerformanceRating",
#     "RelationshipSatisfaction",
#     "StockOptionLevel",
#     "TotalWorkingYears",
#     "TrainingTimesLastYear",
#     "WorkLifeBalance",
#     "YearsAtCompany",
#     "YearsInCurrentRole",
#     "YearsSinceLastPromotion",
#     "YearsWithCurrManager",
# ]
st.write("""
App was devoloped by [Esteban Encina](https://github.com/eeeds)
""")