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

st.write("""
App was devoloped by [Esteban Encina](https://github.com/eeeds)
""")