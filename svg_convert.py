from PIL import Image, ImageDraw
import math


def create_extension_icons():
    """Create extension icons using PIL only (no external dependencies)"""

    sizes = [16, 48, 128]

    for size in sizes:
        # Create a new image with transparent background
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Colors
        bg_color = (26, 115, 232)  # Google Blue
        white = (255, 255, 255)

        # Scale everything based on size
        center = size // 2
        radius = int(size * 0.44)  # Background circle radius

        # Draw background circle
        draw.ellipse([center - radius, center - radius,
                      center + radius, center + radius],
                     fill=bg_color)

        # Draw search magnifying glass
        glass_radius = int(size * 0.15)
        glass_center_x = int(size * 0.35)
        glass_center_y = int(size * 0.35)
        stroke_width = max(1, size // 32)

        # Search circle (outline only)
        draw.ellipse([glass_center_x - glass_radius, glass_center_y - glass_radius,
                      glass_center_x + glass_radius, glass_center_y + glass_radius],
                     outline=white, width=stroke_width)

        # Search handle
        handle_start_x = glass_center_x + int(glass_radius * 0.7)
        handle_start_y = glass_center_y + int(glass_radius * 0.7)
        handle_end_x = int(size * 0.75)
        handle_end_y = int(size * 0.75)

        # Draw handle line (approximated with small rectangles for thickness)
        dx = handle_end_x - handle_start_x
        dy = handle_end_y - handle_start_y
        length = math.sqrt(dx * dx + dy * dy)
        if length > 0:
            steps = int(length)
            for i in range(steps):
                x = handle_start_x + (dx * i // steps)
                y = handle_start_y + (dy * i // steps)
                draw.rectangle([x - stroke_width // 2, y - stroke_width // 2,
                                x + stroke_width // 2, y + stroke_width // 2], fill=white)

        # Draw API connection dots (only for larger sizes)
        if size >= 48:
            dot_radius = max(1, size // 32)

            # Three dots representing API connections
            dots = [
                (int(size * 0.7), int(size * 0.25)),
                (int(size * 0.8), int(size * 0.4)),
                (int(size * 0.7), int(size * 0.55))
            ]

            for dot_x, dot_y in dots:
                draw.ellipse([dot_x - dot_radius, dot_y - dot_radius,
                              dot_x + dot_radius, dot_y + dot_radius], fill=white)

                # Draw connection lines from search center to dots
                line_width = max(1, size // 64)
                steps = 20
                dx = dot_x - glass_center_x
                dy = dot_y - glass_center_y
                for i in range(steps):
                    x = glass_center_x + (dx * i // steps)
                    y = glass_center_y + (dy * i // steps)
                    draw.rectangle([x - line_width // 2, y - line_width // 2,
                                    x + line_width // 2, y + line_width // 2],
                                   fill=(255, 255, 255, 180))  # Semi-transparent

        # Save the image
        filename = f'icon{size}.png'
        img.save(filename, 'PNG')
        print(f"✅ Created {filename} ({size}x{size})")

    print(f"\n🎉 Successfully created all icon files!")
    print("Your extension now has custom icons!")


if __name__ == "__main__":
    create_extension_icons()