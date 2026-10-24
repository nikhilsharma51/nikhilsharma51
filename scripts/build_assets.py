"""
Asset Generator - Creates all custom SVG animations
Generates: Hero banner, dividers, language chart, ASCII art
All assets are theme-aware (work in light + dark mode)
"""

import os
from datetime import datetime
from pathlib import Path
from theme import (
    THEME,
    DISPLAY_NAME,
    TAGLINE,
    TECH_STACK,
    SIZES,
    css_vars,
)

# Output directory
ASSETS_DIR = Path(__file__).parent.parent / "assets"
ASSETS_DIR.mkdir(exist_ok=True)


def save_svg(filename: str, content: str):
    """Save SVG content to file"""
    filepath = ASSETS_DIR / filename
    filepath.write_text(content, encoding="utf-8")
    print(f"✓ Generated: {filename}")


def generate_hero_banner():
    """
    Generate animated hero banner with typing effect
    Shows: Name + Typing animation of tagline
    """
    width = SIZES["hero_width"]
    height = SIZES["hero_height"]

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
    {css_vars()}
    <style>
        .hero-bg {{ fill: var(--bg); }}
        .hero-border {{ stroke: var(--accent); stroke-width: 2; fill: none; }}
        .hero-name {{ font-family: system-ui, sans-serif; font-size: 48px; font-weight: 700; fill: var(--accent); }}
        .hero-tagline {{ font-family: system-ui, sans-serif; font-size: 20px; fill: var(--muted); }}
        .typing-cursor {{ animation: blink 1s infinite; }}
        @keyframes blink {{
            0%, 49% {{ opacity: 1; }}
            50%, 100% {{ opacity: 0; }}
        }}
        .typing-clip {{
            animation: reveal 6s steps(40) infinite;
        }}
        @keyframes reveal {{
            0% {{ width: 0; }}
            60% {{ width: 100%; }}
            100% {{ width: 100%; }}
        }}
    </style>
    
    <!-- Background -->
    <rect class="hero-bg" width="{width}" height="{height}"/>
    <rect class="hero-border" x="1" y="1" width="{width-2}" height="{height-2}" rx="8"/>
    
    <!-- Name -->
    <text class="hero-name" x="40" y="60">{DISPLAY_NAME}</text>
    
    <!-- Typing Animation -->
    <g>
        <defs>
            <clipPath id="typing-clip">
                <rect class="typing-clip" x="0" y="0" width="0" height="35"/>
            </clipPath>
        </defs>
        <text class="hero-tagline" x="40" y="110" clip-path="url(#typing-clip)">{TAGLINE}</text>
        <text class="hero-tagline typing-cursor" x="40" y="110">_</text>
    </g>
</svg>"""

    save_svg("hero-banner.svg", svg)


def generate_divider():
    """
    Generate animated moving line divider
    Creates a subtle animated separator between sections
    """
    width = SIZES["divider_width"]
    height = SIZES["divider_height"]

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
    {css_vars()}
    <style>
        .divider-line {{ stroke: var(--accent); stroke-width: 2; }}
        .moving-dot {{ animation: move-dot 3s ease-in-out infinite; }}
        @keyframes move-dot {{
            0% {{ cx: 50; }}
            50% {{ cx: {width - 50}; }}
            100% {{ cx: 50; }}
        }}
        .pulse-glow {{ animation: glow 2s ease-in-out infinite; }}
        @keyframes glow {{
            0%, 100% {{ opacity: 0.3; }}
            50% {{ opacity: 1; }}
        }}
    </style>
    
    <!-- Background -->
    <rect fill="var(--bg)" width="{width}" height="{height}"/>
    
    <!-- Horizontal Line -->
    <line x1="0" y1="{height//2}" x2="{width}" y2="{height//2}" class="divider-line" opacity="0.3"/>
    
    <!-- Moving Dot -->
    <circle class="moving-dot pulse-glow" cy="{height//2}" r="6" fill="var(--accent)"/>
    
    <!-- Accent Line Under -->
    <line x1="0" y1="{height//2 + 8}" x2="{width}" y2="{height//2 + 8}" stroke="var(--accent)" stroke-width="1" opacity="0.1"/>
</svg>"""

    save_svg("divider.svg", svg)


def generate_language_chart():
    """
    Generate language breakdown chart
    Shows distribution of your tech stack by category
    """
    width = SIZES["chart_width"]
    height = 180

    categories = list(TECH_STACK.keys())
    colors = [THEME["accent"], THEME["accent_soft"], THEME["accent_deep"]]
    bar_height = 40
    spacing = 15

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
    {css_vars()}
    <style>
        .chart-bg {{ fill: var(--bg); }}
        .chart-label {{ font-family: system-ui, sans-serif; font-size: 14px; fill: var(--ink); font-weight: 600; }}
        .chart-bar {{ fill: var(--accent); animation: grow 1s ease-out forwards; }}
        .bar-1 {{ --bar-width: 85%; }}
        .bar-2 {{ --bar-width: 75%; }}
        .bar-3 {{ --bar-width: 80%; }}
        @keyframes grow {{
            from {{ width: 0%; }}
            to {{ width: var(--bar-width); }}
        }}
        .tech-text {{ font-family: system-ui, sans-serif; font-size: 12px; fill: var(--muted); }}
    </style>
    
    <!-- Background -->
    <rect class="chart-bg" width="{width}" height="{height}"/>
    
    <!-- Chart Title -->
    <text class="chart-label" x="20" y="25">Tech Stack Distribution</text>
    
    <!-- Bars -->"""

    y_offset = 50
    for idx, (category, color) in enumerate(zip(categories, colors)):
        tech_count = len(TECH_STACK[category])
        width_pct = (tech_count / 7) * 100  # Normalize to 7 as max
        
        svg += f"""
    <!-- {category} -->
    <text class="chart-label" x="20" y="{y_offset + 15}">{category}</text>
    <rect class="chart-bar bar-{idx + 1}" x="200" y="{y_offset - 10}" height="20" fill="{color}" rx="3" style="width: var(--bar-width);"/>
    <text class="tech-text" x="710" y="{y_offset + 5}">{tech_count} items</text>"""
        
        y_offset += bar_height + spacing

    svg += f"""
