import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from datetime import datetime

# Токен вашего бота
BOT_TOKEN = "TOKEN"

# Инициализация
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Список вопросов о дронах (50 вопросов)
DRONE_QUESTIONS = [
    {"question": "Что означает аббревиатура VTOL?",
     "options": ["Vertical Take-Off and Landing", "Variable Thrust Output Level", "Vertical Torque Over Load"],
     "correct": 0},

    {"question": "Какой датчик отвечает за определение высоты по давлению?",
     "options": ["Гироскоп", "Барометр", "Акселерометр"],
     "correct": 1},

    {"question": "Что такое failsafe у дрона?",
     "options": ["Режим экономии энергии", "Аварийный сценарий при потере сигнала", "Система охлаждения"],
     "correct": 1},

    {"question": "Какой параметр аккумулятора обозначается как mAh?",
     "options": ["Напряжение", "Ёмкость", "Ток разряда"],
     "correct": 1},

    {"question": "Что происходит при переразряде Li-Po аккумулятора?",
     "options": ["Увеличивается ёмкость", "Аккумулятор повреждается", "Ничего не происходит"],
     "correct": 1},

    {"question": "Как называется защитный режим аккумулятора при низком заряде?",
     "options": ["Low Voltage Cutoff", "Safe Power Mode", "Battery Lock"],
     "correct": 0},

    {"question": "Какой режим полёта использует GPS для стабилизации?",
     "options": ["Acro", "GPS Hold", "Manual"],
     "correct": 1},

    {"question": "Что такое yaw у дрона?",
     "options": ["Наклон вперёд/назад", "Поворот вокруг вертикальной оси", "Наклон вбок"],
     "correct": 1},

    {"question": "Что означает pitch?",
     "options": ["Поворот влево/вправо", "Наклон вперёд/назад", "Вращение моторов"],
     "correct": 1},

    {"question": "Что такое roll?",
     "options": ["Наклон влево/вправо", "Подъём вверх", "Поворот по курсу"],
     "correct": 0},

    {"question": "Какой протокол часто используется между приёмником и FC?",
     "options": ["PWM", "Оба варианта", "SBUS"],
     "correct": 2},

    {"question": "Что такое Blackbox логирование?",
     "options": ["Запись видео", "Запись телеметрии полёта", "Аварийный режим"],
     "correct": 1},

    {"question": "Какой параметр ESC отвечает за плавность запуска мотора?",
     "options": ["Timing", "Startup Power", "Current Limit"],
     "correct": 1},

    {"question": "Что означает C-рейтинг аккумулятора?",
     "options": ["Ёмкость", "Максимальный ток разряда", "Количество циклов"],
     "correct": 1},

    {"question": "Как называется режим удержания высоты?",
     "options": ["Altitude Hold", "Position Lock", "Hover Mode"],
     "correct": 0},

    {"question": "Что такое telemetry?",
     "options": ["Передача управляющих команд", "Передача данных о состоянии дрона", "Видеосигнал"],
     "correct": 1},

    {"question": "Какой элемент отвечает за распределение питания?",
     "options": ["PDB", "FC", "ESC"],
     "correct": 0},

    {"question": "Что такое RSSI?",
     "options": ["Уровень сигнала приёмника", "Скорость передачи данных", "Задержка видео"],
     "correct": 0},

    {"question": "Как называется эффект потери подъёмной силы при резком снижении?",
     "options": ["Ground Effect", "Vortex Ring State", "Prop Wash"],
     "correct": 1},

    {"question": "Что такое prop wash?",
     "options": ["Загрязнение пропеллеров", "Турбулентность от пропеллеров", "Потеря сигнала"],
     "correct": 1},

    {"question": "Какой материал чаще всего используется для рам FPV?",
     "options": ["Алюминий", "Карбон", "Пластик"],
     "correct": 1},

    {"question": "Что означает режим Angle?",
     "options": ["Полностью ручной", "С ограничением угла наклона", "Трюковой режим"],
     "correct": 1},

    {"question": "Какой параметр отвечает за резкость реакции дрона?",
     "options": ["PID", "GPS", "RSSI"],
     "correct": 0},

    {"question": "Что такое arm у дрона?",
     "options": ["Взлёт", "Разблокировка моторов", "Калибровка"],
     "correct": 1},

    {"question": "Как называется процесс настройки моторов и ESC?",
     "options": ["Синхронизация", "Калибровка", "Инициализация"],
     "correct": 1},

    {"question": "Что такое deadcat рама?",
     "options": ["Складная рама", "Рама без пропеллеров в кадре", "Гоночная рама"],
     "correct": 1},

    {"question": "Какой элемент уменьшает вибрации камеры?",
     "options": ["Подвес (gimbal)", "ESC", "Антенна"],
     "correct": 0},

    {"question": "Что такое gimbal?",
     "options": ["Антенна", "Стабилизатор камеры", "Тип рамы"],
     "correct": 1},

    {"question": "Какой режим чаще используют новички?",
     "options": ["Acro", "Angle", "Manual"],
     "correct": 1},

    {"question": "Что такое home point?",
     "options": ["Место хранения дрона", "Точка взлёта", "GPS спутник"],
     "correct": 1},

    {"question": "Как называется ограничение полётов по высоте?",
     "options": ["Ceiling Lock", "Altitude Limit", "Height Fence"],
     "correct": 1},

    {"question": "Что такое no-fly zone?",
     "options": ["Зона посадки", "Зона без GPS", "Запретная зона полётов"],
     "correct": 2},

    {"question": "Какой датчик измеряет ускорение?",
     "options": ["Акселерометр", "Барометр", "Магнетометр"],
     "correct": 0},

    {"question": "Что такое mag?",
     "options": ["Магнетометр", "Магнитный мотор", "Режим полёта"],
     "correct": 0},

    {"question": "Какой параметр влияет на время полёта?",
     "options": ["Вес дрона", "Ёмкость аккумулятора", "Оба варианта"],
     "correct": 2},

    {"question": "Что такое thrust?",
     "options": ["Скорость", "Подъёмная сила", "Вес"],
     "correct": 1},

    {"question": "Как называется защита винтов?",
     "options": ["Prop Guard", "Motor Shield", "Frame Lock"],
     "correct": 0},

    {"question": "Что означает BNF?",
     "options": ["Build Not Finished", "Bind-N-Fly", "Battery Not Found"],
     "correct": 1},

    {"question": "Что означает RTF?",
     "options": ["Ready To Fly", "Return To Field", "Remote Transfer Function"],
     "correct": 0},

    {"question": "Как называется передача видео в реальном времени?",
     "options": ["Streaming", "Live View", "FPV"],
     "correct": 2},

    {"question": "Что такое latency?",
     "options": ["Задержка сигнала", "Потеря качества", "Сила сигнала"],
     "correct": 0},

    {"question": "Какой параметр важен для дальности управления?",
     "options": ["Мощность передатчика", "Цвет дрона", "Размер пропеллеров"],
     "correct": 0},

    {"question": "Что такое antenna diversity?",
     "options": ["Использование нескольких антенн", "Тип поляризации", "Усиление сигнала"],
     "correct": 0},

    {"question": "Как называется автоматический взлёт?",
     "options": ["Auto Start", "Auto Takeoff", "Quick Launch"],
     "correct": 1},

    {"question": "Что такое crash recovery?",
     "options": ["Ремонт дрона", "Восстановление после переворота", "Запись аварии"],
     "correct": 1},

    {"question": "Какой фактор сильнее всего влияет на устойчивость?",
     "options": ["Ветер", "Цвет корпуса", "Форма аккумулятора"],
     "correct": 0},

    {"question": "Что такое hover?",
     "options": ["Резкий подъём", "Зависание на месте", "Автоматическая посадка"],
     "correct": 1},

    { "question": "Как называется датчик, определяющий направление по магнитному полю Земли?",
        "options": ["Акселерометр", "Магнетометр", "Гироскоп"],
        "correct": 1},

    {"question": "Что такое VTX в FPV-дроне?",
        "options": ["Видео-передатчик", "Видео-приёмник", "Контроллер камеры"],
        "correct": 0},

    {"question": "Как называется максимальное время нахождения дрона в воздухе?",
        "options": ["Flight Time", "Hover Time", "Air Limit"],
        "correct": 0}
]
    
    

