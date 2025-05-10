import os

# Расширения файлов, которые будем обрабатывать
VALID_EXTENSIONS = {'.py', '.js', '.css', '.html'}

# Путь к корневой папке проекта
ROOT_DIR = r'D:\GitProjects\Torgi_monet-diplom'  # замените при необходимости

# Файл, куда будет сохранён итоговый листинг
OUTPUT_FILE = 'full_source_listing.txt'


def collect_source_code(root_path):
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as output:
        for dirpath, _, filenames in os.walk(root_path):
            for filename in filenames:
                ext = os.path.splitext(filename)[1]
                if ext in VALID_EXTENSIONS:
                    full_path = os.path.join(dirpath, filename)
                    rel_path = os.path.relpath(full_path, root_path)

                    output.write(f"\n{'='*80}\n")
                    output.write(f"Файл: {rel_path}\n")
                    output.write(f"{'='*80}\n")

                    try:
                        with open(full_path, 'r', encoding='utf-8') as f:
                            output.write(f.read())
                    except Exception as e:
                        output.write(f"[ОШИБКА ЧТЕНИЯ ФАЙЛА]: {e}\n")


if __name__ == '__main__':
    collect_source_code(ROOT_DIR)
    print(f"✅ Готово. Листинг сохранён в файл: {OUTPUT_FILE}")
