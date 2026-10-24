"""
Theme Configuration - Single Source of Truth for Visual Identity
All brand colors, fonts, and design tokens defined here.
Change one value → entire profile updates automatically.
"""

# ============================================================================
# BRAND IDENTITY
# ============================================================================

USERNAME = "nikhilsharma51"
DISPLAY_NAME = "Nikhil Sharma"
LOCATION = "Delhi"
TAGLINE = "Full-Stack Developer · AI/ML Explorer · Building Agentic Systems"

# ============================================================================
# COLOR PALETTE - Modern Professional (Blues & Teals)
# ============================================================================

THEME = {
    # PRIMARY ACCENT - Core brand color
    "accent": "#0066CC",              # Primary blue
    "accent_deep": "#003D99",         # Darker blue (20% darker)
    "accent_soft": "#3399FF",         # Lighter blue (20% lighter)
    
    # DARK MODE (design for dark first - GitHub default)
    "bg_dark": "#0D1117",             # GitHub dark background
    "surface_dark": "#161B22",        # Card/panel background
    "ink_dark": "#C9D1D9",            # Primary text (light gray)
    "muted_dark": "#8B949E",          # Secondary text (dim gray)
    "grid_dark": "#30363D",           # Subtle borders/dividers
    "accent_dark": "#58A6FF",         # Lighter blue for dark mode
    
    # LIGHT MODE (flip contrast)
    "bg_light": "#FFFFFF",            # White background
    "surface_light": "#F6F8FA",       # Light panel background
    "ink_light": "#24292F",           # Dark text
    "muted_light": "#57606A",         # Gray text
    "grid_light": "#D0D7DE",          # Light borders
    "accent_light": "#0066CC",        # Primary blue
}

# ============================================================================
# TYPOGRAPHY
# ============================================================================

FONTS = {
    "sans": "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif",
    "mono": "'Courier New', monospace",
}

# ============================================================================
# SPACING & SIZING
# ============================================================================

SIZES = {
    "hero_width": 830,                # Mobile-safe max width
    "hero_height": 200,
    "divider_width": 830,
    "divider_height": 30,
    "chart_width": 830,
    "chart_height": 300,
}

# ============================================================================
# SVG STYLE TEMPLATES
# ============================================================================

def css_vars():
    """Generate CSS variables for theme switching (light/dark mode)"""
    return f"""
    <style>
        :root {{
            --accent: {THEME['accent_dark']};
            --accent-deep: {THEME['accent_deep']};
            --accent-soft: {THEME['accent_soft']};
            --bg: {THEME['bg_dark']};
            --surface: {THEME['surface_dark']};
            --ink: {THEME['ink_dark']};
            --muted: {THEME['muted_dark']};
            --grid: {THEME['grid_dark']};
        }}
        @media (prefers-color-scheme: light) {{
            :root {{
                --accent: {THEME['accent_light']};
                --accent-deep: {THEME['accent_deep']};
                --accent-soft: {THEME['accent_soft']};
                --bg: {THEME['bg_light']};
                --surface: {THEME['surface_light']};
                --ink: {THEME['ink_light']};
                --muted: {THEME['muted_light']};
                --grid: {THEME['grid_light']};
            }}
        }}
    </style>
    """


def card_params(accent_color=None):
    """Generate parameters for external service URLs (shields.io, etc)"""
    color = (accent_color or THEME["accent"]).lstrip("#")
    return {
        "color": color,
        "labelColor": THEME["accent_deep"].lstrip("#"),
        "style": "flat-square",
    }


def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(r, g, b):
    """Convert RGB tuple to hex color"""
    return f"#{r:02x}{g:02x}{b:02x}"


def lighten(hex_color, percent=20):
    """Lighten a hex color by percentage"""
    r, g, b = hex_to_rgb(hex_color)
    r = min(255, int(r + (255 - r) * percent / 100))
    g = min(255, int(g + (255 - g) * percent / 100))
    b = min(255, int(b + (255 - b) * percent / 100))
    return rgb_to_hex(r, g, b)


def darken(hex_color, percent=20):
    """Darken a hex color by percentage"""
    r, g, b = hex_to_rgb(hex_color)
    r = max(0, int(r * (1 - percent / 100)))
    g = max(0, int(g * (1 - percent / 100)))
    b = max(0, int(b * (1 - percent / 100)))
    return rgb_to_hex(r, g, b)


# ============================================================================
# TECH STACK CONFIGURATION
# ============================================================================

TECH_STACK = {
    "Frontend": ["React", "Next.js", "TypeScript", "Tailwind CSS", "HTML", "CSS"],
    "Backend": ["Node.js", "Express", "Python", "MongoDB", "Supabase", "Prisma"],
    "AI/ML": ["LangChain", "RAG", "Generative AI", "Agentic AI", "LangGraph"],
}

# ============================================================================
# CONTACT INFORMATION
# ============================================================================

CONTACTS = {
    "email": "nikhilsharma721764@gmail.com",
    "twitter": "https://twitter.com/nikhilsharma51",  # Update with your handle
    "linkedin": "https://linkedin.com/in/nikhilsharma51",  # Update with your profile
    "github": "https://github.com/nikhilsharma51",
}

# ============================================================================
# FEATURED PROJECTS (Update these to your actual repos)
# ============================================================================

FEATURED_PROJECTS = [
    {
        "name": "Project 1",
        "description": "Your first featured project",
        "url": "https://github.com/nikhilsharma51/project-1",
        "lang": "TypeScript",
    },
    {
        "name": "Project 2",
        "description": "Your second featured project",
        "url": "https://github.com/nikhilsharma51/project-2",
        "lang": "Python",
    },
    {
        "name": "Project 3",
        "description": "Your third featured project",
        "url": "https://github.com/nikhilsharma51/project-3",
        "lang": "JavaScript",
    },
]

if __name__ == "__main__":
    print("✓ Theme configuration loaded")
    print(f"  Brand: {DISPLAY_NAME} (@{USERNAME})")
    print(f"  Tagline: {TAGLINE}")
    print(f"  Primary Color: {THEME['accent']}")
