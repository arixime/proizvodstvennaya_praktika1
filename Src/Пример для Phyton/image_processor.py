from PIL import Image
import os
def ensure_results_directory():
    results_dir = "Результаты"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
        print(f"Создана папка: {results_dir}")
    return results_dir

def get_unique_filename(directory, filename):
    base_name, ext = os.path.splitext(filename)
    counter = 1
    unique_name = filename
    while os.path.exists(os.path.join(directory, unique_name)):
        unique_name = f"{base_name}_{counter}{ext}"
        counter += 1
    return unique_name
def resize_image(image_path, new_size):
    try:
        with Image.open(image_path) as img:
            original_mode = img.mode
            if original_mode != 'RGB':
                img = img.convert('RGB')
            resized_img = img.resize(new_size)
            base_name = os.path.basename(image_path)
            name, ext = os.path.splitext(base_name)
            output_filename = f"resized_{name}.jpg"
            results_dir = ensure_results_directory()
            unique_output_name = get_unique_filename(results_dir, output_filename)
            output_path = os.path.join(results_dir, unique_output_name)
            resized_img.save(output_path, quality=95)
            return output_path
    except Exception as e:
        print(f"Ошибка при изменении размера {image_path}: {e}")
        return None
def concat_images(image1_path, image2_path, output_name="combined_result.jpg"):
    try:
        with Image.open(image1_path) as img1, Image.open(image2_path) as img2:
            if img1.mode != 'RGB':
                img1 = img1.convert('RGB')
            if img2.mode != 'RGB':
                img2 = img2.convert('RGB')
            max_width = max(img1.width, img2.width)
            def scale_to_width(image, target_width):
                width_percent = target_width / float(image.width)
                new_height = int(float(image.height) * float(width_percent))
                return image.resize((target_width, new_height), Image.Resampling.LANCZOS)
            img1_scaled = scale_to_width(img1, max_width)
            img2_scaled = scale_to_width(img2, max_width)
            total_height = img1_scaled.height + img2_scaled.height
            new_image = Image.new('RGB', (max_width, total_height))
            new_image.paste(img1_scaled, (0, 0))
            new_image.paste(img2_scaled, (0, img1_scaled.height))
            results_dir = ensure_results_directory()
            unique_output_name = get_unique_filename(results_dir, output_name)
            output_path = os.path.join(results_dir, unique_output_name)
            new_image.save(output_path, quality=95)
            return output_path
            
    except Exception as e:
        print(f"Ошибка при склеивании: {e}")
        return None

def get_image_info(image_path):
    try:
        with Image.open(image_path) as img:
            file_stats = os.stat(image_path)
            info = {
                'size': img.size,
                'format': img.format,
                'mode': img.mode,
                'width': img.width,
                'height': img.height,
                'file_size': file_stats.st_size,
                'file_path': image_path
            }
            return info
    except Exception as e:
        print(f"Ошибка при получении информации: {e}")
        return None