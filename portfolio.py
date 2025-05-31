import streamlit as st
from streamlit_analytics import track

with track():
    # Page config
    st.set_page_config(page_title="Ayman Ismaili Portfolio", layout="centered")

    # Header with columns for name and contact info
    col1, col2 = st.columns([2, 3])
    with col1:
        st.title("Ayman Ismaili")
        st.markdown("**Industrial Engineering, AI & Data Science**")
    with col2:
        st.markdown(
            """
            <div style='text-align: right'>
            Meknès, Morocco<br>
            ismailiayman1@gmail.com<br>
            +212 625-778326
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Social links in a row
    st.markdown(
        """
        <div style='text-align: center'>
        <a href='https://www.linkedin.com/in/ayman-ismaili-ml'>LinkedIn</a> | 
        <a href='https://github.com/ISMAILI-AYMAN'>GitHub</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("---")

    # Professional summary
    st.header("Professional Summary")
    st.write(
        """
        Final-year engineering student at ENSAM-Meknès, specializing in AI and Data Science.
        Experienced in building ML pipelines, deploying models, and MLOps.
        Seeking a final-year internship (July–August 2025) in ML, MLOps, Data Engineering or Data Science.
        Open to remote/hybrid roles worldwide.
        """
    )

    st.write("---")

    # Projects
    st.header("Technical Projects")

    projects = [
        {
            "title": "CIFAR-10 Image Classifier Web Application",
            "tech": "PyTorch, Streamlit",
            "year": "2025",
            "description": [
                "Built and trained a convolutional neural network to classify CIFAR-10 images using PyTorch.",
                "Deployed the model as an interactive web app using Streamlit Cloud with real-time predictions.",
                "Integrated visualization: training loss curves, prediction samples, confusion matrix.",
            ],
            "live_link": "https://ejgtpj8eaiwnunyixmoja6.streamlit.app",
            "repo_link": "",
        },
        {
            "title": "Large-Scale Customer Segmentation with PySpark",
            "tech": "PySpark, MLflow",
            "year": "2025",
            "description": [
                "Processed 100,000+ e-commerce transaction records with PySpark for distributed computing.",
                "Engineered features and applied clustering with Spark MLlib.",
                "Used MLflow for experiment tracking and model comparison.",
            ],
            "live_link": "",
            "repo_link": "",
        },
        {
            "title": "Scholarship Assistant Chatbot",
            "tech": "LangChain, Streamlit",
            "year": "2024",
            "description": [
                "Developed an NLP-powered chatbot answering scholarship queries.",
                "Integrated LangChain with Streamlit UI for seamless interaction.",
                "Deployed online with responsive design and multilingual support.",
            ],
            "live_link": "",
            "repo_link": "",
        },
        {
            "title": "Flower Species Recognition System",
            "tech": "Keras, TensorFlow",
            "year": "2023",
            "description": [
                "Built CNN-based classifier for flower species recognition.",
                "Added training visualization and model evaluation metrics.",
            ],
            "live_link": "",
            "repo_link": "",
        },
    ]

    for project in projects:
        st.subheader(f"{project['title']} ({project['year']})")
        col1, col2 = st.columns([3, 2])
        with col1:
            st.markdown(f"**Tech stack:** {project['tech']}")
            for desc in project['description']:
                st.write(f"- {desc}")
        with col2:
            if project["live_link"]:
                st.markdown(f"[Live demo]({project['live_link']})")
            if project["repo_link"]:
                st.markdown(f"[GitHub Repo]({project['repo_link']})")
        st.write("---")

    # Resume section
    st.header("Resume")
    st.write("You can download my resume here:")
    st.markdown("[Resume PDF](./Ayman_Ismaili_Resume.pdf)")

    st.write("---")

    # Contact section in columns
    st.header("Contact")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Email:** ismailiayman1@gmail.com")
        st.write("**LinkedIn:**")
        st.markdown("[linkedin.com/in/ayman-ismaili-ml](https://www.linkedin.com/in/ayman-ismaili-ml)")
    with col2:
        st.write("**GitHub:**")
        st.markdown("[github.com/ISMAILI-AYMAN](https://github.com/ISMAILI-AYMAN)")
