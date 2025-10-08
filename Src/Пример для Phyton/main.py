import os
from user_interface import main as start_program
def main():
    try:
        start_program()
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем")
    except Exception as e:
        print(f"\nПроизошла ошибка: {e}")

if __name__ == "__main__":
    main()