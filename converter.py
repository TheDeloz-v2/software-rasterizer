from PIL import Image

def bmp_to_jpg(input_path, output_path):
    try:
        image = Image.open(input_path)
        
        image.save(output_path, "JPEG")
        
        print(f"Successful conversion: {input_path} -> {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")

