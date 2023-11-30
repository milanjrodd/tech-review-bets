# ТЕХ РАЗБОР: СТАВКИ

Этот репозиторий предназначен для исследования ставок на события.
Спонсор темы - WINLINE

### Книги для изучения

- хью баркер - математика на миллион долларов

### План на исследование

- Определить цель
- Поставить ограничения
- Что такое ставка

> Теория Вероятности — раздел математики, изучающий случайные события, случайные величины, их свойства и операции над ними.

> Математически случайное событие — подмножество пространства элементарных исходов случайного эксперимента.

> Ставка у букмекера - это интеллектуальное пари между игроком и букмекером: игрок делает свой прогноз на спортивное событие и ставит деньги на то, что этот прогноз окажется верным. При верной ставке он возвращает себе эти деньги с прибылью, при проигранной, соответственно, проигрывает их.

> Коэффициент — это главная характеристика любой ставки у букмекера, потому что от него зависит размер потенциального выигрыша. Как букмекеры рассчитывают котировки пари, какие факторы влияют на их величину, и как найти контору с самыми выгодными кэфами?

> Принимать во внимание результаты очных противостояний при анализе матчей нужно весьма сдержанно. Важнее нынешнее состояние команд, а не игры между ними много лет назад. Когда же некоторые прогнозисты в основу прогноза ставят лишь историю очных противостояний — это вызывает недоумение.

> Ваша свободная воля. Творческий процесс по выбору матчей для ставок и самих ставок на конкретные исходы. Если определять матчи не выборочно, а все подряд, то статистика будет работать точнее!

> Предположение необходимо выносить холодно, по единой системе и модели.

> Стратегия с фиксированными ставками и вероятностью выигрыша в 51% не актуальна, так как имеющиеся коэффициенты не позволят быть в плюсе при таком проценте. Либо правильность модели должна быть больше 67% при минимальном коэффициенте в 1.5, либо необходимо грамотно управлять банком.

> Существует стратегия определения вероятности события по коэффициентам букмекера. Такое себе.

> Раз с нарастанием серии проигрышей повышается вероятность выигрыша — повышайте ставки в геометрической прогрессии. И будет счастье… для букмекера.

> В картах вероятность непрокнувшего события возрастает с каждой картой вытащенной из колоды. В футболе между разными матчами это не работает. Но в доте между разными картами это может работать (аналогом в футболе это было бы ситуацией в которой второй гол имел бы вероятность 100 процентов, но неизвестно какая команда бы его забила).

### Формула для расчета мат. ожидания

Для грамотного управления банком необходимо применять формулу рассчета математического ожидания

> (Вероятность выигрыша) х (сумму потенциального выигрыша по текущему пари) – (вероятность проигрыша) х (сумму потенциального проигрыша по текущему пари).

Какой бы выверенной ни была формула теории вероятности в ставках на футбол, хоккей, теннис или другой вид спорта, не все так просто. Как мы уже знаем, коэффициент 1.2 свидетельствует о том, что в 83 из 100 случаев событие случится. Однако, когда ставка окажется плюсовой, а когда минусовой на дистанции – непонятно.

### Формула рассчета дисперсии

> Дисперсией принято называть отклонение результатов игры от усредненных показателей, которые должны учитываться в используемой математической модели.

> (1 – 1 / букмекерский коэффициент) в степени S (количество минусовых ставок подряд).

## Математические стратегии ставок на спорт

Применение математического расчета в спортивных ставках позволяет не только выбрать событие с повышенной вероятностью выигрыша, но и увеличить игровой банк за счет различных финансовых стратегий.

> Флэт – пари с фиксированным размером ставки. Это самой простой и самый популярный способ распределения игрового банка, который позволяет как минимум не остаться с нулем за несколько дней. Ставя на каждый исход по 3-5% от начального банка и угадывая не менее 51% от всех пари с коэффициентом не ниже 2.0, беттер будет в плюсе. Незначительно, но в плюсе.

Эта стратегия не принесет огромных выигрышей, но «научит» правильно подбирать события и грамотно анализировать возможные исходы с минимальными рисками «слива» банкролла.

> Система Мартингейл – еще одна математическая стратегия, основанная на двукратном увеличении суммы ставки при неудачном исходе. При этом котировки на интересующий исход должны быть равны или выше отметки 2.0. В противном случае прибыль от выигранной ставки не сможет перекрыть предыдущие минусы.

Эта математическая стратегия размещения ставок на спорт является довольно рискованной, особенно если не учитывать дисперсию. При затяжной серии неудач игроку может не хватить оставшихся на счету денег для размещения следующей ставки или букмекер может отказать в заключении сделки.

На основе системы Мартингейл была создана стратегия игры «догоном».

Стратегия Д’Аламбера напоминает систему Мартингейла. Суть стратегии следующая: при проигрыше ставки сумма следующего пари увеличивается на единицу, а при выигрыше она уменьшается на это значение.

Если первая ставка равна 1 000 рублей, а коэффициент 2.2, то:

- При выигрыше чистая прибыль составит 1 200 рублей.
- Если ставка не выиграет, то сумма следующего пари возрастет до 2 000 рублей. При удачном исходе выплата составит 4 400, что компенсирует предыдущую неудачу и увеличит игровой банк. Размер следующей ставки должен быть равен 1 000 рублей.

Используя эту стратегию, можно как минимум оставаться в небольшом плюсе на дистанции.

Игроки используют теорию вероятности в ставках на настольный теннис, баскетбол, киберспорт и прочие виды спорта, даже не осознавая этого факта. Отслеживание изменений букмекерских котировок, изучение текущей формы соперников, анализ предыдущих игр – все это и есть математическое ожидание. И если все подсчеты сделаны правильно, вероятность выигрыша будет выше. Как минимум математически.
