package main

import (
	"fmt"
	"learn-nn/train"

	"github.com/fxsjy/gonn/gonn"
)

func GetResult(output []float64) string {
	max := -99999.0
	pos := -1
	// Ищем позицию нейрона с самым большим весом.
	for i, value := range output {
		if value > max {
			max = value
			pos = i
		}
	}

	// Теперь, в зависимости от позиции, возвращаем решение.
	switch pos {
	case 0:
		return "Атаковать"
	case 1:
		return "Красться"
	case 2:
		return "Убегать"
	case 3:
		return "Ничего не делать"
	}
	return ""
}

func main() {
	train.CreateNN()
	// Загружем НС из файла.
	nn := gonn.LoadNN("gonn")

	// Записываем значения в переменные:
	// hp - здоровье (0.1 - 1.0)
	// weapon - наличие оружия (0 - нет, 1 - есть)
	// enemyCount - количество врагов
	var hp float64 = 0.7
	var weapon float64 = 1.0
	var enemyCount float64 = 1.0

	// Получаем ответ от НС (массив весов)
	out := nn.Forward([]float64{hp, weapon, enemyCount})
	// Печатаем ответ на экран.
	fmt.Println(GetResult(out))
}
