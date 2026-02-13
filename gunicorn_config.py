import multiprocessing

# Gunicorn configuration file

# Bind to localhost on port 5001
bind = "0.0.0.0:5001"

# Worker processes
# A common formula is 2 * num_cores + 1
workers = multiprocessing.cpu_count() * 2 + 1

# Worker type
worker_class = 'gthread'
threads = 4

# Logging
accesslog = "-"  # Log to stdout
errorlog = "-"   # Log to stderr
loglevel = "info"

# Timeout
timeout = 360  # Increased for long-running LLM queries
