import requests
import streamlit as st


@st.cache_data(show_spinner=False)
def fetch_github_repos(
    username: str,
    exclude_repos: list[str] | None = None,
    min_stars: int = 0,
    max_repos: int = 4,
) -> list[dict]:
    """Lightweight helper to pull recent GitHub repos for the portfolio."""
    if not username:
        return []

    exclude_repos = exclude_repos or []
    url = f"https://api.github.com/users/{username}/repos?per_page=100&sort=updated"

    try:
        response = requests.get(
            url,
            headers={"Accept": "application/vnd.github+json"},
            timeout=10,
        )
        response.raise_for_status()
    except requests.RequestException:
        return []

    repos = []
    for repo in response.json():
        if repo.get("private") or repo.get("archived"):
            continue
        if repo.get("name") in exclude_repos:
            continue
        if repo.get("stargazers_count", 0) < min_stars:
            continue

        repos.append(
            {
                "title": repo.get("name", "GitHub Project"),
                "tech": [repo.get("language") or "Python"],
                "year": repo.get("created_at", "")[:4] or "2025",
                "description": [
                    repo.get("description") or "Open-source project hosted on GitHub."
                ],
                "live_link": repo.get("html_url", ""),
                "repo_link": repo.get("html_url", ""),
                "featured": False,
            }
        )

        if len(repos) >= max_repos:
            break

    return repos


def ensure_list(value):
    if isinstance(value, (list, tuple)):
        return list(value)
    if isinstance(value, str):
        return [value]
    return []


# Page config
st.set_page_config(page_title="Ayman Ismaili Portfolio", layout="centered")

# Header with columns for name and contact info
col1, col2 = st.columns([2, 3])
with col1:
    st.title("Ayman Ismaili")
    st.title("**Industrial Engineering, AI & Data Science**")
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

