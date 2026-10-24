"""
Master Build Script - Orchestrates all build tasks
Run this locally: python scripts/build.py
Generates assets, verifies README, prepares deployment
"""

import sys
import subprocess
from pathlib import Path


def run_command(command: list, description: str) -> bool:
    """Run a shell command and report status"""
    print(f"\n📦 {description}...")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"Error: {e.stderr}")
        return False
    except FileNotFoundError:
        print(f"❌ Command not found: {command[0]}")
        return False


def main():
    """Execute build pipeline"""
    print("\n" + "=" * 60)
    print("  GITHUB PROFILE BUILD SYSTEM")
    print("=" * 60)

    scripts_dir = Path(__file__).parent
    project_dir = scripts_dir.parent

    # Step 1: Generate Assets
    if not run_command(
        [sys.executable, str(scripts_dir / "build_assets.py")],
        "Generating SVG assets",
    ):
        print("⚠️  Asset generation failed, but continuing...")

    # Step 2: Verify README
    if not run_command(
        [sys.executable, str(scripts_dir / "verify_readme.py")],
        "Verifying README.md",
    ):
        print("⚠️  README verification failed, check manually before deploying")
        return False

    print("\n" + "=" * 60)
    print("  ✅ BUILD COMPLETE")
    print("=" * 60)
    print("\n📋 Next steps:")
    print("   1. Review generated assets in /assets directory")
    print("   2. Commit changes: git add . && git commit -m 'build: generate assets'")
    print("   3. Push to GitHub: git push origin main")
    print("   4. GitHub Actions will automatically run on push")
    print("\n")

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
