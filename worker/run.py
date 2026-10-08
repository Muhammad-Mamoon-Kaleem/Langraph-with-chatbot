"""
RQ worker entry point.

Run from project root:
    python -m worker.run

Windows requires SimpleWorker (no os.fork).
Linux/macOS use the default Worker with fork.
"""

import subprocess
import sys

from chatbot.config import REDIS_QUEUE_NAME, REDIS_URL

WORKER_CLASS = (
    "rq.worker.SimpleWorker"
    if sys.platform == "win32"
    else "rq.worker.Worker"
)


def main() -> None:
    print(f"Starting RQ worker on queue '{REDIS_QUEUE_NAME}' ({WORKER_CLASS})")
    subprocess.run(
        [
            sys.executable,
            "-m",
            "rq.cli",
            "worker",
            REDIS_QUEUE_NAME,
            "--url",
            REDIS_URL,
            "--worker-class",
            WORKER_CLASS,
        ],
        check=True,
    )


if __name__ == "__main__":
    main()
