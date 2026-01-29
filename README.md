├ api/ # API layer (job submission endpoint)
│ └ server.py
│
├ core/ # Core execution pipeline
│ ├ parser.py # Read & parse job.yaml
│ ├ manifest.py # Generate Kubernetes YAML
│ └ submit.py # kubectl apply controller
│
├ templates/ # Kubernetes template
│ └ runtime.yaml.j2 # Universal template
│
├ jobs/ # User input
│ ├ job.yaml # Environment & runtime spec (user write this file and submit to the system )
│ └ code/ # User code file
| └ main.py
