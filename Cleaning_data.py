# filename: extract_to_txt.py
import json
import re
import os

# --- Konfigurasi ---
# Folder sumber yang berisi data JSON asli
SOURCE_ROOT_DIR = 'match_resume_grouped'
# Folder tujuan untuk menyimpan hasil .txt
DEST_ROOT_DIR = 'match_resume_grouped_txt'

def clean_text(text):
    """
    Fungsi untuk membersihkan sebuah string teks.
    """
    if not isinstance(text, str):
        return text
    text = text.replace('**', '')
    text = text.replace('\n', ' ').replace('\t', ' ')
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

# --- Proses Utama ---
if not os.path.exists(SOURCE_ROOT_DIR):
    print(f"Error: Folder sumber '{SOURCE_ROOT_DIR}' tidak ditemukan.")
else:
    print(f"Memulai proses ekstrak dan cleaning dari direktori: {SOURCE_ROOT_DIR}")
    
    # os.walk akan menjelajahi setiap folder dan subfolder
    for root, dirs, files in os.walk(SOURCE_ROOT_DIR):
        # Membuat struktur folder yang sama di direktori tujuan
        dest_dir = root.replace(SOURCE_ROOT_DIR, DEST_ROOT_DIR, 1)
        os.makedirs(dest_dir, exist_ok=True)
        
        print(f"\nMemproses folder: {root}")

        # Loop melalui setiap file di dalam folder
        for filename in files:
            if filename.endswith('.json'):
                source_path = os.path.join(root, filename)
                
                try:
                    # Buka dan baca file JSON asli
                    with open(source_path, 'r', encoding='utf-8') as f_in:
                        record = json.load(f_in)

                    # Ekstrak dan bersihkan teks dari JSON
                    cleaned_jd = clean_text(record['input']['job_description'])
                    cleaned_resume = clean_text(record['input']['resume'])
                    
                    # Tentukan nama dasar file tanpa ekstensi .json
                    base_filename = os.path.splitext(filename)[0]
                    
                    # Tentukan nama dan path untuk file output .txt
                    jd_txt_path = os.path.join(dest_dir, f"{base_filename}_jd.txt")
                    resume_txt_path = os.path.join(dest_dir, f"{base_filename}_resume.txt")
                    
                    # Tulis teks yang sudah bersih ke file .txt masing-masing
                    with open(jd_txt_path, 'w', encoding='utf-8') as f_jd:
                        f_jd.write(cleaned_jd)
                    
                    with open(resume_txt_path, 'w', encoding='utf-8') as f_resume:
                        f_resume.write(cleaned_resume)
                        
                    print(f"  - Berhasil mengekstrak {filename} -> {base_filename}_jd.txt & {base_filename}_resume.txt")

                except Exception as e:
                    print(f"  - Gagal memproses file {filename}: {e}")

    print(f"\n\nProses selesai. Semua file .txt telah disimpan di direktori '{DEST_ROOT_DIR}'.")