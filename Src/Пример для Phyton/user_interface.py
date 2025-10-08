import os
from image_processor import concat_images, resize_image, get_image_info, ensure_results_directory
def get_image_paths():
    print("\n       Введите информацию")
    
    while True:
        image1 = input("Введите путь к первому изображению: ").strip('"').strip()
        if os.path.exists(image1):
            info = get_image_info(image1)
            if info:
                print(f"    Размер: {info['size']}, Формат: {info['format']}")
            break
        print("Путь указан неверно")
    
    while True:
        image2 = input("Введите путь ко второму изображению: ").strip('"').strip()
        if os.path.exists(image2):
            info = get_image_info(image2)
            if info:
                print(f"    Размер: {info['size']}, Формат: {info['format']}")
            break
        print("Путь указан неверно")
    
    return image1, image2

def get_resize_option():
    print("\n       Изменение размера")
    while True:
        choice = input("Изменить размер изображений? (y/n): ").lower().strip()
        if choice in ['y', 'н', 'да']:
            return True
        elif choice in ['n', 'т', 'нет']:
            return False
        else:
            print("Введите 'y' (да) или 'n' (нет)")

def get_new_size():
    try:
        print("\nВведите новый размер изображений:")
        width = int(input("    Ширина (в пикселях): "))
        height = int(input("    Высота (в пикселях): "))
        
        if width <= 0 or height <= 0:
            print("Размер не может быть отрицательным")
            return None
            
        return (width, height)
    except ValueError:
        print("Введите числа")
        return None

def get_output_filename():
    print("\n       Сохранение результата")
    while True:
        filename = input("Введите имя для выходного файла (без расширения): ").strip()
        if filename:
            if not filename.lower().endswith(('.jpg', '.jpeg')):
                filename += '.jpg'
            return filename
        else:
            print("Имя файла не может быть пустым")

def process_images(image1, image2, resize_size=None):
    print("\n       Обработка изображений")
    output_filename = get_output_filename()
    if resize_size:
        image1_resized = resize_image(image1, resize_size)
        image2_resized = resize_image(image2, resize_size)
        if not image1_resized or not image2_resized:
            print("Ошибка при изменении размера!")
            return None
        image1 = image1_resized
        image2 = image2_resized
    result_path = concat_images(image1, image2, output_filename)
    
    return result_path

def show_result(result_path):
    if result_path and os.path.exists(result_path):
        info = get_image_info(result_path)
        if info:
            print(f"Размер изображения: {info['width']} x {info['height']}")
            print(f"Размер файла: {info['file_size']} байт")

        full_path = os.path.abspath(result_path)
        print(f"Полный путь: {full_path}")
        
    else:
        print("\nПроизошла ошибка при обработке изображений")
        print("Результирующий файл не был создан")

def ask_for_another_operation():
    while True:
        choice = input("\nВыполнить еще одну операцию? (y/n): ").lower().strip()
        if choice in ['y', 'н', 'да']:
            return True
        elif choice in ['n', 'т', 'нет']:
            return False
        else:
            print("Введите 'y' (да) или 'n' (нет)")

def cleanup_temp_files():
    try:
        results_dir = "Результаты"
        if os.path.exists(results_dir):
            for file in os.listdir(results_dir):
                if file.startswith('resized_') and file.endswith(('.jpg', '.jpeg', '.png')):
                    file_path = os.path.join(results_dir, file)
                    os.remove(file_path)
    except Exception as e:
        print(f"Не удалось удалить временные файлы: {e}")

def show_results_folder_info():
    results_dir = "Результаты"
    if os.path.exists(results_dir):
        files = os.listdir(results_dir)
        if files:
            for file in files:
                file_path = os.path.join(results_dir, file)
                file_size = os.path.getsize(file_path)

def main():
    try:
        ensure_results_directory()
        while True:
            image1, image2 = get_image_paths()
            need_resize = get_resize_option()
            resize_size = None
            if need_resize:
                resize_size = get_new_size()
                if not resize_size:
                    print("Продолжаем без изменения размера")
            result = process_images(image1, image2, resize_size)
            show_result(result)
            show_results_folder_info()
            cleanup_temp_files()
            if not ask_for_another_operation():
                break
                
    except KeyboardInterrupt:
        print("\n\nПрограмма завершена пользователем")
        cleanup_temp_files()
    except Exception as e:
        print(f"\nОшибка: {e}")
        cleanup_temp_files()

if __name__ == "__main__":
    main()