st.markdown(
    """
    <style>
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2d3748;
        margin: 2rem 0 1rem 0;
    }
    .project-card {
        border: 1px solid rgba(0,0,0,0.1);
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        background: rgba(255,255,255,0.85);
    }
    .project-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1a202c;
    }
    .project-year {
        color: #4a5568;
        font-size: 0.95rem;
    }
    .tech-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        margin-right: 0.4rem;
        margin-bottom: 0.4rem;
        font-size: 0.85rem;
        border-radius: 999px;
        background: #edf2f7;
        color: #2d3748;
    }
    .featured-badge {
        display: inline-block;
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        font-size: 0.75rem;
        padding: 0.2rem 0.6rem;
        border-radius: 999px;
        margin-left: 0.35rem;
    }
    .project-link {
        display: inline-block;
        margin-right: 1rem;
        color: #5a67d8;
        text-decoration: none;
        font-weight: 500;
    }
    .project-link:hover {
        text-decoration: underline;
    }
    .contact-card {
        border: 1px solid rgba(0,0,0,0.08);
        border-radius: 0.75rem;
        padding: 1.5rem;
        background: rgba(247,250,252,0.85);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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

manual_projects = [
    {
        "title": "CIFAR-10 Image Classifier Web Application",
        "tech": ["PyTorch", "Streamlit"],
        "year": "2025",
        "description": [
            "Built and trained a convolutional neural network to classify CIFAR-10 images using PyTorch.",
            "Deployed the model as an interactive web app using Streamlit Cloud with real-time predictions.",
            "Integrated visualization: training loss curves, prediction samples, confusion matrix.",
        ],
        "live_link": "https://ejgtpj8eaiwnunyixmoja6.streamlit.app",
        "repo_link": "",
        "featured": True,
    },
    {
        "title": "Large-Scale Customer Segmentation with PySpark",
        "tech": ["PySpark", "MLflow", "Spark MLlib", "Distributed Computing"],
        "year": "2025",
        "description": [
            "Processed 100,000+ e-commerce transaction records with PySpark for distributed computing.",
            "Engineered features and applied clustering with Spark MLlib.",
            "Used MLflow for experiment tracking and model comparison.",
        ],
        "live_link": "",
        "repo_link": "",
        "featured": True,
    },
    {
        "title": "Scholarship Assistant Chatbot",
        "tech": ["LangChain", "Streamlit", "NLP", "RAG"],
        "year": "2024",
        "description": [
            "Developed an NLP-powered chatbot answering scholarship queries.",
            "Integrated LangChain with Streamlit UI for seamless interaction.",
            "Deployed online with responsive design and multilingual support.",
        ],
        "live_link": "",
        "repo_link": "",
        "featured": False,
    },
    {
        "title": "Flower Species Recognition System",
        "tech": ["Keras", "TensorFlow", "CNN", "Computer Vision"],
        "year": "2023",
        "description": [
            "Built CNN-based classifier for flower species recognition.",
            "Added training visualization and model evaluation metrics.",
        ],
        "live_link": "",
        "repo_link": "",
        "featured": False,
    },
]

# Auto-fetch GitHub projects
github_username = "ISMAILI-AYMAN"
exclude_repos = ["foloi"]

github_projects = fetch_github_repos(
    username=github_username,
    exclude_repos=exclude_repos,
    min_stars=0,
)

all_projects = manual_projects + github_projects
all_projects.sort(
    key=lambda x: (
        not x.get("featured", False),
        x.get("year", "0"),
    ),
    reverse=True,
)

for project in all_projects:
    featured_badge = (
        "<span class='featured-badge'>Featured</span>"
        if project.get("featured", False)
        else ""
    )
    tech_stack = "".join(
        f"<span class='tech-badge'>{tech}</span>" for tech in ensure_list(project["tech"])
    )

    project_html = f"""
    <div class="project-card">
        <div class="project-title">{project['title']} {featured_badge}</div>
        <div class="project-year">{project.get('year', '')}</div>
        <div style="margin: 1rem 0;">
            {tech_stack}
        </div>
        <ul style="margin: 1rem 0; padding-left: 1.5rem; line-height: 1.8;">
    """

    for desc in project["description"]:
        project_html += f"<li>{desc}</li>"

    project_html += "</ul>"

    if project.get("live_link"):
        project_html += (
            f'<a href="{project["live_link"]}" target="_blank" class="project-link">Live Demo</a>'
        )
    if project.get("repo_link"):
        project_html += (
            f'<a href="{project["repo_link"]}" target="_blank" class="project-link">GitHub Repo</a>'
        )

    project_html += "</div>"

    st.markdown(project_html, unsafe_allow_html=True)

# Resume Section
st.markdown('<div class="section-header">Resume</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div style="text-align: center; padding: 1rem;">
        <p style="font-size: 1.1rem; margin-bottom: 1rem;">Download my resume to learn more about my experience and qualifications.</p>
        <a href="./Ayman_Ismaili_Resume.pdf" download class="project-link" style="display: inline-block; text-decoration: none;">Download Resume PDF</a>
    </div>
""",
    unsafe_allow_html=True,
)

st.write("")

# Contact Section
st.markdown('<div class="section-header">Contact</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="contact-card">
        <h3 style="margin-top: 0; color: #2d3748;">Let's Connect!</h3>
        <p style="font-size: 1.1rem; margin-bottom: 1.5rem;">Feel free to reach out via email or LinkedIn. I'm always open to discussing new opportunities and collaborations.</p>
        <div class="contact-item">
            <strong>Email:</strong> <a href="mailto:ismailiayman1@gmail.com" style="color: #667eea; text-decoration: none;">ismailiayman1@gmail.com</a>
        </div>
        <div class="contact-item">
            <strong>LinkedIn:</strong> <a href="https://www.linkedin.com/in/ayman-ismaili-ml" target="_blank" style="color: #667eea; text-decoration: none;">linkedin.com/in/ayman-ismaili-ml</a>
        </div>
        <div class="contact-item">
            <strong>GitHub:</strong> <a href="https://github.com/ISMAILI-AYMAN" target="_blank" style="color: #667eea; text-decoration: none;">github.com/ISMAILI-AYMAN</a>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# Footer
st.markdown(
    """
    <div style="text-align: center; padding: 2rem; color: #718096; margin-top: 3rem;">
        <p>&copy; 2025 Ayman Ismaili. Built with Streamlit.</p>
    </div>
""",
    unsafe_allow_html=True,
)
