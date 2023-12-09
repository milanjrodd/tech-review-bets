package main

import (
	"encoding/csv"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"strconv"
	"time"
)

func main() {
	var file *os.File

	// Check if data.csv exists
	if _, err := os.Stat("data.csv"); os.IsNotExist(err) {
		// Create a new CSV file
		file, err := os.Create("data.csv")

		if err != nil {
			fmt.Println("Error creating file:", err)
			return
		}
		defer file.Close()

		// Create a CSV writer
		writer := csv.NewWriter(file)
		defer writer.Flush()

		// Write the CSV header
		writer.Write([]string{"match_id", "radiant_team", "dire_team", "radiant_win"})
	} else {
		// Open the CSV file
		file, err = os.OpenFile("data.csv", os.O_RDWR|os.O_APPEND, os.ModeAppend)
		if err != nil {
			fmt.Println("Error opening file:", err)
			return
		}
		defer file.Close()
	}

	writer := csv.NewWriter(file)
	defer writer.Flush()

	// Set initial match ID and request limit
	matchID := getLatestMatchID("data.csv")
	requestLimit := time.Tick(time.Second)
	matchesCounter := 0

	for i := 0; i < 2; i++ {
		fmt.Println("Request #", i+1, "...")
		fmt.Println("Waiting for request limit...")
		<-requestLimit // Wait for the request limit

		// Make a GET request to the API
		var url string
		if matchID == 0 {
			url = "https://api.opendota.com/api/publicMatches"
		} else {
			url = fmt.Sprintf("https://api.opendota.com/api/publicMatches?less_than_match_id=%d", matchID)
		}
		resp, err := http.Get(url)
		if err != nil {
			fmt.Println("Error making request:", err)
			return
		}

		// Read the response body and parse the data
		var matches []Match
		if err := json.NewDecoder(resp.Body).Decode(&matches); err != nil {
			fmt.Println("Error decoding response:", err)
			return
		}

		// Update the match ID
		if len(matches) > 0 {
			matchID = matches[len(matches)-1].MatchID
		}

		fmt.Printf("Successfully fetched %d matches\n", len(matches))
		matchesCounter += len(matches)

		for _, match := range matches {
			writer.Write([]string{strconv.Itoa(match.MatchID), match.RadiantTeam, match.DireTeam, strconv.FormatBool(match.RadiantWin)})
		}

		resp.Body.Close()

		// Break the loop if no more matches are available
		if resp.StatusCode != http.StatusOK {
			break
		}
	}

	fmt.Printf("Matches fetched: %d\nOutput file: data.csv\n", matchesCounter)
}

type Match struct {
	MatchID     int    `json:"match_id"`
	RadiantTeam string `json:"radiant_team"`
	DireTeam    string `json:"dire_team"`
	RadiantWin  bool   `json:"radiant_win"`
}

func getLatestMatchID(filepath string) int {
	file, err := os.Open(filepath)
	if err != nil {
		fmt.Println("Error opening file:", err)
		return 0
	}
	defer file.Close()

	reader := csv.NewReader(file)
	records, err := reader.ReadAll()
	if err != nil {
		fmt.Println("Error reading file:", err)
		return 0
	}

	if len(records) > 1 {
		latestMatchID, _ := strconv.Atoi(records[len(records)-1][0])
		return latestMatchID
	}

	return 0
}
