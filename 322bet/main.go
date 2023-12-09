package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"strconv"
	"strings"

	"github.com/fxsjy/gonn/gonn"
)

const (
	iterations     = 1000
	hiddenNeurons  = 14
	numberOfHeroes = 138
	filePathTrain  = "../dataParser/matches.csv"
	filePathTest   = "matches-test.csv"
)

func train() {
	file, err := os.Open(filePathTrain)
	if err != nil {
		fmt.Println("Error opening file:", err)
		return
	}
	defer file.Close()

	reader := csv.NewReader(file)
	reader.FieldsPerRecord = -1
	records, err := reader.ReadAll()
	if err != nil {
		fmt.Println("Error reading CSV file:", err)
		return
	}

	// Создаём НС со входными нейронами (столько же входных параметров),
	// 16 скрытыми нейронами и
	// 2 выходными нейронами (столько же вариантов ответа)
	nn := gonn.DefaultNetwork(numberOfHeroes*2, hiddenNeurons, 1, false)

	// Теперь создаём "входы" - те данные, на основе которых будет обучаться НС
	input := [][]float64{}

	for r, record := range records {
		if r == 0 {
			continue
		}

		matchInput := []float64{}

		for j := 1; j < 3; j++ {
			var heroesIdMask [numberOfHeroes]float64

			for i := 0; i < numberOfHeroes; i++ {
				heroesIdMask[i] = 0
			}

			heroes := strings.Split(record[j], ",")

			for i := range heroes {
				heroID, _ := strconv.Atoi(heroes[i])

				if heroID > 0 {
					heroesIdMask[heroID-1] = 1
				}
			}

			matchInput = append(matchInput, heroesIdMask[:]...)
		}

		input = append(input, matchInput)
	}

	// Теперь создаём "выходы" - те данные, которые должны получиться на выходе
	output := [][]float64{}

	for _, record := range records {
		matchOutput := []float64{}

		if record[3] == "true" {
			matchOutput = append(matchOutput, 1)
		} else {
			matchOutput = append(matchOutput, 0)
		}

		output = append(output, matchOutput)
	}

	// Начинаем обучать нашу НС.
	// Количество итераций - 100000
	fmt.Printf("Training started with %d iterations and %d hidden neurons\n", iterations, hiddenNeurons)
	nn.Train(input, output, iterations)

	// Сохраняем готовую НС в файл.
	gonn.DumpNN("gonn", nn)
}

func test() {
	// Загружем НС из файла.
	nn := gonn.LoadNN("gonn")

	file, err := os.Open(filePathTest)
	if err != nil {
		fmt.Println("Error opening file:", err)
		return
	}
	defer file.Close()

	reader := csv.NewReader(file)
	reader.FieldsPerRecord = -1
	records, err := reader.ReadAll()
	if err != nil {
		fmt.Println("Error reading CSV file:", err)
		return
	}

	errorCounter := 0

	for r, record := range records {
		if r == 0 {
			continue
		}

		matchInput := []float64{}

		for j := 1; j < 3; j++ {
			var heroesIdMask [numberOfHeroes]float64

			for i := 0; i < numberOfHeroes; i++ {
				heroesIdMask[i] = 0
			}

			heroes := strings.Split(record[j], ",")

			for i := range heroes {
				heroID, _ := strconv.Atoi(heroes[i])

				if heroID > 0 {
					heroesIdMask[heroID-1] = 1
				}
			}

			matchInput = append(matchInput, heroesIdMask[:]...)
		}

		out := nn.Forward(matchInput)
		predictedResult := GetResult(out)

		parsedResult, _ := strconv.ParseBool(record[3])
		realResult := ""
		if parsedResult {
			realResult = "Radiant"
		} else {
			realResult = "Dire"
		}

		if predictedResult != realResult {
			errorCounter++
		}

		// fmt.Printf("%s - %s\n", predictedResult, realResult)
	}

	fmt.Printf("Success rate: %f\n", 1-float64(errorCounter)/float64(len(records)))
}

func GetResult(output []float64) string {
	max := -99999.0
	// Ищем позицию нейрона с самым большим весом.
	for _, value := range output {
		if value > max {
			max = value
		}

		if value > 0.5 {
			return "Radiant"
		} else {
			return "Dire"
		}
	}

	return ""
}

func main() {
	train()
	test()
}
