from jinja2 import Template
import os

COMPUTE_IMAGES = [
    "tensorflow",
    "pytorch",
    "xgboost",
    "openmpi",
    "mpioperator"
]

SERVICE_IMAGES = [
    "kafka",
    "redis",
    "postgres",
    "hadoop",
    "spark",
    "flink"
]

def is_compute(image: str):
    img = image.lower()
    return any(k in img for k in COMPUTE_IMAGES)

def is_service(image: str):
    img = image.lower()
    return any(k in img for k in SERVICE_IMAGES)

import re

def k8s_name(image: str):
    name = image.lower()
    name = name.replace("/", "-").replace(":", "-")
    name = re.sub(r"[^a-z0-9-]", "-", name)   # thay mọi ký tự không hợp lệ (., _, +, ...)
    name = re.sub(r"-+", "-", name)           # gộp nhiều dấu -
    name = name.strip("-")                    # bỏ - đầu/cuối
    return name

def gen(job, job_id):
    t = open("templates/runtime.yaml.j2").read()
    template = Template(t, trim_blocks=True, lstrip_blocks=True)


    yamls = []
    has_code = os.path.exists("jobs/code")

    os_pkgs = []
    py_pkgs = []
    sources = []
    
    namespace = f"job-{job_id}"

    for item in job.get("install", []):
        if item["type"] == "os_pkg":
            os_pkgs = item.get("packages", [])
        if item["type"] == "lang_pkg" and item.get("lang") == "python":
            py_pkgs = item.get("packages", [])
        if item["type"] == "source":
            sources.append(item)

    for item in job.get("install", []):
        if item.get("type") != "container":
            continue

        kind = item.get("kind", "Pod")
        image = item["image"]

        compute = is_compute(image)
        service = is_service(image)

        data = {
            "kind": kind,
            "job_id": job_id,
            "namespace": namespace,
            "name": k8s_name(image),
            "image": image,
            "resources": job["resources"],
            "entrypoint": job.get("entrypoint", "main.py"),
            "has_code": has_code,
            "compute": compute,
            "service": service,
            "os_pkgs": os_pkgs,
            "py_pkgs": py_pkgs,
            "sources": sources
        }

        y = template.render(**data)
        yamls.append(y)

    return "\n---\n".join(yamls)
