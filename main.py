from llama_cpp import Llama
import os

# Konfigurasi
MODEL_PATH = "models\mistral-7b-instruct-v0.1.Q4_K_M.gguf"
CTX_SIZE = 2048
MAX_TOKENS = 512
THREADS = 4

# Cek apakah model ada
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"⚠️ Model tidak ditemukan di: {MODEL_PATH}")

# Load model
print("⏳ Memuat model...")
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=CTX_SIZE,
    n_threads=THREADS
)
print("✅ Model siap digunakan.")

# Load deskripsi pekerjaan
with open("job.txt", "r", encoding="utf-8") as f:
    job_description = f.read().strip()

# Load prompt template
with open("prompt_template.txt", "r", encoding="utf-8") as f:
    prompt_template = f.read()

# Ganti placeholder di prompt
prompt = prompt_template.replace("{JOB_DESCRIPTION}", job_description)

# Cek panjang prompt
if len(prompt) > CTX_SIZE * 4:
    print("⚠️ Prompt terlalu panjang, akan dipotong.")
    prompt = prompt[:CTX_SIZE * 4]

# Tampilkan prompt (untuk debugging)
print("\n📝 Prompt yang dikirim ke model:")
print("=" * 40)
print(prompt[:1000])  # tampilkan 1000 karakter pertama
print("=" * 40)

# Jalankan prompt
print("🚀 Menghasilkan resume dari model...")
output = llm(prompt, max_tokens=MAX_TOKENS)

# Deteksi format output
if isinstance(output, dict):
    print("📦 Output model bertipe dict.")
    result = output["choices"][0]["text"]
elif isinstance(output, str):
    print("📦 Output model langsung bertipe string.")
    result = output
else:
    print("❌ Format output tidak dikenali.")
    result = ""

# Cek hasil kosong
if not result.strip():
    print("⚠️ Model tidak menghasilkan output.")
else:
    print("✅ Output berhasil didapat.")

# Simpan ke file
with open("resume.txt", "w", encoding="utf-8") as f:
    f.write(result.strip())

print("📄 Resume disimpan di 'resume.txt'.")
