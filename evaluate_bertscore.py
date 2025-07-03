# filename: evaluate_bertscore.py
from bert_score import score

# --- Tentukan file yang akan dibandingkan ---
CANDIDATE_FILE = "resume_generated.txt"
REFERENCE_FILE = "match_resume_grouped_txt\Cloud_Engineer\match_25_jd.txt"

print(f"Membaca file kandidat: {CANDIDATE_FILE}")
print(f"Membaca file referensi: {REFERENCE_FILE}")

# --- Baca isi kedua file ---
try:
    with open(CANDIDATE_FILE, "r", encoding="utf-8") as f:
        candidate_text = f.read()
    
    with open(REFERENCE_FILE, "r", encoding="utf-8") as f:
        reference_text = f.read()
except FileNotFoundError as e:
    print(f"Error: File tidak ditemukan. {e}")
    exit()

# BERTScore mengharapkan input berupa list of strings, jadi kita bungkus teks kita dalam list
candidates = [candidate_text]
references = [reference_text]

print("\nMenghitung BERTScore... (Proses ini mungkin perlu waktu sejenak)")

# --- Hitung skornya ---
# 'lang="en"' penting karena teks kita berbahasa Inggris
# 'verbose=True' akan menampilkan progress bar
(P, R, F1) = score(candidates, references, lang="en", verbose=True)

print("\n--- Hasil Evaluasi BERTScore ---")
# F1 score adalah metrik utama yang paling sering dilihat
print(f"Skor F1: {F1.mean():.4f}") 
print(f"Precision: {P.mean():.4f}")
print(f"Recall: {R.mean():.4f}")

print("\n--- Interpretasi ---")
print(f"Skor F1 (rata-rata): {F1.mean():.4f}")
print("Ini adalah skor keseimbangan antara Precision dan Recall. Semakin tinggi semakin baik.")
print("\nPrecision: Seberapa relevan kata-kata di resume dengan deskripsi pekerjaan?")
print("Recall: Seberapa banyak konsep dari deskripsi pekerjaan yang berhasil 'ditangkap' oleh resume?")