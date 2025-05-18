#!/usr/bin/env python3
import itertools
import random

# 1) Define expanded lists of actions, subjects, and qualifiers
actions = [
    "How to", "Best way to", "Quick tutorial on", "Guide to",
    "Tips for", "Beginner's guide to", "Advanced", "Troubleshooting",
    "Step-by-step", "Complete guide to", "Easy way to", "Professional",
    "Ultimate guide to", "Mastering", "Learn", "Understand",
    "Fix", "Solve", "Optimize", "Debug",
    "Implement", "Create", "Build", "Develop",
    "Install", "Configure", "Set up", "Deploy",
    "Migrate", "Convert", "Automate", "Secure",
    "Test", "Validate", "Monitor", "Scale",
    "Troubleshoot", "Resolve", "Avoid", "Prevent",
    "Compare", "Difference between", "Pros and cons of",
    "When to use", "Alternatives to", "Examples of""How to", "Best way to", "Quick tutorial on", "Guide to",
    "Tips for", "Beginner's guide to", "Advanced", "Troubleshooting",
    
    # Skill levels
    "Novice", "Intermediate", "Expert", "Professional",
    
    # Action verbs
    "Implement", "Create", "Build", "Develop", "Design",
    "Install", "Configure", "Set up", "Deploy", "Launch",
    "Migrate", "Convert", "Automate", "Secure", "Harden",
    "Test", "Validate", "Monitor", "Scale", "Parallelize",
    
    # Problem-solving
    "Fix", "Solve", "Optimize", "Debug", "Hack",
    "Troubleshoot", "Resolve", "Avoid", "Prevent", "Bypass",
    
    # Comparative
    "Compare", "Difference between", "Pros and cons of", "Showdown",
    "When to use", "Alternatives to", "Examples of", "Case study on",
    
    # Quality descriptors
    "Comprehensive", "Practical", "Effective", "Modern",
    "Essential", "Hidden", "Secret", "Powerful",
    "Underrated", "Overlooked", "Cutting-edge", "Next-gen",
    
    # Performance
    "Production-grade", "Enterprise", "Scalable", "Robust",
    "Minimal", "Lightweight", "Blazing fast", "High-performance",
    
    # AI-focused
    "AI-powered", "ML-enhanced", "Automated", "Smart",
    "LLM-assisted", "Neural", "Generative", "Transformer-based"
]

