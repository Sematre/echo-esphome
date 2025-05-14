import sys
import json

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy.ndimage import gaussian_filter

# Constants for conversion
DPI = 300  # Image resolution in DPI
MM_TO_INCH = 25.4  # Conversion from millimeters to inches

def mm_to_pixels(mm, dpi=DPI):
    """Convert millimeters to pixels based on the image DPI."""
    return int((mm / MM_TO_INCH) * dpi)

def get_points(json_report_path):
    points = []

    # Load the JSON report
    with open(json_report_path, 'r') as file:
        report = json.load(file)
    
    # Annotate unconnected items
    for error in report.get('unconnected_items', []):
        description = error['description']
        for item in error['items']:
            # Get the position in millimeters and convert to pixels
            pos_mm = item['pos']

            # Add it to the list
            points.append((
                mm_to_pixels(pos_mm['x']),
                mm_to_pixels(pos_mm['y']),
                0.5,
            ))
    
    return points

def create_heatmap_overlay(width, height, points, max_radius=100, alpha=0.7, merge_method='screen'):
    """
    Create a heatmap overlay with different merging strategies.
    
    Args:
        merge_method: How to merge overlapping bubbles
            'maximum' - take the maximum value (original method)
            'additive' - simply add values (can lead to oversaturation)
            'weighted' - weighted addition that prevents exceeding 1.0
            'screen' - similar to Photoshop's screen blend mode
    """
    # Create a heat accumulation map
    heatmap = np.zeros((height, width), dtype=np.float32)
    
    # Generate each bubble's contribution
    for px, py, intensity in points:
        # Create a more complex hill function for each bubble
        y, x = np.ogrid[:height, :width]
        dist_squared = ((x - px) ** 2 + (y - py) ** 2).astype(np.float32)
        radius = int(max_radius * intensity)
        
        # Create a radial gradient with a more sophisticated falloff
        # Using a combination of Gaussian and polynomial falloff for smoother edges
        mask = dist_squared <= (radius ** 2)
        normalized_dist = np.sqrt(dist_squared[mask]) / radius
        
        # Create a smoother hill function (polynomial with cubic interpolation)
        # This creates a more natural-looking falloff than pure Gaussian
        radial_gradient = np.zeros_like(heatmap)
        radial_gradient[mask] = (1 - normalized_dist**2)**2 * intensity
        
        # Apply the selected merging strategy
        if merge_method == 'maximum':
            heatmap = np.maximum(heatmap, radial_gradient)
        elif merge_method == 'additive':
            heatmap += radial_gradient
        elif merge_method == 'weighted':
            # Weighted addition prevents oversaturation
            heatmap = heatmap + radial_gradient * (1 - heatmap)
        elif merge_method == 'screen':
            # Screen blend mode (like in Photoshop)
            # Formula: 1 - (1-a) * (1-b)
            heatmap = 1 - (1 - heatmap) * (1 - radial_gradient)
    
    # Normalize if we went over 1.0 (especially likely with additive method)
    if merge_method == 'additive':
        heatmap = np.clip(heatmap, 0, 1)
    
    # Apply light gaussian blur for smoother transitions
    heatmap = gaussian_filter(heatmap, sigma=2)
    
    # Create our custom colormap
    colors = [(1, 0, 0, 1),      # red
              (1, 0.5, 0, 1),    # orange
              (1, 1, 0, 1),      # yellow
              (0, 0.8, 0, 1),    # green
              (0, 0.8, 0.8, 1)]  # teal
    
    cmap = LinearSegmentedColormap.from_list("custom_heatmap", colors)
    
    # Apply the colormap
    colored_heatmap = cmap(1 - heatmap)  # 1-heatmap reverses it so red is center
    
    # Convert to 8-bit RGBA
    overlay = (colored_heatmap * 255).astype(np.uint8)
    overlay[:, :, 3] = (heatmap * alpha * 255).astype(np.uint8)
    
    return overlay

def apply_heatmap_to_image(points, image_path, output_path, max_radius=100, merge_method='screen'):
    # Function remains mostly the same
    img = Image.open(image_path)
    width, height = img.size
    
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    img_array = np.array(img)
    
    overlay = create_heatmap_overlay(width, height, points, max_radius, 
                                     merge_method=merge_method)
    
    alpha = overlay[:, :, 3:4] / 255.0
    result = overlay[:, :, :3] * alpha + img_array[:, :, :3] * (1 - alpha)
    final = np.dstack((result.astype(np.uint8), img_array[:, :, 3]))
    
    output_img = Image.fromarray(final)
    output_img.save(output_path)
    
    return output_img

if __name__ == "__main__":
    # Command-line arguments: json_report_path, input_image_path, output_image_path
    if len(sys.argv) != 4:
        print("Usage: python overlay_heatmap.py <json_report_path> <input_image_path> <output_image_path>")
        sys.exit(1)

    json_report_path = sys.argv[1]
    input_image_path = sys.argv[2]
    output_image_path = sys.argv[3]

    points = get_points(json_report_path)

    # Try different merge methods and save multiple outputs
    apply_heatmap_to_image(
        points,
        input_image_path,
        output_image_path,
        max_radius=120,
        merge_method='screen',
    )
