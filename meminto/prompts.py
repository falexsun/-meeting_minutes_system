CONTEXT = """
You are a team assistant and support the team with its daily work.
"""

CONTEXT_RUSSIAN = """
Вы - помощник команды и помогаете команде в её повседневной работе.
"""

INSTRUCTIONS_CREATE_MEETING_MINUTES = """
Your task is to create the meeting minutes for the transcript you get handed by the user.
Proceed step-by-step:
1. Read through the text.
2. Extract the goals of the meeting if possible and add them to the minutes under the title **Goals**.
3. Extract all decisions that were discussed and add them to the minutes under the title **Decisions**.
4. Extract tasks that were assigned to a specific person and add them to the minutes under the title **Assigned Tasks**.
5. Under the title **Additional Notes** add those discussion points from the transcript that seem important but didn't
   make it into one of the above categories.
6. Return the final meeting notes to the user.
"""

INSTRUCTIONS_CREATE_MEETING_MINUTES_RUSSIAN = """
Ваша задача - создать протокол совещания на основе расшифровки, которую вам предоставит пользователь.

Используйте следующий ШАБЛОН для оформления протокола:

ПРОТОКОЛ № [___]
расширенного совещания [Название комиссии/рабочей группы]

Дата проведения: [число.месяц.год]
Начало совещания: [чч:мм]
Продолжительность совещания: [___] минут

Председательствующий:
[Должность] – [Инициалы, Фамилия]

Секретарь:
[Инициалы, Фамилия]

Участники совещания:
1.  [Должность] – [Инициалы, Фамилия]
2.  [Должность] – [Инициалы, Фамилия]
...

ПОВЕСТКА ДНЯ:

1.  О [вопрос для обсуждения 1].
    Докладчик: [Должность, Инициалы, Фамилия]

2.  О [вопрос для обсуждения 2].
    Докладчик: [Должность, Инициалы, Фамилия]
...

СЛУШАЛИ:

1.  По первому вопросу повестки дня слушали [Должность, Инициалы, Фамилия докладчика].
    В ходе доклада было отмечено следующее: [Краткое содержание выступления].
    ВЫСТУПИЛИ:
    [Должность, Инициалы, Фамилия]: [Краткое содержание выступления].
    РЕШИЛИ:
    1.1. [Текст решения]. Срок: [дата]. Ответственный: [Должность, Инициалы, Фамилия].

2.  По второму вопросу повестки дня слушали [Должность, Инициалы, Фамилия докладчика].
    В ходе доклада было отмечено следующее: [Краткое содержание выступления].
    РЕШИЛИ:
    2.1. [Текст решения]. Срок: [дата]. Ответственный: [Должность, Инициалы, Фамилия].
...

ИНСТРУКЦИИ ПО ЗАПОЛНЕНИЮ:
1. Проанализируйте расшифровку и извлеките: спикеров (SPEAKER_00, SPEAKER_01 и т.д.), темы обсуждения, решения.
2. Заполните шапку протокола: дату, время (если указаны), участников на основе количества спикеров.
3. Сформируйте повестку дня на основе обсуждаемых тем.
4. В разделе СЛУШАЛИ по каждому пункту повестки укажите:
   - Кто выступал (спикер)
   - Краткое содержание доклада
   - Кто еще выступил по вопросу
   - Какие решения были приняты с указанием сроков и ответственных
5. Если информация отсутствует в расшифровке, оставьте поле [___] для ручного заполнения.
6. Верните протокол в указанном формате.
"""

SELECT_LANGUAGE = "Always respond in "

EXAMPLE_OUTPUT_INTRO = """

Example output:

"""

EXAMPLE_OUTPUT = """
**Goals:**

- Organise a surprise party for Adam.

**Decisions:**

Suprise:
    - Suprise Adam when he comes back home.
    - Everybody hides in the kitchen until Adam enters the flat.
    - When Adam enters the flat everybody sings Happy Birthday.
Party:
    - Afterward there will be a party with music, cake and soft drinks.
    - The Party should not be longer then 11 o'clock as everbody need to work the next day.

**Assigned Tasks:**

    - No task assigned

**Additional Notes:**

    - The idea to hire a clown for the party was dissmissed as to expensive.

"""


