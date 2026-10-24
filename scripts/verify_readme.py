"""
README Verification Suite - CI Quality Gate
Validates README.md before deployment
Checks: Accessibility, link validity, mobile-friendly, theme consistency
"""

import re
from pathlib import Path
from urllib.parse import urlparse


class ReadmeVerifier:
    """Validates README against professional standards"""

    def __init__(self):
        self.readme_path = Path(__file__).parent.parent / "README.md"
        self.errors = []
        self.warnings = []

    def read_readme(self) -> str:
        """Read README content"""
        if not self.readme_path.exists():
            self.errors.append("❌ README.md not found")
            return ""
        return self.readme_path.read_text(encoding="utf-8")

    def check_alt_text(self, content: str):
        """Verify all images have alt text"""
        # Pattern: ![alt](url)
        images = re.findall(r"!\[(.*?)\]\((.*?)\)", content)
        for alt, url in images:
            if not alt or alt.strip() == "":
                self.errors.append(f"❌ Image missing alt text: {url}")

    def check_links_resolve(self, content: str):
        """Verify all links are valid URLs or internal paths"""
        # Pattern: [text](url)
        links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)
        for text, url in links:
            if url.startswith("http"):
                # Check URL structure (basic validation)
                parsed = urlparse(url)
                if not parsed.scheme or not parsed.netloc:
                    self.errors.append(f"❌ Invalid URL: {url}")
            elif not url.startswith("#"):
                # Internal link - should exist or be an anchor
                if not url.startswith("/"):
                    self.warnings.append(f"⚠️  Relative link (verify manually): {url}")

    def check_mobile_width(self, content: str):
        """Verify no elements exceed mobile-safe width (830px)"""
        # Check for hardcoded large widths
        if re.search(r'width\s*=\s*["\']?([0-9]{4,})', content):
            matches = re.findall(r'width\s*=\s*["\']?(\d+)', content)
            for width in matches:
                if int(width) > 830:
                    self.errors.append(
                        f"❌ Element width exceeds 830px: {width}px"
                    )

    def check_theme_consistency(self, content: str):
        """Verify colors come from theme.py (no hardcoded colors in README)"""
        # Look for hex colors in markdown
        hex_colors = re.findall(r"#[0-9a-fA-F]{6}", content)
        if hex_colors:
            self.warnings.append(
                f"⚠️  Hardcoded colors found (use theme.py): {', '.join(set(hex_colors))}"
            )

    def check_structure(self, content: str):
        """Verify basic README structure"""
        required_sections = [
            ("Name/Title", r"^#+\s+Nikhil Sharma", re.MULTILINE),
            ("About", r"##\s+About|##\s+Hi|##\s+Introduction", re.MULTILINE),
            ("Contact", r"(LinkedIn|Email|Twitter|Contact)", re.MULTILINE),
        ]

        for section_name, pattern, flags in required_sections:
            if not re.search(pattern, content, flags):
                self.warnings.append(f"⚠️  Missing section: {section_name}")

    def check_no_dangerous_tags(self, content: str):
        """Verify no <script> or other GitHub-stripped tags"""
        dangerous = [
            ("<script", "Script tags (will be stripped by GitHub)"),
            ("<iframe", "iFrame tags (not allowed by GitHub)"),
            ("javascript:", "JavaScript protocol (not allowed)"),
        ]

        for tag, description in dangerous:
            if tag in content.lower():
                self.errors.append(f"❌ {description}: {tag}")

    def check_svg_validity(self, content: str):
        """Verify SVG tags are properly formatted"""
        svg_embeds = re.findall(r'<svg[^>]*>', content)
        for svg in svg_embeds:
            if "xmlns" not in svg:
                self.warnings.append("⚠️  SVG missing xmlns attribute")

    def check_accessibility(self, content: str):
        """Verify basic accessibility standards"""
        # Check for heading hierarchy
        headings = re.findall(r"^#+\s", content, re.MULTILINE)
        if not headings:
            self.errors.append("❌ No headings found in README")

        # Check for proper list formatting
        unordered_lists = re.findall(r"^[-*]\s", content, re.MULTILINE)
        if not unordered_lists and not re.search(r"\d\.\s", content):
            self.warnings.append("⚠️  No lists found (consider adding structure)")

    def verify(self) -> bool:
        """Run all verification checks"""
        content = self.read_readme()
        if not content:
            return False

        print("\n🔍 Verifying README.md...\n")

        self.check_alt_text(content)
        self.check_links_resolve(content)
        self.check_mobile_width(content)
        self.check_theme_consistency(content)
        self.check_structure(content)
        self.check_no_dangerous_tags(content)
        self.check_svg_validity(content)
        self.check_accessibility(content)

        # Print results
        if self.errors:
            print("❌ ERRORS (will fail CI):")
            for error in self.errors:
                print(f"   {error}")
            print()

        if self.warnings:
            print("⚠️  WARNINGS (review but won't fail):")
            for warning in self.warnings:
                print(f"   {warning}")
            print()

        if not self.errors and not self.warnings:
            print("✅ README verification passed - ready to deploy!\n")
            return True

        if self.errors:
            print(f"❌ Verification failed with {len(self.errors)} error(s)\n")
            return False

        print(f"✅ Verification passed with {len(self.warnings)} warning(s)\n")
        return True


def main():
    """Run verification"""
    verifier = ReadmeVerifier()
    success = verifier.verify()
    exit(0 if success else 1)


if __name__ == "__main__":
    main()
