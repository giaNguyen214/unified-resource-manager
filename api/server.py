from fastapi import FastAPI, UploadFile
import subprocess, os
import sys

app = FastAPI()

@app.post("/submit")
async def submit(yaml: UploadFile, code: UploadFile = None):
    os.makedirs("jobs", exist_ok=True)

    yaml_path = f"jobs/{yaml.filename}"
    with open(yaml_path, "wb") as f:
        f.write(await yaml.read())

    if code:
        code_path = "jobs/code.py"
        with open(code_path, "wb") as f:
            f.write(await code.read())

    # subprocess.run(["python", "core/submit.py", yaml_path], check=True)
    subprocess.run([sys.executable, "-m", "core.submit", yaml_path], check=True)
    
    return {"status": "submitted"}
