from PIL import Image
import os

def crop_center_design(image_path, output_path=None):
    image = Image.open(image_path).convert("RGB")
    width, height = image.size

    # Define the crop box as a percentage of the original dimensions
    left = int(width * 0.2)
    right = int(width * 0.8)
    top = int(height * 0.1)
    bottom = int(height * 0.8)

    cropped = image.crop((left, top, right, bottom))

    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cropped.save(output_path)
        print(f"Cropped to center design and saved to {output_path}")

    return cropped

def main():
    input_path = "data/images/redbubble/0.jpg"
    output_path = "data/cropped/redbubble/0_cropped.jpg"

    crop_center_design(input_path, output_path).show()

# Example usage:
if __name__ == "__main__":
    main()
