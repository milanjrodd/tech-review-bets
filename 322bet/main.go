package main

import (
	"github.com/fxsjy/gonn/gonn"
)

func CreateNN() {
	// Создаём НС с 3 входными нейронами (столько же входных параметров),
	// 16 скрытыми нейронами и
	// 4 выходными нейронами (столько же вариантов ответа)
	nn := gonn.DefaultNetwork(3, 16, 4, false)

	// Создаём массив входящих параметров:
	// 1 параметр - количество здоровья (0.1 - 1.0)
	// 2 параметр - наличие оружия (0 - нет, 1 - есть)
	// 3 параметр - количество врагов
	input := [][]float64{
		{0.5, 1, 1}, {0.9, 1, 2}, {0.8, 0, 1},
		{0.3, 1, 1}, {0.6, 1, 2}, {0.4, 0, 1},
		{0.9, 1, 7}, {0.6, 1, 4}, {0.1, 0, 1},
		{0.6, 1, 0}, {1, 0, 0}}

	// Теперь создаём "цели" - те результаты, которые нужно получить
	target := [][]float64{
		{1, 0, 0, 0}, {1, 0, 0, 0}, {1, 0, 0, 0},
		{0, 1, 0, 0}, {0, 1, 0, 0}, {0, 1, 0, 0},
		{0, 0, 1, 0}, {0, 0, 1, 0}, {0, 0, 1, 0},
		{0, 0, 0, 1}, {0, 0, 0, 1}}

	// Начинаем обучать нашу НС.
	// Количество итераций - 100000
	nn.Train(input, target, 100000)

	// Сохраняем готовую НС в файл.
	gonn.DumpNN("gonn", nn)
}