</svg>"""

    save_svg("language-chart.svg", svg)


def generate_ascii_art():
    """
    Generate ASCII art placeholder
    In production, this would convert a profile photo to ASCII art
    For now, creating a professional placeholder
    """
    width = SIZES["hero_width"]
    height = 250

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
    {css_vars()}
    <style>
        .ascii-bg {{ fill: var(--surface); }}
        .ascii-border {{ stroke: var(--grid); stroke-width: 1; fill: none; }}
        .ascii-text {{ font-family: 'Courier New', monospace; font-size: 10px; fill: var(--accent); line-height: 1.2; }}
        .ascii-title {{ font-family: system-ui, sans-serif; font-size: 14px; fill: var(--ink); font-weight: 600; }}
    </style>
    
    <!-- Background -->
    <rect class="ascii-bg" width="{width}" height="{height}"/>
    <rect class="ascii-border" x="1" y="1" width="{width-2}" height="{height-2}" rx="4"/>
    
    <!-- Title -->
    <text class="ascii-title" x="20" y="25">Profile | nikhilsharma51</text>
    
    <!-- ASCII Art -->
    <text class="ascii-text" x="20" y="50">╔════════════════════════════════════════════════════════════╗</text>
    <text class="ascii-text" x="20" y="65">║                                                            ║</text>
    <text class="ascii-text" x="20" y="80">║   NIKHIL SHARMA                                            ║</text>
    <text class="ascii-text" x="20" y="95">║   Full-Stack Developer · AI/ML Explorer                   ║</text>
    <text class="ascii-text" x="20" y="110">║   Building Agentic Systems                               ║</text>
    <text class="ascii-text" x="20" y="125">║                                                            ║</text>
    <text class="ascii-text" x="20" y="140">║   ► Frontend  : React, Next.js, TypeScript                ║</text>
    <text class="ascii-text" x="20" y="155">║   ► Backend   : Node.js, Express, Python                 ║</text>
    <text class="ascii-text" x="20" y="170">║   ► AI/ML     : LangChain, RAG, Agentic AI               ║</text>
    <text class="ascii-text" x="20" y="185">║                                                            ║</text>
    <text class="ascii-text" x="20" y="200">║   Location: Delhi | Open to Internships & Opportunities  ║</text>
    <text class="ascii-text" x="20" y="215">║                                                            ║</text>
    <text class="ascii-text" x="20" y="230">╚════════════════════════════════════════════════════════════╝</text>
</svg>"""

    save_svg("ascii-profile.svg", svg)


def generate_stats_placeholder():
    """
    Generate placeholder for daily stats
    Will be updated by GitHub Actions workflow
    """
    width = SIZES["hero_width"]
    height = 150

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
    {css_vars()}
    <style>
        .stats-bg {{ fill: var(--surface); }}
        .stats-border {{ stroke: var(--grid); stroke-width: 1; fill: none; }}
        .stats-label {{ font-family: system-ui, sans-serif; font-size: 14px; fill: var(--muted); font-weight: 500; }}
        .stats-value {{ font-family: system-ui, sans-serif; font-size: 24px; fill: var(--accent); font-weight: 700; }}
    </style>
    
    <!-- Background -->
    <rect class="stats-bg" width="{width}" height="{height}"/>
    <rect class="stats-border" x="0" y="0" width="{width}" height="{height}" rx="4"/>
    
    <!-- Stat 1 -->
    <text class="stats-label" x="40" y="35">Contributions (This Year)</text>
    <text class="stats-value" x="40" y="75">Loading...</text>
    
    <!-- Stat 2 -->
    <text class="stats-label" x="350" y="35">Public Repos</text>
    <text class="stats-value" x="350" y="75">Loading...</text>
    
    <!-- Stat 3 -->
    <text class="stats-label" x="600" y="35">Total Stars</text>
    <text class="stats-value" x="600" y="75">Loading...</text>
    
    <!-- Update Time -->
    <text class="stats-label" x="40" y="130">Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}</text>
</svg>"""

    save_svg("stats-card.svg", svg)


def main():
    """Generate all assets"""
    print("\n🎨 Generating SVG assets...\n")

    generate_hero_banner()
    generate_divider()
    generate_language_chart()
    generate_ascii_art()
    generate_stats_placeholder()

    print(f"\n✓ All assets generated to: {ASSETS_DIR}\n")


if __name__ == "__main__":
    main()
