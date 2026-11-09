#!/usr/bin/env python3
"""
push_to_github.py
Bu betik, yerel Git deposunu oluşturduğunuz GitHub deposuna push eder.
Kullanım:
    python push_to_github.py https://github.com/mserman90/suhaber.git [GITHUB_TOKEN]
"""

import sys
import subprocess
from pathlib import Path

def push_with_cli(remote_url: str) -> bool:
    """Fallback using local git CLI."""
    try:
        cmd = ["git", "push", remote_url, "refs/heads/main"]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            print("[+] Git CLI ile başarıyla GitHub'a push edildi!")
            return True
        else:
            print(f"[-] Git CLI push hatası: {res.stderr.strip()}")
            return False
    except Exception as e:
        print(f"[-] Git CLI çalıştırılamadı: {e}")
        return False

def push_with_dulwich(repo_dir: Path, remote_url: str) -> bool:
    """Push using dulwich library if installed."""
    try:
        from dulwich.repo import Repo
        from dulwich.porcelain import push
        repo = Repo(str(repo_dir))
        push(repo, remote_url, refspecs=b"refs/heads/main")
        print("[+] Dulwich ile başarıyla GitHub'a push edildi!")
        return True
    except ImportError:
        return False
    except Exception as e:
        print(f"[-] Dulwich hatası: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Kullanım: python push_to_github.py <REPO_URL> [GITHUB_TOKEN]")
        print("Örnek:   python push_to_github.py https://github.com/mserman90/suhaber.git")
        return

    remote_url = sys.argv[1].strip()
    token = sys.argv[2].strip() if len(sys.argv) > 2 else None

    # URL içine token enjekte et (gerekirse)
    if token and "github.com" in remote_url and "@" not in remote_url:
        remote_url = remote_url.replace("https://", f"https://{token}@")

    repo_dir = Path(__file__).resolve().parent

    print(f"[*] Depo push ediliyor: {remote_url}")
    
    # Try dulwich first, fallback to CLI
    if not push_with_dulwich(repo_dir, remote_url):
        if not push_with_cli(remote_url):
            print("\nİpucu: Eğer kurum güvenlik duvarınız GitHub bağlantılarını engelliyorsa,")
            print("bu klasörü VS Code veya GitHub web arayüzü ile doğrudan yükleyebilirsiniz.")

if __name__ == "__main__":
    main()
