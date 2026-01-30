import sys, subprocess, uuid
from core.parser import parse
from core.manifest import gen

job = parse(sys.argv[1])
job_id = job.get("job_id", str(uuid.uuid4())[:8])

manifest = gen(job, job_id)

out = f"job-{job_id}.yaml"
with open(out, "w") as f:
    f.write(manifest)



# namespace tự sinh theo job_id
namespace = f"job-{job_id}"

# tạo namespace nếu chưa tồn tại
if subprocess.call(
    ["kubectl", "get", "namespace", namespace],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
) != 0:
    subprocess.run(["kubectl", "create", "namespace", namespace], check=True)

subprocess.run(["kubectl", "apply", "-f", out, "-n", namespace], check=True)


