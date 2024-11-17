class Template:
    START = "Вас вітає Flagrate Movie Bot! Введіть /search [назва фільму] для пошуку фільму."
    START_DB_ERROR = "💔 Щось пішло не так. Спробуйте команду /start ще раз пізніше\nФункціонал обраних фільмів тимчасово недоступний"
    
    ERROR = "💔 Щось пішло не так. Спробуйте пізніше"

    SEARCH_NOT_FOUND = (
        "💔 Нічого не знайдено. Спробуйте інший пошуковий запит або англійську мову"
    )
    SEARCH_NO_ARGS = "💔 Неправильне використання команди, введіть параметри пошуку"
    MORE_RESULTS_SHOW = "Буде показано ще результатів пошуку: "
    MORE_RESULTS_SHOWN = "Показано ще варіантів: "

    FAVORITES_ADD_BUTTON = "❤️ Додати до обраного"
    FAVORITES_REMOVE_BUTTON = "❌ Видалити з обраного"

    FAVORITES_ADDED_ALERT = "✅ Фільм додано до обраного"
    FAVORITES_REMOVED_ALERT = "❌ Фільм видалено з обраного"

    FAVORITES_SHOW_BUTTON = "❤️ Обрані фільми"
    FAVORITES_EMPTY = "😞 У Вас поки немає обраних фільмів"
    FAVORITES_CLEAR_BUTTON = "🗑️ Очистити обрані фільми"

    SEARCH_BUTTON = "🔎 Пошук фільму"
    TRENDING_BUTTON = "🔥 Популярні фільми"
    HELP_BUTTON = "💡 Допомога"
    MORE_RESULTS_BUTTON = "🔎 Показати інші варіанти"

    FSM_SEARCH_START = "🔎 Пошук фільму. Відправте мені назву фільму"
    FSM_FAVORITES_ACTIONS = "Ви можете очистити цей список"

    ACCESS_DENIED = "🚫 Цю команду можуть використовувати лише адміністратори"

    CLEAR_CONFIRM = "❗️ Ви впевнені, що хочете очистити список обраних фільмів?\n\nЦю дію неможливо буде повернути"
    CLEAR_YES_BUTTON = "✅ Так, очистити"
    CLEAR_NO_BUTTON = "🚫 Ні, не очищати"
    CLEAR_FINISHED = "🗑️ Список обраних фільмів очищено"
    CLEAR_CANCELLED = "✅ Список обраних фільмів залишено без змін"
    
    HELP = "Перелік команд:\n/search - пошук фільму\n/favorites - список обраних фільмів\n/trending - популярні зараз фільми\n/clear_favorites - очистити список обраних фільмів\n/help - допомога"
