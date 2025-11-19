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
Действуйте пошагово:
1. Прочитайте весь текст.
2. Извлеките цели совещания, если это возможно, и добавьте их в протокол под заголовком **Цели**.
3. Извлеките все принятые решения и добавьте их в протокол под заголовком **Решения**.
4. Извлеките задачи, которые были назначены конкретным лицам, и добавьте их в протокол под заголовком **Назначенные задачи**.
5. Под заголовком **Дополнительные заметки** добавьте те моменты обсуждения из расшифровки, которые кажутся важными,
   но не попали ни в одну из вышеперечисленных категорий.
6. Верните итоговый протокол совещания пользователю.
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
