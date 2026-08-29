import sys
import os
import pandas as pd
import streamlit as st

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.set_page_config(page_title="Resume Match Labeling", layout="wide")

def load_data():
    resume_csv = os.path.join(os.path.dirname(__file__), '..', 'data', 'Resume.csv')
    jd_csv = os.path.join(os.path.dirname(__file__), '..', 'data', 'job_title_des.csv')
    
    resume_df = pd.read_csv(resume_csv).dropna(subset=['Resume_str', 'Category'])
    jd_df = pd.read_csv(jd_csv).dropna(subset=['Job Title', 'Job Description'])
    return resume_df, jd_df

def main():
    st.title("🎯 Resume/JD Labeling Interface")
    st.write("Help train the Machine Learning weights by labeling these pairs as a Match (1) or No Match (0).")
    
    resume_df, jd_df = load_data()
    
    labeled_csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'labeled_matches.csv')
    if os.path.exists(labeled_csv_path):
        labeled_df = pd.read_csv(labeled_csv_path)
    else:
        labeled_df = pd.DataFrame(columns=['Resume_Category', 'Resume_Text', 'JD_Title', 'JD_Text', 'Label'])
        
    st.sidebar.metric("Labels Collected", len(labeled_df))
    st.sidebar.write("Goal: 20-50 labels")
    
    # Generate random pair
    if 'current_resume' not in st.session_state:
        st.session_state.current_resume = resume_df.sample(1).iloc[0]
        st.session_state.current_jd = jd_df.sample(1).iloc[0]
        
    res = st.session_state.current_resume
    jd = st.session_state.current_jd
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"Resume: {res['Category']}")
        st.text_area("Resume Text", res['Resume_str'], height=400, disabled=True)
        
    with col2:
        st.subheader(f"Job Description: {jd['Job Title']}")
        st.text_area("JD Text", jd['Job Description'], height=400, disabled=True)
        
    st.divider()
    st.subheader("Does this Resume match this Job Description?")
    
    c1, c2, c3, _ = st.columns([1, 1, 1, 5])
    
    def save_label(label):
        nonlocal labeled_df
        new_row = {
            'Resume_Category': res['Category'],
            'Resume_Text': res['Resume_str'],
            'JD_Title': jd['Job Title'],
            'JD_Text': jd['Job Description'],
            'Label': label
        }
        labeled_df = pd.concat([labeled_df, pd.DataFrame([new_row])], ignore_index=True)
        labeled_df.to_csv(labeled_csv_path, index=False)
        # Reset state to force new random pair
        del st.session_state.current_resume
        del st.session_state.current_jd
        st.rerun()

    with c1:
        if st.button("✅ YES (Match)", use_container_width=True, type="primary"):
            save_label(1)
    with c2:
        if st.button("❌ NO (Mismatch)", use_container_width=True):
            save_label(0)
    with c3:
        if st.button("⏭️ SKIP", use_container_width=True):
            del st.session_state.current_resume
            del st.session_state.current_jd
            st.rerun()

if __name__ == '__main__':
    main()
