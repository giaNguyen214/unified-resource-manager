```
project/
│
├── api/
│   └── server.py                # API layer (job submission endpoint)
│
├── core/
│   ├── parser.py                # Read & parse job.yaml
│   ├── manifest.py              # Generate Kubernetes YAML
│   └── submit.py                # kubectl apply controller
│
├── templates/
│   └── runtime.yaml.j2          # Universal Kubernetes template
│
├── jobs/
│   ├── job.yaml                 # Environment & runtime spec (user submits this file)
│   └── code/
│       └── main.py              # User code
│
└── README.md
```
