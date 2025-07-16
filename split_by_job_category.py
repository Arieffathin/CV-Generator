import os
import json
import shutil

# Folder asal berisi file JSON
SOURCE_FOLDER = r"D:\Project_Dira\resume-score-details\match_resume"
# Folder tujuan hasil kelompok per kategori
DEST_ROOT = "match_resume_grouped"

# Kategori berdasarkan kata kunci dalam job_description
topic_keywords = {
    "Cloud Engineer": ["cloud", "aws", "infrastructure", "lambda", "vpc", "s3"],
    "Software Engineer": ["software", "developer", "coding", "application", "programming"],
    "Data Analyst": ["data", "analysis", "analytics", "visualization", "insight", "sql", "power bi"],
    "Product Manager": ["product", "market", "strategy", "roadmap", "stakeholder"],
    "Security Engineer": ["security", "compliance", "risk", "penetration", "vulnerability"]
}

# Buat folder tujuan utama jika belum ada
os.makedirs(DEST_ROOT, exist_ok=True)

# Loop semua file di folder asal
for fname in os.listdir(SOURCE_FOLDER):
    if not fname.endswith(".json"):
        continue

    file_path = os.path.join(SOURCE_FOLDER, fname)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            desc = data.get("input", {}).get("job_description", "").lower()

            matched = False
            for label, keywords in topic_keywords.items():
                if any(keyword in desc for keyword in keywords):
                    target_folder = os.path.join(DEST_ROOT, label)
                    os.makedirs(target_folder, exist_ok=True)
                    shutil.copy2(file_path, os.path.join(target_folder, fname))
                    matched = True
                    break

            if not matched:
                # Jika tidak cocok ke kategori manapun, masuk ke 'Other'
                other_folder = os.path.join(DEST_ROOT, "Other")
                os.makedirs(other_folder, exist_ok=True)
                shutil.copy2(file_path, os.path.join(other_folder, fname))

    except Exception as e:
        print(f"❌ Error processing {fname}: {e}")