subjects = [
    # Python Core
    "list comprehension in Python", "merging dictionaries in Python",
    "async/await in Python", "decorators in Python",
    "virtualenv vs conda", "logging best practices in Python",
    "type hints in Python", "pytest fixtures",
    "lambda functions in Python", "zipfile module example",
    "CSV to JSON conversion in Python", "XML parsing in Python",
    "priority queues with heapq", "dataclasses vs namedtuple",
    "context managers in Python", "memory profiling in Python",
    "performance optimization tips", "advanced f-strings usage",
    "itertools examples", "enum module tutorial",
    "socket programming in Python", "subprocess.run examples",
    "file monitoring with watchdog", "dependency management with Poetry",
    "code formatting with Black", "import sorting with isort",
    "static typing with mypy", "SQLite3 CRUD in Python",
    
    # Web Development
    "Flask JWT authentication", "Django REST framework tutorial",
    "FastAPI SQLModel", "Flask SQLAlchemy session management",
    "Django custom user model", "Django allauth social login",
    "Django channels websocket", "Flask Celery background tasks",
    "Django middleware", "Django signals",
    "Django ORM optimization", "Django template inheritance",
    "Flask Blueprint large app", "Django pytest fixtures",
    "Django caching strategies", "Flask rate limiting",
    "Django deployment Nginx Gunicorn", "Flask Docker compose",
    "Django GitHub Actions CI/CD", "Django PostgreSQL full-text search",
    "Django GraphQL graphene", "Flask Swagger documentation",
    "Django admin customization", "Django bulk_create",
    
    # Data Science
    "Pandas DataFrame filtering", "NumPy array operations",
    "Matplotlib subplots", "Seaborn violin plot",
    "Plotly interactive chart", "Bokeh dashboard",
    "scikit-learn SVM", "XGBoost tutorial",
    "TensorFlow GPU setup", "PyTorch RNN",
    "Keras callback usage", "OpenCV video processing",
    "Pillow image manipulation", "Pandas pivot tables",
    "NumPy broadcasting", "Seaborn heatmap",
    "Plotly Dash app", "Dask parallel processing",
    
    # JavaScript/Web
    "React useState useEffect", "Vue 3 composition API",
    "Angular dependency injection", "Next.js getServerSideProps",
    "Svelte store", "React Router v6",
    "Vuex state management", "Redux toolkit slice",
    "React context API", "Vue Pinia setup",
    "Angular RxJS observable", "React custom hooks",
    "Vue teleport", "React performance optimization",
    
    # Mobile
    "Android Compose navigation", "Kotlin coroutines Room DB",
    "Flutter Riverpod state", "React Native FlatList",
    "SwiftUI MVVM", "Jetpack Compose themes",
    "Android WorkManager", "Flutter Firebase auth",
    
    # DevOps/Cloud
    "AWS Lambda Python", "Azure Functions Python",
    "Docker compose Redis", "Kubernetes Helm chart",
    "Terraform AWS EC2", "GitHub Actions CI/CD",
    "Nginx reverse proxy", "Let's Encrypt certbot",
    
    # Databases
    "PostgreSQL indexing", "MongoDB aggregation pipeline",
    "Redis caching strategy", "SQLite performance tuning",
    "MySQL backup and restore", "Firebase Realtime Database rules",
    
    # Security
    "JWT token refresh", "OAuth2 implementation",
    "bcrypt password hashing", "CSRF protection Django",
    "SSL/TLS certificate setup", "penetration testing basics",
    
    # AI/ML
    "TensorFlow object detection", "PyTorch GAN",
    "Hugging Face transformers", "spaCy NER training",
    "YOLOv5 custom dataset", "Stable Diffusion Python",
    
    # General Programming
    "clean code principles", "design patterns implementation",
    "algorithm complexity analysis", "data structures comparison",
    "unit testing best practices", "CI/CD pipeline setup",
    "microservices architecture", "REST API design",
    "GraphQL vs REST", "WebSocket implementation",
    
    # Tools
    "VSCode shortcuts", "IntelliJ productivity tips",
    "Git rebase workflow", "Docker best practices",
    "Postman API testing", "Jupyter Notebook tricks",
    
    # OS/System
    "Linux command line tricks", "Windows PowerShell scripting",
    "Mac terminal customization", "SSH key management",
    "cron job scheduling", "systemd service creation","list comprehension in Python", "merging dictionaries in Python",
    "async/await in Python", "decorators in Python",
    "virtualenv vs conda vs pipenv", "logging best practices in Python",
    "type hints in Python", "pytest fixtures and parametrization",
    
    ## JavaScript/TypeScript
    "async/await in JavaScript", "TypeScript generics",
    "ES6 modules", "Node.js event loop",
    
    ## Java/Kotlin
    "Java streams API", "Kotlin coroutines",
    
    ## Rust/Go
    "Rust ownership", "Go goroutines",
    
    ## Web Development
    "React hooks", "Vue composition API",
    "Angular signals", "Svelte stores",
    
    # ========== AI/ML ==========
    ## LLMs
    "LLM prompt engineering", "Fine-tuning GPT-4",
    "RAG implementation", "LangChain agents",
    
    ## Computer Vision
    "YOLOv9 object detection", "Stable Diffusion XL",
    
    ## Traditional ML
    "XGBoost hyperparameter tuning", "PyTorch Lightning",
    
    # ========== DevOps ==========
    "Kubernetes operators", "Terraform modules",
    "GitHub Actions workflows", "ArgoCD rollouts",
    
    # ========== Databases ==========
    "PostgreSQL partitioning", "MongoDB transactions",
    
    # ========== Mobile ==========
    "Jetpack Compose animations", "SwiftUI navigation",
    
    # ========== Emerging Tech ==========
    "Quantum algorithms", "Blockchain oracles"
]

qualifiers = [
    "", "for beginners", "step by step", "with examples",
    "best practices", "in 10 minutes", "2025 edition",
    "complete tutorial", "from scratch", "the right way",
    "in depth", "with Python 3.12", "for production",
    "for data science", "for web development", "for mobile apps",
    "with Docker", "on AWS", "on Ubuntu", "on Windows",
    "on Mac", "in Visual Studio Code", "using ChatGPT",
    "with performance tips", "with security considerations",
    "for large datasets", "for high traffic applications",
    "with TypeScript", "with React", "with Vue.js",
    "with Django", "with Flask", "with FastAPI",
    "with TensorFlow", "with PyTorch", "with Pandas",
    "with NumPy", "with SQLAlchemy", "with Celery",
    "for interviews", "for competitive programming",
    "with cheat sheet", "with benchmarks", "with alternatives","for beginners", "for intermediates", "for experts",
    
    # Time constraints
    "in 5 minutes", "in 10 minutes", "in 30 minutes",
    
    # Environments
    "on Windows", "on Mac", "on Linux",
    "in Docker", "in Kubernetes", "on AWS",
    
    # Tools
    "using VSCode", "with Copilot", "in Jupyter",
    
    # Years
    "in 2024", "in 2025", "future-proof",
    
    # Special cases
    "with examples", "step by step", "the right way"
]

# 2) Generate a set of combinations
queries = set()
for action, subj, qual in itertools.product(actions, subjects, qualifiers):
    q = f"{action} {subj}".strip()
    if qual:
        q += f" {qual}"
    queries.add(q)

# 3) Randomize and pick the first N (e.g. 1000)
N = 1000
new_queries = random.sample(sorted(queries), min(N, len(queries)))

# 4) Append to queries.txt, skipping duplicates
existing = set()
try:
    with open("queries.txt", "r", encoding="utf-8") as f:
        existing = set(line.strip() for line in f)
except FileNotFoundError:
    pass

with open("queries.txt", "a", encoding="utf-8") as f:
    added_count = 0
    for q in new_queries:
        if q not in existing:
            f.write(q + "\n")
            added_count += 1

print(f"Added {added_count} new queries (total possible: {len(queries)}).")