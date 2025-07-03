import streamlit as st
from llama_cpp import Llama
import os
import json
from datetime import datetime

st.set_page_config(layout="wide", page_title="AI Resume Optimizer", page_icon="✨")

EXAMPLE_JOB_DESC = "..." 
EXAMPLE_RESUME = "..."
EXAMPLE_JOB_DESC = """
**Title: Cloud Engineer**
**Company: Awan Digital Nusantara**
**Location: Jakarta, Indonesia (Hybrid)**

**Job Description:**
We are seeking a skilled Cloud Engineer to join our growing infrastructure team. The ideal candidate will be responsible for designing, implementing, and maintaining our cloud infrastructure on AWS. You will play a key role in automating our operational processes and ensuring the reliability, scalability, and security of our platform.

**Key Responsibilities:**
- Design, deploy, and manage scalable and secure cloud environments on AWS (EC2, S3, RDS, VPC).
- Automate infrastructure provisioning using Infrastructure as Code (IaC) tools like Terraform.
- Develop and maintain CI/CD pipelines to streamline application deployment.

**Required Skills:**
- Proven experience as a Cloud Engineer or DevOps Engineer.
- Strong hands-on experience with AWS services.
- Proficiency in scripting with Python or Bash.
- Solid understanding of Infrastructure as Code (Terraform is a must).
"""

EXAMPLE_RESUME = """
**Name: Budi Santoso**
Email: budi.santoso@email.tech
Phone: +62 812 1234 5678
Location: Bandung, Indonesia
Education: Sarjana Teknik Informatika, Institut Teknologi Bandung (ITB)

**Experience:**
- Cloud Engineer - SolusiTek Prima (2022 - Present): Managed and scaled AWS infrastructure for various client projects. Automated server provisioning using Terraform scripts, reducing manual setup time by over 50%. Deployed containerized applications using Docker and managed clusters on Kubernetes.
- DevOps Engineer - Startup Maju (2020 - 2022): Responsible for server administration and writing automation scripts using Bash and Python.

**Skills:**
Cloud Platforms: AWS (EC2, S3, RDS, VPC, IAM, EKS), Google Cloud Platform (GCP)
Infrastructure as Code: Terraform, Ansible
Containerization: Docker, Kubernetes
Scripting: Python, Bash
"""

MODEL_PATH = "models/mistral-7b-instruct-v0.1.Q4_K_M.gguf"
HISTORY_FILE = "history.json"

@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        st.error(f"Model tidak ditemukan di path: {MODEL_PATH}")
        return None
    llm = Llama(model_path=MODEL_PATH, n_ctx=2048, n_threads=4, verbose=False)
    return llm

PROMPT_TEMPLATE = "..." 
PROMPT_TEMPLATE = """
### INSTRUCTION:
You are an expert HR professional and a technical resume writer. Your task is to rewrite a professional resume based on the provided "CANDIDATE DATA". You must tailor this resume to perfectly match the "JOB DESCRIPTION".

RULES:
1.  You MUST ONLY use the information provided in the "CANDIDATE DATA".
2.  DO NOT invent or hallucinate any facts, experiences, skills, or education.
3.  Highlight the skills and experiences from the "CANDIDATE DATA" that are most relevant to the "JOB DESCRIPTION".
4.  The output must be only the resume text, without any explanation.

### JOB DESCRIPTION:
{JOB_DESCRIPTION}

### CANDIDATE DATA:
{CANDIDATE_DATA}

### TAILORED RESUME:
"""

# --- Fungsi untuk Riwayat ---
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)

llm = load_model()

if 'history' not in st.session_state:
    st.session_state.history = load_history()
if 'latest_result' not in st.session_state:
    st.session_state.latest_result = ""

with st.sidebar:
    st.title("ℹ️ Tentang Aplikasi")
    st.info("Aplikasi ini menggunakan model bahasa Mistral-7B untuk menganalisis deskripsi pekerjaan dan menulis ulang resume Anda agar lebih menonjol dan relevan.")
    st.markdown("---")
    st.markdown("**Riwayat Optimasi**")
    if not st.session_state.history:
        st.write("Belum ada riwayat.")
    else:
        for i, entry in enumerate(reversed(st.session_state.history)):
            with st.expander(f"Riwayat #{len(st.session_state.history) - i} - {entry['timestamp']}"):
                st.text_area("Deskripsi Pekerjaan", value=entry['job_desc'], height=100, disabled=True, key=f"jd_{i}")
                st.text_area("Resume Hasil AI", value=entry['generated_resume'], height=100, disabled=True, key=f"gr_{i}")

st.title("✨ AI Resume Optimizer")
st.markdown("Ubah resume Anda menjadi alat pemasaran diri yang kuat dan spesifik untuk setiap lamaran!")

if llm:
    if st.button("Isi dengan Contoh (Cloud Engineer)"):
        st.session_state.jd_text = EXAMPLE_JOB_DESC
        st.session_state.resume_text = EXAMPLE_RESUME
        st.session_state.latest_result = "" 
        st.rerun()

    st.divider()
    st.header("Masukkan Data Anda", divider="rainbow")
    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            job_description_input = st.text_area("1️⃣ **Deskripsi Pekerjaan**", value=st.session_state.get('jd_text', ''), height=350)
    with col2:
        with st.container(border=True):
            original_resume_input = st.text_area("2️⃣ **Resume Asli Anda**", value=st.session_state.get('resume_text', ''), height=350)
    
    st.write("")
    
    generate_button = st.button("🚀 Optimalkan Resume Saya!", type="primary", use_container_width=True)

    if generate_button:
        if not job_description_input or not original_resume_input:
            st.warning("Mohon isi kedua kolom: Deskripsi Pekerjaan dan Resume Asli.")
        else:
            with st.spinner("⏳ AI sedang menganalisis dan menulis ulang resume Anda..."):
                prompt = PROMPT_TEMPLATE.replace("{JOB_DESCRIPTION}", job_description_input)
                prompt = prompt.replace("{CANDIDATE_DATA}", original_resume_input)
                output = llm(prompt, max_tokens=768, stop=["###"])
                result = output["choices"][0]["text"].strip()

            st.session_state.latest_result = result

            new_entry = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "job_desc": job_description_input,
                "original_resume": original_resume_input,
                "generated_resume": result
            }
            st.session_state.history.append(new_entry)
            save_history(st.session_state.history)

    if st.session_state.latest_result:
        st.balloons()
        st.success("🎉 Berhasil! Resume Anda telah dioptimalkan.")
        
        with st.expander("Lihat Hasil Resume", expanded=True):
            st.markdown(st.session_state.latest_result)
            st.download_button(
                label="⬇️ Unduh Resume (.txt)",
                data=st.session_state.latest_result,
                file_name="resume_optimized.txt",
                mime="text/plain"
            )
else:
    st.error("Gagal memuat model AI. Pastikan path model sudah benar.")