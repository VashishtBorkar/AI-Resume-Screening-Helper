import streamlit as st
from app.resume_parser import extract_text_from_pdf
from app.skill_extractor import extract_skills
from app.question_generator import generate_questions
from visualizations import plot_bubble_cloud

def main():
    st.title("AI Resume Interviewer ")

    uploaded_file = st.file_uploader("Choose a file", type="pdf")
    # requirements = st.text_area("Enter job requirements (keywords or sentences):")

    if uploaded_file is not None:
        resume_text = extract_text_from_pdf(uploaded_file)
        extracted_skills = extract_skills(resume_text)

        st.markdown("### 🛠️ Detected Skills:")
        st.info("Select skills to generate questions")
            
        selected_skills = []

        if extracted_skills:
            num_cols = 3
            cols = st.columns(num_cols)
            for i, (skill, score) in enumerate(extracted_skills):
                with cols[i % num_cols]:
                    if st.checkbox(f"{skill}", key=f"skill_{i}"):
                        selected_skills.append(skill)
            st.write("")

        if st.button("Generate Question"):
            if selected_skills:
                with st.spinner("Generating questions..."):
                    qa_pairs = generate_questions(selected_skills)

                st.markdown("### Suggested Interview Questions:")
                st.write("")
                for pair in qa_pairs:
                    st.markdown(f"**Q:** {pair['question']}")
                    st.markdown(f"**A:** {pair['answer']}")
                    st.markdown("---")
            else:
                st.warning("Please select at least one skill before generating questions.")


if __name__ == "__main__":
    main()