class UserState(StatesGroup):
    waiting_for_fio = State()
    waiting_for_start = State()
    answering = State()

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer(
        "👋 Привет! Я бот для викторины о дронах 🚁\n\n"
        "📝 Для начала мне нужно узнать ваше ФИО.\n"
        "Пожалуйста, напишите ваше полное имя (Фамилия Имя Отчество):"
    )
    await state.set_state(UserState.waiting_for_fio)

@dp.message(UserState.waiting_for_fio)
async def process_fio(message: types.Message, state: FSMContext):
    fio = message.text.strip()
    
    # Проверка, что введено не пустое значение
    if len(fio) < 3:
        await message.answer("❌ Пожалуйста, введите ваше полное ФИО (минимум 3 символа).")
        return
    
    # Сохраняем ФИО и время регистрации
    await state.update_data(
        fio=fio,
        registration_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    
    await message.answer(
        f"✅ Отлично, {fio}!\n"
        f"Теперь вы можете начать викторину.\n\n"
        f"ℹ️ Я задам 50 вопросов о беспилотных летательных аппаратах.\n"
        f"📊 В конце вы узнаете результат.\n\n"
        f"Используйте команду /quiz чтобы начать!\n"
        f"Или /profile чтобы посмотреть свой профиль."
    )
    await state.set_state(UserState.waiting_for_start)

@dp.message(Command("profile"))
async def cmd_profile(message: types.Message, state: FSMContext):
    data = await state.get_data()
    fio = data.get("fio")
    
    if not fio:
        await message.answer(
            "❌ Вы ещё не зарегистрированы.\n"
            "Пожалуйста, используйте /start для регистрации."
        )
        return
    
    registration_date = data.get("registration_date", "Неизвестно")
    total_attempts = data.get("total_attempts", 0)
    best_score = data.get("best_score", 0)
    last_score = data.get("last_score", "Не пройдено")
    
    await message.answer(
        f"📋 <b>Ваш профиль:</b>\n\n"
        f"👤 <b>ФИО:</b> {fio}\n"
        f"📅 <b>Дата регистрации:</b> {registration_date}\n"
        f"🎯 <b>Всего попыток:</b> {total_attempts}\n"
        f"🏆 <b>Лучший результат:</b> {best_score}/50\n"
        f"📊 <b>Последний результат:</b> {last_score}\n\n"
        f"Используйте /quiz чтобы начать новую викторину!",
        parse_mode="HTML"
    )

@dp.message(Command("quiz"))
async def start_quiz(message: types.Message, state: FSMContext):
    data = await state.get_data()
    fio = data.get("fio")
    
    if not fio:
        await message.answer(
            "❌ Сначала нужно зарегистрироваться!\n"
            "Пожалуйста, используйте /start и введите ваше ФИО."
        )
        return
    
    # Увеличиваем счетчик попыток
    total_attempts = data.get("total_attempts", 0) + 1
    await state.update_data(total_attempts=total_attempts)
    
    await state.update_data(
        current_question=0,
        score=0,
        total_questions=len(DRONE_QUESTIONS),
        quiz_start_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    
    await message.answer(
        f"🎮 <b>Начинаем викторину!</b>\n\n"
        f"👤 <b>Участник:</b> {fio}\n"
        f"📊 <b>Всего вопросов:</b> 50\n"
        f"⏱️ <b>Время начала:</b> {datetime.now().strftime('%H:%M:%S')}\n\n"
        f"Удачи! 🚀",
        parse_mode="HTML"
    )
    
    # Ждем 2 секунды перед первым вопросом
    await asyncio.sleep(2)
    await ask_question(message, state)

async def ask_question(message: types.Message, state: FSMContext):
    data = await state.get_data()
    current = data.get("current_question", 0)
    
    if current >= len(DRONE_QUESTIONS):
        await finish_quiz(message, state)
        return
    
    question_data = DRONE_QUESTIONS[current]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text=option)] for option in question_data["options"]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
    await message.answer(
        f"❓ <b>Вопрос {current + 1}/{len(DRONE_QUESTIONS)}:</b>\n"
        f"{question_data['question']}",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await state.set_state(UserState.answering)

@dp.message(UserState.answering)
async def handle_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    current = data.get("current_question", 0)
    score = data.get("score", 0)
    
    if current >= len(DRONE_QUESTIONS):
        return
    
    question_data = DRONE_QUESTIONS[current]
    user_answer = message.text
    
    # Проверка ответа
    if user_answer == question_data["options"][question_data["correct"]]:
        score += 1
        await message.answer("✅ <b>Правильно!</b>", parse_mode="HTML")
    else:
        correct_answer = question_data["options"][question_data["correct"]]
        await message.answer(f"❌ <b>Неправильно.</b> Правильный ответ: <b>{correct_answer}</b>", parse_mode="HTML")
    
    # Обновление состояния
    await state.update_data(
        current_question=current + 1,
        score=score
    )
    
    # Задержка перед следующим вопросом
    await asyncio.sleep(0.3)
    await ask_question(message, state)

async def finish_quiz(message: types.Message, state: FSMContext):
    data = await state.get_data()
    score = data.get("score", 0)
    total = data.get("total_questions", len(DRONE_QUESTIONS))
    fio = data.get("fio", "Участник")
    quiz_start_time = data.get("quiz_start_time", "Неизвестно")
    quiz_end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    percentage = (score / total) * 100
    
    # Обновляем лучший результат
    best_score = data.get("best_score", 0)
    if score > best_score:
        await state.update_data(best_score=score)
        best_score = score
    
    # Сохраняем последний результат
    await state.update_data(last_score=f"{score}/{total}")
    
    # Определяем оценку
    if percentage >= 90:
        grade = "Отлично! 🏆"
        grade_emoji = "🎖️"
    elif percentage >= 70:
        grade = "Хорошо! 👍"
        grade_emoji = "⭐"
    elif percentage >= 50:
        grade = "Удовлетворительно 👌"
        grade_emoji = "✅"
    else:
        grade = "Нужно подучить теорию 📚"
        grade_emoji = "📖"
    
    # Удаляем клавиатуру
    remove_keyboard = types.ReplyKeyboardRemove()

    
    await message.answer(
        f"🎉 <b>ВИКТОРИНА ЗАВЕРШЕНА!</b> {grade_emoji}\n\n"
        f"👤 <b>Участник:</b> {fio}\n"
        f"📅 <b>Начало:</b> {quiz_start_time}\n"
        f"📅 <b>Окончание:</b> {quiz_end_time}\n\n"
        f"📊 <b>Ваш результат:</b> {score}/{total}\n"
        f"📈 <b>Процент правильных ответов:</b> {percentage:.1f}%\n"
        f"🏆 <b>Оценка:</b> {grade}\n\n"
        f"Используйте /quiz чтобы начать заново!\n"
        f"Или /profile чтобы посмотреть свой профиль.",
        reply_markup=remove_keyboard,
        parse_mode="HTML"
    )
    await state.set_state(UserState.waiting_for_start)

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "🆘 <b>Список команд:</b>\n\n"
        "/start - Регистрация и ввод ФИО\n"
        "/quiz - Начать викторину (50 вопросов)\n"
        "/profile - Посмотреть свой профиль\n"
        "/help - Показать это сообщение\n"
        "/cancel - Отменить текущее действие\n\n"
        "📚 <b>О викторине:</b>\n"
        "• 50 вопросов о дронах\n"
        "• 3 варианта ответа на каждый вопрос\n"
        "• Результаты сохраняются\n"
        "• Можно проходить многократно",
        parse_mode="HTML"
    )

@dp.message(Command("cancel"))
async def cmd_cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    
    if current_state is None:
        await message.answer("Нет активных действий для отмены.")
        return
    
    await state.clear()
    await message.answer(
        "Действие отменено. Используйте /start для регистрации или /quiz для начала викторины.",
        reply_markup=types.ReplyKeyboardRemove()
    )

@dp.message()
async def handle_other_messages(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    
    if current_state == UserState.waiting_for_fio:
        await process_fio(message, state)
    elif current_state == UserState.waiting_for_start:
        await message.answer(
            "Используйте /quiz чтобы начать викторину!\n"
            "Или /help для списка команд."
        )
    else:
        await message.answer(
            "Привет! Используйте /start для регистрации или /help для списка команд."
        )

# Запуск бота
async def main():
    print("🚀 Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
