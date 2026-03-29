"""
Sync Data — Pushea snapshot diario a GitHub
=============================================
Corre automaticamente via Task Scheduler a las 16:50 ARG.
Genera snapshot de metricas y lo pushea para que el agente remoto lo lea.

Uso:
    python sync_data.py          # Generar snapshot + git push
    python sync_data.py --dry    # Solo generar snapshot, sin push
"""

import subprocess
import sys
from pathlib import Path

REPO_DIR = Path(__file__).parent


def run(cmd, check=True):
    """Ejecutar comando en el directorio del repo."""
    result = subprocess.run(
        cmd,
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
        shell=True,
    )
    if check and result.returncode != 0:
        print(f"  ERROR: {cmd}")
        print(f"  {result.stderr}")
        return False
    if result.stdout.strip():
        print(f"  {result.stdout.strip()}")
    return True


def main():
    dry_run = "--dry" in sys.argv

    print(f"\n  Polymarket Data Sync")
    print(f"  {'='*40}")

    # 1. Generar snapshot via daily_review.py
    print(f"\n  [1/4] Generando snapshot...")
    if not run("python daily_review.py"):
        print("  FALLO: No se pudo generar snapshot")
        return

    if dry_run:
        print(f"\n  Dry run — no se pushea nada.")
        return

    # 2. Git pull primero (por si el agente remoto hizo cambios)
    print(f"\n  [2/4] Pulling cambios remotos...")
    run("git pull --rebase origin main", check=False)

    # 3. Git add snapshots
    print(f"\n  [3/4] Staging snapshots...")
    run("git add data/snapshots/")
    run("git add data/daily_report.json", check=False)

    # Check if there's anything to commit
    result = subprocess.run(
        "git diff --cached --quiet",
        cwd=REPO_DIR,
        shell=True,
    )
    if result.returncode == 0:
        print(f"\n  Sin cambios nuevos para pushear.")
        return

    # 4. Commit + push
    print(f"\n  [4/4] Commit + push...")
    from datetime import datetime, timezone
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    run(f'git commit -m "data: daily snapshot {date}"')
    run("git push origin main")

    print(f"\n  Sync completado!")


if __name__ == "__main__":
    main()
