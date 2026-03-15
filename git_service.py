import os
import shutil
import stat
from git import Repo


def handle_remove_readonly(func, path, exc_info):
    """Error handler for shutil.rmtree to remove read-only files (Windows fix)."""
    os.chmod(path, stat.S_IWRITE)
    func(path)


def clone_repository(github_url: str) -> str:
    # Basic extraction of the repository name from the URL
    repo_name = github_url.rstrip('/').split('/')[-1]
    if repo_name.endswith('.git'):
        repo_name = repo_name[:-4]

    # Define local path
    base_dir = "temp_repos"
    local_path = os.path.join(base_dir, repo_name)

    # If the directory already exists, delete it to ensure a fresh clone
    if os.path.exists(local_path):
        shutil.rmtree(local_path, onerror=handle_remove_readonly)

    # Ensure base directory exists (in case it's the first run)
    os.makedirs(base_dir, exist_ok=True)

    # Clone the repository
    Repo.clone_from(github_url, local_path)

    return local_path


def count_python_files(repo_path: str) -> dict:
    counts = {"python": 0, "javascript": 0, "typescript": 0}

    for root, _, files in os.walk(repo_path):
        # Optional: Skip .git directory to save time
        if '.git' in root:
            continue

        for file in files:
            if file.endswith('.py'):
                counts["python"] += 1
            elif file.endswith('.js') or file.endswith('.jsx'):
                counts["javascript"] += 1
            elif file.endswith('.ts') or file.endswith('.tsx'):
                counts["typescript"] += 1

    return counts
