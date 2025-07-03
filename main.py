from llama_cpp import Llama
import os

MODEL_PATH = "models/mistral-7b-instruct-v0.1.Q4_K_M.gguf"
CTX_SIZE = 2048
MAX_TOKENS = 512 
THREADS = 4


JOB_DESC_FILE = "target_job.txt"
CANDIDATE_DATA_FILE = "myresume.txt"
PROMPT_TEMPLATE_FILE = "prompt_template.txt" 
OUTPUT_FILE = "resume_generated.txt" 

for f in [MODEL_PATH, JOB_DESC_FILE, CANDIDATE_DATA_FILE, PROMPT_TEMPLATE_FILE]:
    if not os.path.exists(f):
        raise FileNotFoundError(f"⚠️ File tidak ditemukan di: {f}")

print("⏳ Memuat model...")
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=CTX_SIZE,
    n_threads=THREADS,
    verbose=False 
)
print("✅ Model siap digunakan.")

print("📄 Membaca data input...")
with open(JOB_DESC_FILE, "r", encoding="utf-8") as f:
    job_description = f.read().strip()
with open(CANDIDATE_DATA_FILE, "r", encoding="utf-8") as f:
    candidate_data = f.read().strip()
with open(PROMPT_TEMPLATE_FILE, "r", encoding="utf-8") as f:
    prompt_template = f.read()

print("📝 Menyusun prompt...")
prompt = prompt_template.replace("{JOB_DESCRIPTION}", job_description)
prompt = prompt.replace("{CANDIDATE_DATA}", candidate_data)

print("🚀 Menghasilkan resume dari model...")
output = llm(prompt, max_tokens=MAX_TOKENS, stop=["###"])

result = output["choices"][0]["text"].strip()

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(result)
print(f"📄 Resume berhasil disimpan di '{OUTPUT_FILE}'.")
