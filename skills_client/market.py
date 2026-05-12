import git
import shutil
from pathlib import Path
from typing import Optional

class SkillMarket:
    def __init__(self, repo_url: str, local_cache_dir: str = ".skill_market"):
        self.repo_url = repo_url
        self.cache_dir = Path(local_cache_dir)

    def sync(self):
        if self.cache_dir.exists():
            repo = git.Repo(self.cache_dir)
            repo.remotes.origin.pull()
        else:
            git.Repo.clone_from(self.repo_url, self.cache_dir)

    def install(self, skill_name: str, target_dir: str = "skills") -> bool:
        self.sync()
        source = self.cache_dir / skill_name
        if not source.exists() or not source.is_dir():
            return False
        dest = Path(target_dir) / skill_name
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(source, dest)
        return True