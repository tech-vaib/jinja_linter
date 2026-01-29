import sys
from pathlib import Path
from jinja2 import Template, TemplateSyntaxError


def check_file(file_path: Path) -> bool:
    try:
        with file_path.open("r", encoding="utf-8") as f:
            content = f.read()

        Template(content)
        print(f"✅ OK: {file_path}")
        return True

    except TemplateSyntaxError as e:
        print(f"❌ SYNTAX ERROR: {file_path}")
        print(f"   Line {e.lineno}: {e.message}")
        return False

    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {file_path}")
        print(f"   {e}")
        return False


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent

    # 🔹 Your requested pattern
    jinja_files = list(repo_root.glob("pr-*/**/pr*.jinja"))

    if not jinja_files:
        print("ℹ️ No matching Jinja files found (pr-*/**/pr*.jinja)")
        return 0

    print(f"🔍 Found {len(jinja_files)} Jinja file(s)\n")

    failed = []

    for jinja_file in jinja_files:
        if not check_file(jinja_file):
            failed.append(jinja_file)

    if failed:
        print("\n🚨 The following Jinja files failed validation:")
        for f in failed:
            print(f" - {f}")
        return 1

    print("\n🎉 All Jinja files are valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
