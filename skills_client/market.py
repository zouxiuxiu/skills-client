import shutil
import subprocess
from pathlib import Path
from typing import Optional

class SkillMarket:
    def __init__(self, repo_url: str, local_cache_dir: str = ".skill_market"):
        self.repo_url = repo_url
        self.cache_dir = Path(local_cache_dir)

    def _run_git(self, *args, cwd: Optional[Path] = None) -> str:
        cmd = ["git"] + list(args)
        result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Git command failed: {' '.join(cmd)}\n{result.stderr}")
        return result.stdout

    def sync(self):
        if self.cache_dir.exists():
            self._run_git("pull", cwd=self.cache_dir)
        else:
            self._run_git("clone", self.repo_url, str(self.cache_dir))

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