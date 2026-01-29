import sys, subprocess, uuid
from core.parser import parse
from core.manifest import gen

job = parse(sys.argv[1])
job_id = job.get("job_id", str(uuid.uuid4())[:8])

manifest = gen(job, job_id)

out = f"job-{job_id}.yaml"
with open(out, "w") as f:
    f.write(manifest)

subprocess.run(["kubectl", "apply", "-f", out], check=True)
