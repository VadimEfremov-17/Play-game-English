import json
import random
import time
import os
from datetime import datetime

class WordMaster:
    def __init__(self, filename="words.json"):
        self.filename = filename
        self.words = self.load_words()
        self.stats = {
            'games_played': 0,
            'total_score': 0,
            'best_score': 0,
            'words_learned': set()
        }
        self.load_stats()
    
    def load_words(self):
        """Загрузка слов из JSON файла"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Файл {self.filename} не найден. Создаю базовый словарь...")
            return self.create_default_words()
    
    def create_default_words(self):
        """Создание базового словаря, если файл не найден"""
        default_words = {
            "beginner": [
                {"en": "hello", "ru": "привет", "example": "Hello, how are you?"},
                {"en": "goodbye", "ru": "до свидания", "example": "Goodbye, see you tomorrow!"},
                {"en": "thank you", "ru": "спасибо", "example": "Thank you for your help."}
            ]
        }
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(default_words, f, ensure_ascii=False, indent=2)
        return default_words
    
    def save_words(self):
        """Сохранение слов в JSON файл"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.words, f, ensure_ascii=False, indent=2)
    
    def load_stats(self):
        """Загрузка статистики"""
        try:
            with open('stats.json', 'r') as f:
                self.stats = json.load(f)
                # Преобразуем список обратно в множество
                self.stats['words_learned'] = set(self.stats.get('words_learned', []))
        except FileNotFoundError:
            self.save_stats()
    
    def save_stats(self):
        """Сохранение статистики"""
        stats_to_save = self.stats.copy()
        stats_to_save['words_learned'] = list(stats_to_save['words_learned'])
        with open('stats.json', 'w') as f:
            json.dump(stats_to_save, f, indent=2)
    
    def choose_level(self):
        """Выбор уровня сложности"""
        print("\n" + "="*50)
        print("ВЫБЕРИТЕ УРОВЕНЬ СЛОЖНОСТИ:")
        print("="*50)
        
        levels = list(self.words.keys())
        for i, level in enumerate(levels, 1):
            word_count = len(self.words[level])
            print(f"{i}. {level.upper()} ({word_count} слов)")
        
        while True:
            try:
                choice = int(input(f"\nВыберите уровень (1-{len(levels)}): "))
                if 1 <= choice <= len(levels):
                    return levels[choice-1]
                else:
                    print("Неверный выбор. Попробуйте снова.")
            except ValueError:
                print("Пожалуйста, введите число.")
    
    def choose_mode(self):
        """Выбор режима игры"""
        print("\n" + "="*50)
        print("РЕЖИМЫ ИГРЫ:")
        print("="*50)
        modes = [
            "1. Быстрый перевод (рус → англ)",
            "2. Быстрый перевод (англ → рус)",
            "3. Выбор правильного перевода",
            "4. Заполни пропуск в предложении",
            "5. Диктант (английский)",
            "6. Смешанный режим (все задания)"
        ]
        
        for mode in modes:
            print(mode)
        
        while True:
            try:
                choice = int(input(f"\nВыберите режим (1-{len(modes)}): "))
                if 1 <= choice <= len(modes):
                    return choice
                else:
                    print("Неверный выбор. Попробуйте снова.")
            except ValueError:
                print("Пожалуйста, введите число.")
    
    def mode_1_translation_ru_en(self, level, num_questions=5):
        """Режим 1: Перевод с русского на английский"""
        print("\n" + "="*50)
        print("РЕЖИМ: Русский → Английский")
        print("="*50)
        print("Напишите английский перевод слова.\n")
        
        score = 0
        words = random.sample(self.words[level], min(num_questions, len(self.words[level])))
        
        for i, word in enumerate(words, 1):
            print(f"\nВопрос {i}/{len(words)}")
            print(f"Слово: {word['ru'].upper()}")
            
            answer = input("Ваш перевод: ").strip().lower()
            
            if answer == word['en'].lower():
                print(f"✅ Правильно! {word['en']} - {word['ru']}")
                print(f"Пример: {word['example']}")
                score += 2
                self.stats['words_learned'].add(word['en'])
            else:
                print(f"❌ Неправильно. Правильный ответ: {word['en']}")
                print(f"Пример: {word['example']}")
        
        return score
    
    def mode_2_translation_en_ru(self, level, num_questions=5):
        """Режим 2: Перевод с английского на русский"""
        print("\n" + "="*50)
        print("РЕЖИМ: Английский → Русский")
        print("="*50)
        print("Напишите русский перевод слова.\n")
        
        score = 0
        words = random.sample(self.words[level], min(num_questions, len(self.words[level])))
        
        for i, word in enumerate(words, 1):
            print(f"\nВопрос {i}/{len(words)}")
            print(f"Слово: {word['en'].upper()}")
            
            answer = input("Ваш перевод: ").strip().lower()
            
            # Проверяем несколько вариантов перевода (если их несколько через запятую)
            correct_translations = [t.strip().lower() for t in word['ru'].split(',')]
            
            if answer in correct_translations:
                print(f"✅ Правильно! {word['en']} - {word['ru']}")
                print(f"Пример: {word['example']}")
                score += 2
                self.stats['words_learned'].add(word['en'])
            else:
                print(f"❌ Неправильно. Правильный ответ: {word['ru']}")
                print(f"Пример: {word['example']}")
        
        return score
    
    def mode_3_multiple_choice(self, level, num_questions=5):
        """Режим 3: Выбор правильного перевода"""
        print("\n" + "="*50)
        print("РЕЖИМ: Выбор правильного перевода")
        print("="*50)
        print("Выберите правильный перевод слова.\n")
        
        score = 0
        all_words = self.words[level]
        
        for i in range(num_questions):
            # Выбираем правильное слово и 3 случайных неправильных
            correct_word = random.choice(all_words)
            wrong_words = random.sample([w for w in all_words if w != correct_word], 3)
            
            # Создаем список вариантов и перемешиваем
            options = wrong_words + [correct_word]
            random.shuffle(options)
            correct_index = options.index(correct_word)
            
            print(f"\nВопрос {i+1}/{num_questions}")
            print(f"Слово: {correct_word['en'].upper()}")
            print("\nВарианты ответа:")
            
            for j, option in enumerate(options, 1):
                print(f"{j}. {option['ru']}")
            
            while True:
                try:
                    choice = int(input("\nВаш выбор (1-4): "))
                    if 1 <= choice <= 4:
                        break
                    else:
                        print("Пожалуйста, введите число от 1 до 4.")
                except ValueError:
                    print("Пожалуйста, введите число.")
            
            if choice == correct_index + 1:
                print(f"✅ Правильно! {correct_word['en']} - {correct_word['ru']}")
                print(f"Пример: {correct_word['example']}")
                score += 1
                self.stats['words_learned'].add(correct_word['en'])
            else:
                print(f"❌ Неправильно. Правильный ответ: {correct_word['ru']}")
                print(f"Пример: {correct_word['example']}")
        
        return score
    
    def mode_4_fill_blank(self, level, num_questions=5):
        """Режим 4: Заполни пропуск в предложении"""
        print("\n" + "="*50)
        print("РЕЖИМ: Заполни пропуск")
        print("="*50)
        print("Введите слово, которое пропущено в предложении.\n")
        
        score = 0
        words = random.sample(self.words[level], min(num_questions, len(self.words[level])))
        
        for i, word in enumerate(words, 1):
            print(f"\nВопрос {i}/{len(words)}")
            
            # Создаем предложение с пропуском
            sentence = word['example']
            target_word = word['en']
            
            # Заменяем целевое слово на пропуск
            sentence_with_gap = sentence.replace(target_word, "______")
            print(f"Предложение: {sentence_with_gap}")
            print(f"Перевод пропущенного слова: {word['ru']}")
            
            answer = input("Введите пропущенное слово: ").strip().lower()
            
            if answer == target_word.lower():
                print(f"✅ Правильно! Полное предложение: {sentence}")
                score += 2
                self.stats['words_learned'].add(word['en'])
            else:
                print(f"❌ Неправильно. Правильный ответ: {target_word}")
                print(f"Полное предложение: {sentence}")
        
        return score
    
    def mode_5_dictation(self, level, num_questions=5):
        """Режим 5: Диктант"""
        print("\n" + "="*50)
        print("РЕЖИМ: Диктант")
        print("="*50)
        print("Напишите слово по его переводу.\n")
        
        score = 0
        words = random.sample(self.words[level], min(num_questions, len(self.words[level])))
        
        for i, word in enumerate(words, 1):
            print(f"\nВопрос {i}/{len(words)}")
            print(f"Перевод: {word['ru']}")
            
            answer = input("Напишите слово на английском: ").strip().lower()
            
            if answer == word['en'].lower():
                print(f"✅ Правильно! {word['en']} - {word['ru']}")
                print(f"Пример: {word['example']}")
                score += 3  # Диктант стоит больше очков
                self.stats['words_learned'].add(word['en'])
            else:
                print(f"❌ Неправильно. Правильный ответ: {word['en']}")
                print(f"Пример: {word['example']}")
        
        return score
    
    def mode_6_mixed(self, level, num_questions=10):
        """Режим 6: Смешанный режим"""
        print("\n" + "="*50)
        print("РЕЖИМ: Смешанный (все виды заданий)")
        print("="*50)
        
        score = 0
        words = random.sample(self.words[level], min(num_questions, len(self.words[level])))
        
        for i, word in enumerate(words, 1):
            print(f"\nВопрос {i}/{len(words)}")
            
            # Случайный выбор типа вопроса
            question_type = random.randint(1, 4)
            
            if question_type == 1:
                print(f"Переведите на английский: {word['ru'].upper()}")
                answer = input("Ваш ответ: ").strip().lower()
                if answer == word['en'].lower():
                    print(f"✅ Правильно!")
                    score += 2
                else:
                    print(f"❌ Неправильно. Правильно: {word['en']}")
            
            elif question_type == 2:
                print(f"Что означает '{word['en']}'?")
                answer = input("Ваш ответ: ").strip().lower()
                correct_translations = [t.strip().lower() for t in word['ru'].split(',')]
                if answer in correct_translations:
                    print(f"✅ Правильно!")
                    score += 2
                else:
                    print(f"❌ Неправильно. Правильно: {word['ru']}")
            
            elif question_type == 3:
                sentence = word['example'].replace(word['en'], "______")
                print(f"Заполните пропуск: {sentence}")
                print(f"(Перевод пропущенного слова: {word['ru']})")
                answer = input("Ваш ответ: ").strip().lower()
                if answer == word['en'].lower():
                    print(f"✅ Правильно!")
                    score += 2
                else:
                    print(f"❌ Неправильно. Правильно: {word['en']}")
            
            elif question_type == 4:
                print(f"Напишите по буквам слово с переводом '{word['ru']}':")
                answer = input("Ваш ответ: ").strip().lower()
                if answer == word['en'].lower():
                    print(f"✅ Правильно!")
                    score += 3
                else:
                    print(f"❌ Неправильно. Правильно: {word['en']}")
            
            self.stats['words_learned'].add(word['en'])
            print(f"Пример: {word['example']}")
            time.sleep(1)
        
        return score
    
    def add_new_word(self):
        """Добавление нового слова в словарь"""
        print("\n" + "="*50)
        print("ДОБАВЛЕНИЕ НОВОГО СЛОВА")
        print("="*50)
        
        level = self.choose_level()
        
        en_word = input("Введите слово на английском: ").strip()
        ru_word = input("Введите перевод на русский: ").strip()
        example = input("Введите пример предложения: ").strip()
        
        new_word = {
            "en": en_word,
            "ru": ru_word,
            "example": example
        }
        
        self.words[level].append(new_word)
        self.save_words()
        print(f"\n✅ Слово '{en_word}' добавлено в уровень '{level}'!")
    
    def show_stats(self):
        """Показать статистику"""
        print("\n" + "="*50)
        print("ВАША СТАТИСТИКА")
        print("="*50)
        print(f"Сыграно игр: {self.stats['games_played']}")
        print(f"Всего очков: {self.stats['total_score']}")
        print(f"Лучший результат: {self.stats['best_score']}")
        print(f"Изучено слов: {len(self.stats['words_learned'])}")
        
        # Показываем последние 5 изученных слов
        learned_words = list(self.stats['words_learned'])
        if learned_words:
            print("\nПоследние изученные слова:")
            for word in learned_words[-5:]:
                print(f"  • {word}")
    
    def show_dictionary(self, level=None):
        """Показать словарь"""
        print("\n" + "="*50)
        print("ВАШ СЛОВАРЬ")
        print("="*50)
        
        if level:
            if level in self.words:
                print(f"\nУровень: {level.upper()}")
                for i, word in enumerate(self.words[level], 1):
                    print(f"{i}. {word['en']} - {word['ru']}")
                    print(f"   Пример: {word['example']}")
            else:
                print("Такого уровня не существует.")
        else:
            for level_name, word_list in self.words.items():
                print(f"\n{level_name.upper()} ({len(word_list)} слов):")
                for word in word_list[:5]:  # Показываем только первые 5
                    print(f"  • {word['en']} - {word['ru']}")
                if len(word_list) > 5:
                    print(f"  ... и еще {len(word_list)-5} слов")
    
    def play_game(self):
        """Основной игровой цикл"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("✨" * 20)
        print("    WORD MASTER - Тренажер английских слов")
        print("✨" * 20)
        
        level = self.choose_level()
        mode = self.choose_mode()
        
        print("\nНачинаем игру!")
        time.sleep(1)
        
        # Определяем количество вопросов в зависимости от режима
        if mode in [6]:
            num_questions = 10
        else:
            num_questions = min(8, len(self.words[level]))
        
        score = 0
        
        # Запуск выбранного режима
        if mode == 1:
            score = self.mode_1_translation_ru_en(level, num_questions)
        elif mode == 2:
            score = self.mode_2_translation_en_ru(level, num_questions)
        elif mode == 3:
            score = self.mode_3_multiple_choice(level, num_questions)
        elif mode == 4:
            score = self.mode_4_fill_blank(level, num_questions)
        elif mode == 5:
            score = self.mode_5_dictation(level, num_questions)
        elif mode == 6:
            score = self.mode_6_mixed(level, num_questions)
        
        # Обновление статистики
        self.stats['games_played'] += 1
        self.stats['total_score'] += score
        if score > self.stats['best_score']:
            self.stats['best_score'] = score
        
        self.save_stats()
        
        # Результаты
        max_score = {
            1: num_questions * 2,
            2: num_questions * 2,
            3: num_questions * 1,
            4: num_questions * 2,
            5: num_questions * 3,
            6: num_questions * 2.5  # Среднее значение
        }.get(mode, num_questions * 2)
        
        print("\n" + "="*50)
        print("ИГРА ОКОНЧЕНА!")
        print("="*50)
        print(f"Ваш результат: {score} из {max_score} очков")
        
        percentage = (score / max_score) * 100
        if percentage >= 90:
            print("🎉 Отлично! Вы настоящий мастер слов!")
        elif percentage >= 70:
            print("👍 Хорошая работа!")
        elif percentage >= 50:
            print("😊 Неплохо, но есть куда стремиться!")
        else:
            print("💪 Продолжайте тренироваться!")
        
        input("\nНажмите Enter для возврата в меню...")
    
    def main_menu(self):
        """Главное меню"""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("✨" * 20)
            print("    WORD MASTER - Тренажер английских слов")
            print("✨" * 20)
            print("\nГЛАВНОЕ МЕНЮ:")
            print("1. 🎮 Начать игру")
            print("2. 📖 Просмотреть словарь")
            print("3. ➕ Добавить новое слово")
            print("4. 📊 Посмотреть статистику")
            print("5. 🏆 Таблица рекордов")
            print("6. ❌ Выйти из игры")
            
            choice = input("\nВыберите действие (1-6): ").strip()
            
            if choice == "1":
                self.play_game()
            elif choice == "2":
                level = input("Введите уровень (или Enter для всех): ").strip().lower()
                self.show_dictionary(level if level else None)
                input("\nНажмите Enter для продолжения...")
            elif choice == "3":
                self.add_new_word()
                input("\nНажмите Enter для продолжения...")
            elif choice == "4":
                self.show_stats()
                input("\nНажмите Enter для продолжения...")
            elif choice == "5":
                self.show_leaderboard()
                input("\nНажмите Enter для продолжения...")
            elif choice == "6":
                print("\nСпасибо за игру! До встречи! 👋")
                break
            else:
                print("Неверный выбор. Попробуйте снова.")
                time.sleep(1)
    
    def show_leaderboard(self):
        """Показать таблицу рекордов"""
        print("\n" + "="*50)
        print("ТАБЛИЦА РЕКОРДОВ")
        print("="*50)
        print(f"Ваш лучший результат: {self.stats['best_score']} очков")
        print(f"Всего изучено слов: {len(self.stats['words_learned'])}")
        print(f"Сыграно игр: {self.stats['games_played']}")
        
        # Показываем прогресс по уровням
        print("\nПрогресс по уровням:")
        for level in self.words:
            total_words = len(self.words[level])
            learned_in_level = len([w for w in self.words[level] 
                                  if w['en'] in self.stats['words_learned']])
            percentage = (learned_in_level / total_words) * 100 if total_words > 0 else 0
            print(f"{level.upper()}: {learned_in_level}/{total_words} слов "
                  f"({percentage:.1f}%)")

# Запуск игры
if __name__ == "__main__":
    game = WordMaster()
    game.main_menu()
