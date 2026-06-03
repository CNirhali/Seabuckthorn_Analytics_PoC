from PIL import Image
import glob
import os

# Create an animated WebP from the generated plots to demonstrate the results
image_files = ['data/market_overview.png', 'data/pricing_analysis.png', 'data/claims_analysis.png']
images = []

for file in image_files:
    if os.path.exists(file):
        # Open and resize a bit if needed
        img = Image.open(file).convert("RGB")
        # Resize all to match the first one for consistent video frame size
        if not images:
            base_size = img.size
        else:
            img = img.resize(base_size, Image.Resampling.LANCZOS)
        images.append(img)

if images:
    # Save as animated webp
    output_path = "demo.webp"
    images[0].save(
        output_path, 
        format="WebP",
        save_all=True,
        append_images=images[1:],
        duration=2000, # 2 seconds per frame
        loop=0 # Infinite loop
    )
    print(f"Successfully generated {output_path}")
else:
    print("No images found to generate demo.webp. Please run the EDA notebook first.")
