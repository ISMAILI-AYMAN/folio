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
                "year": repo.get("created_at", "")[:4] or "2026",
                "description": [
                    repo.get("description") or "Open-source project hosted on GitHub."
                ],
                "live_link": repo.get("homepage", ""),
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


# Page configuration
st.set_page_config(
    page_title="Ayman Ismaili Portfolio",
    page_icon="👨‍💻",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for optimized styling targeting modern Streamlit native structures
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Target Streamlit's main block containers directly */
    .stApp, .stMainBlockContainer {
        font-family: 'Inter', sans-serif;
        max-width: 1100px;
        margin: 0 auto;
    }
    
    /* Header styles */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 3rem;
        margin-top: -2rem;
    }
    
    .header-left { max-width: 65%; }
    .header-name { font-size: 3rem; font-weight: 700; color: #1a202c; margin-bottom: 0.25rem; }
    .header-title { font-size: 1.25rem; font-weight: 500; color: #4a5568; margin-bottom: 1rem; }
    .header-right { text-align: right; font-size: 0.95rem; color: #4a5568; line-height: 1.6; }
    
    .social-links { margin-top: 1rem; text-align: right; }
    .social-link {
        display: inline-block;
        margin-left: 0.75rem;
        padding: 0.5rem 1rem;
        background: #E2E8F0;
        border-radius: 8px;
        text-decoration: none;
        color: #2d3748;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    .social-link:hover { background: #CBD5E0; transform: translateY(-2px); }
    
    /* Section headers */
    .section-header {
        font-size: 2.25rem;
        font-weight: 700;
        color: #2d3748;
        margin: 3rem 0 1.5rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 4px solid #667eea;
    }
    
    /* Summary box */
    .summary-box {
        background: #ffffff;
        border: 1px solid #E2E8F0;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 3rem;
        line-height: 1.8;
        font-size: 1.1rem;
        color: #4a5568;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    }
    .summary-box ul { padding-left: 1.25rem; margin: 0; }
    .summary-box li { margin-bottom: 0.5rem; }
    .summary-box strong { color: #5a67d8; font-weight: 600; }
    
    /* Project cards */
    .project-card {
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        background: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    .project-card:hover { box-shadow: 0 10px 20px rgba(0,0,0,0.08); transform: translateY(-5px); }
    
    .project-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.75rem; }
    .project-title { font-size: 1.25rem; font-weight: 600; color: #1a202c; }
    .project-year { background: #E2E8F0; color: #4a5568; padding: 0.25rem 0.6rem; border-radius: 16px; font-size: 0.8rem; font-weight: 500; }
    
    .tech-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        font-size: 0.8rem;
        border-radius: 16px;
        background: #edf2f7;
        color: #4a5568;
        font-weight: 500;
    }
    .featured-badge {
        display: inline-block;
        background: #667eea;
        color: white;
        font-size: 0.7rem;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-left: 0.5rem;
    }
    
    .project-description { flex-grow: 1; margin: 1rem 0; padding-left: 1.25rem; line-height: 1.7; color: #4a5568; font-size: 0.95rem; }
    .project-description li { margin-bottom: 0.4rem; }
    .project-links { margin-top: auto; padding-top: 1rem; }
    
    .project-link {
        display: inline-block;
        margin-right: 0.75rem;
        padding: 0.5rem 1rem;
        background: #667eea;
        color: white !important;
        text-decoration: none;
        font-weight: 500;
        border-radius: 8px;
        transition: all 0.3s ease;
        font-size: 0.9rem;
    }
    .project-link:hover { background: #5a67d8; transform: translateY(-2px); }
    
    /* Contact card */
    .contact-card { background: #ffffff; border: 1px solid #E2E8F0; border-radius: 12px; padding: 2rem; box-shadow: 0 4px 20px rgba(0,0,0,0.05); }
    .contact-item { margin: 1rem 0; font-size: 1rem; line-height: 1.7; }
    
    /* Custom container for enclosing native elements cleanly */
    .custom-resume-card {
        text-align: center; 
        padding: 2rem; 
        background: white; 
        border-radius: 12px; 
        border: 1px solid #E2E8F0; 
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
    }

    /* Footer Layout */
    .footer { text-align: center; padding: 2rem; color: #718096; margin-top: 4rem; border-top: 1px solid #E2E8F0; }
    
    /* Hide Streamlit platform defaults */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    @media (max-width: 768px) {
        .header-container { flex-direction: column; }
        .header-left, .header-right { max-width: 100%; text-align: left; }
        .social-links { text-align: left; margin-top: 1.5rem; }
        .social-link { margin-left: 0; margin-right: 0.75rem; }
        .header-name { font-size: 2.5rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header Section
st.markdown(
    """
    <div class="header-container">
        <div class="header-left">
            <div class="header-name">Ayman Ismaili</div>
            <div class="header-title">Industrial Engineering, AI & Data Science</div>
        </div>
        <div class="header-right">
            <div>📍 Casablanca / Meknès, Morocco</div>
            <div>✉️ ismailiayman1@gmail.com</div>
            <div>📞 +212 625-778326</div>
            <div class="social-links">
                <a href="https://www.linkedin.com/in/ayman-ismaili-ml" target="_blank" class="social-link">LinkedIn</a>
                <a href="https://github.com/ISMAILI-AYMAN" target="_blank" class="social-link">GitHub</a>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Professional Summary
st.markdown('<div class="section-header">👨‍💼 Professional Summary</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="summary-box">
        <ul>
            <li><strong>AI & Data Science Engineer</strong> with a strong strategic foundation in Industrial Engineering from <strong>ENSAM-Meknès</strong>.</li>
            <li>Specialized in designing, scaling, and deploying end-to-end machine learning pipelines and secure, data-sovereign local GenAI architectures.</li>
            <li>Actively seeking full-time tracks (<strong>CDI</strong>) as an <strong>AI Engineer, Data Scientist, or MLOps Engineer</strong> starting <strong>September 2026</strong>.</li>
            <li>Open to localized engineering tracks within Morocco, France, or collaborative global hybrid/remote infrastructures. 🌍</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

# Projects Section
st.markdown('<div class="section-header">🚀 Technical Projects</div>', unsafe_allow_html=True)

# Note: Update 'repo_link' addresses directly to point to your specific public GitHub targets.
manual_projects = [
    {
        "title": "AutoCrashCheck: Automated Simulation Auditing Engine",
        "tech": ["Python", "Ollama", "Local LLM Agents", "Isolation Forest", "LS-DYNA"],
        "year": "2026",
        "description": [
            "Engineered a localized, data-sovereign LLM agent framework to orchestrate industrial simulation quality gates without external API lookups.",
            "Implemented an Isolation Forest anomaly detection pipeline to surface structural file corruptions and setup failures automatically.",
            "Built a high-performance regex and pattern parsing backend to map intricate structural engineering keyword components seamlessly."
        ],
        "live_link": "",
        "repo_link": "https://github.com/ISMAILI-AYMAN", 
        "featured": True,
    },
    {
        "title": "Distributed Customer Segmentation Engine",
        "tech": ["PySpark", "MLflow", "Spark MLlib", "Distributed Computing"],
        "year": "2025",
        "description": [
            "Architected a distributed data analytics pipeline utilizing PySpark to structure, clean, and process over 100,000 transaction traces.",
            "Deployed production-grade cluster models using Spark MLlib to extract granular, actionable user traits across high-dimensional features.",
            "Centralized experiment runs, artifact handling, and validation state versioning tracking protocols through MLflow integration."
        ],
        "live_link": "",
        "repo_link": "https://github.com/ISMAILI-AYMAN",
        "featured": True,
    },
    {
        "title": "Industrial Computer Vision & Deep Segmentation Pipeline",
        "tech": ["PyTorch", "UNet", "Docker", "MLOps", "Computer Vision"],
        "year": "2025",
        "description": [
            "Developed and tuned an optimized UNet segmentation network utilizing PyTorch for localized quality metrics and visual extraction.",
            "Containerized core microservices within a clean Docker framework to isolate compute environment variances during evaluation phases.",
            "Designed a highly performant evaluation harness to monitor continuous data shift and operational loss variances cleanly."
        ],
        "live_link": "",
        "repo_link": "https://github.com/ISMAILI-AYMAN",
        "featured": True,
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

featured_projects = [p for p in all_projects if p.get("featured")]
other_projects = [p for p in all_projects if not p.get("featured")]


def render_project(project):
    """Helper function to render a project card safely handling standard dictionary formats."""
    tech_stack = "".join(
        f"<span class='tech-badge'>{tech}</span>"
        for tech in ensure_list(project["tech"])
    )
    description_html = "".join(f"<li>{desc}</li>" for desc in project["description"])
    
    links_html = ""
    if project.get("live_link"):
        links_html += f'<a href="{project["live_link"]}" target="_blank" class="project-link">🔗 Live Demo</a>'
    if project.get("repo_link"):
        links_html += f'<a href="{project["repo_link"]}" target="_blank" class="project-link">📂 GitHub</a>'
        
    featured_badge = (
        "<span class='featured-badge'>Featured</span>" if project.get("featured") else ""
    )

    return f"""
        <div class="project-card">
            <div class="project-header">
                <div class="project-title">{project['title']} {featured_badge}</div>
                <span class="project-year">{project.get('year', '')}</span>
            </div>
            <div style="margin-bottom: 1rem;">{tech_stack}</div>
            <ul class="project-description">{description_html}</ul>
            <div class="project-links">{links_html}</div>
        </div>
    """


# Render featured projects
for project in featured_projects:
    st.markdown(render_project(project), unsafe_allow_html=True)

# Render secondary projects in standard grid rows
if other_projects:
    st.markdown(
        '<div class="section-header" style="margin-top: 3rem;">More Technical Repositories</div>',
        unsafe_allow_html=True,
    )
    num_cols = 2
    cols = st.columns(num_cols)
    for i, project in enumerate(other_projects):
        with cols[i % num_cols]:
            st.markdown(render_project(project), unsafe_allow_html=True)

# Resume Section
st.markdown('<div class="section-header">📄 Resume Evaluation</div>', unsafe_allow_html=True)

# Wrapping descriptive text container card
st.markdown(
    """
    <div class="custom-resume-card">
        <p style="font-size: 1.1rem; margin-bottom: 0rem; color: #4a5568;">
            Download my latest ATS-optimized resume for offline evaluation and full engineering track details.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Executing the download logic directly below to keep UI layout unified inside container card boundaries
try:
    with open("AI_AYMAN_ISMAILI.pdf", "rb") as pdf_file:
        pdf_bytes = pdf_file.read()

    _, col2, _ = st.columns([3, 2, 3])
    with col2:
        st.download_button(
            label="📥 Download Resume (PDF)",
            data=pdf_bytes,
            file_name="AI_AYMAN_ISMAILI.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
except FileNotFoundError:
    st.warning("Resume pipeline offline. Please request documentation directly via email.")

# Contact Section
st.markdown('<div class="section-header">📬 Engineering Connect</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="contact-card">
        <h3 style="margin-top: 0; color: #2d3748; font-size: 1.5rem; margin-bottom: 1rem;">Let's Coordinate!</h3>
        <p style="font-size: 1rem; margin-bottom: 1.5rem; color: #4a5568; line-height: 1.7;">
            I am available for formal corporate screening patterns, technical interview challenges, and architecture reviews for upcoming 2026 CDI engineering tracks.
        </p>
        <div class="contact-item">
            <strong>📧 Corporate Correspondence:</strong> 
            <a href="mailto:ismailiayman1@gmail.com" style="color: #667eea; text-decoration: none; font-weight: 500;">ismailiayman1@gmail.com</a>
        </div>
        <div class="contact-item">
            <strong>💼 Professional Network:</strong> 
            <a href="https://www.linkedin.com/in/ayman-ismaili-ml" target="_blank" style="color: #667eea; text-decoration: none; font-weight: 500;">linkedin.com/in/ayman-ismaili-ml</a>
        </div>
        <div class="contact-item">
            <strong>🐙 Version Control:</strong> 
            <a href="https://github.com/ISMAILI-AYMAN" target="_blank" style="color: #667eea; text-decoration: none; font-weight: 500;">github.com/ISMAILI-AYMAN</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Footer
st.markdown(
    """
    <div class="footer">
        <p style="margin: 0; font-size: 0.9rem;">&copy; 2026 Ayman Ismaili. Maintained with technical resilience using Streamlit.</p>
    </div>
    """,
    unsafe_allow_html=True,
)