INSTRUCTIONS_MERGE_MEETING_MINUTES = """
Your task is to create the meeting minutes for a transcript.
The meeting transcript was to long to be processed at once.
Therefore, the transcript has been split into multiple sections.
For each section individual meeting minutes have been created in a previous step.
You will be handed the different meeting minutes of all transcript sections in chronological order.
Your task is to create the meeting minutes for the whole meeting based on the meeting minutes of the different sections of the transcript.
Return only the final meeting minutes to the user.
"""

INSTRUCTIONS_MERGE_MEETING_MINUTES_RUSSIAN = """
Ваша задача - создать протокол совещания на основе расшифровки.
Расшифровка совещания была слишком длинной для обработки за один раз.
Поэтому расшифровка была разделена на несколько секций.
Для каждой секции на предыдущем этапе были созданы отдельные протоколы.
Вам будут предоставлены различные протоколы всех секций расшифровки в хронологическом порядке.
Ваша задача - создать протокол всего совещания на основе протоколов различных секций расшифровки.
Верните пользователю только итоговый протокол совещания.
"""

EXAMPLE_INPUT_INTRO = """

Example input:

"""

EXAMPLE_INPUT = """
Section 1
**Goals:**

- Organise a surprise party for Adam.

**Decisions:**

    - Suprise Adam when he comes back home.
    - Everybody hides in the kitchen until Adam enters the apartment.
    - When Adam enters the apartment everybody sings Happy Birthday.

**Assigned Tasks:**

SPEAKER_02: Organises the Key to the apartment of Adam.

**Additional Notes:**

    - The idea to hire a clown for the party was dissmissed as to expensive.

Section 2
**Decisions:**

    - Afterward the suprise there will be a party with music, cake and soft drinks.
    - The Party should not be longer then 11 o'clock as everbody need to work the next day.

**Assigned Tasks:**

SPEAKER_01: Buys Drinks
Speaker_02: Organises music
SPEAKER_00: Buys Snacks
Speaker_03: No task assigned

"""

EXAMPLE_OUTPUT_RUSSIAN = """
**Цели:**

- Организовать вечеринку-сюрприз для Адама.

**Решения:**

Сюрприз:
    - Устроить сюрприз Адаму, когда он вернется домой.
    - Все прячутся на кухне, пока Адам не войдет в квартиру.
    - Когда Адам войдет в квартиру, все поют «С днем рождения».
Вечеринка:
    - После сюрприза будет вечеринка с музыкой, тортом и безалкогольными напитками.
    - Вечеринка не должна длиться дольше 11 часов, так как всем нужно работать на следующий день.

**Назначенные задачи:**

    - Задачи не назначены

**Дополнительные заметки:**

    - Идея нанять клоуна для вечеринки была отклонена как слишком дорогая.

"""

EXAMPLE_INPUT_RUSSIAN = """
Секция 1
**Цели:**

- Организовать вечеринку-сюрприз для Адама.

**Решения:**

    - Устроить сюрприз Адаму, когда он вернется домой.
    - Все прячутся на кухне, пока Адам не войдет в квартиру.
    - Когда Адам войдет в квартиру, все поют «С днем рождения».

**Назначенные задачи:**

SPEAKER_02: Организует ключ от квартиры Адама.

**Дополнительные заметки:**

    - Идея нанять клоуна для вечеринки была отклонена как слишком дорогая.

Секция 2
**Решения:**

    - После сюрприза будет вечеринка с музыкой, тортом и безалкогольными напитками.
    - Вечеринка не должна длиться дольше 11 часов, так как всем нужно работать на следующий день.

**Назначенные задачи:**

SPEAKER_01: Покупает напитки
SPEAKER_02: Организует музыку
SPEAKER_00: Покупает закуски
SPEAKER_03: Задачи не назначены

"""
