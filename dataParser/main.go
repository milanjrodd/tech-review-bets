package main

import (
	"encoding/csv"
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"net/http"
	"os"
	"slices"
	"strconv"
	"strings"
	"time"
)

const (
	filePath = "matches.csv"
	apiURL   = "https://api.opendota.com/api/publicMatches"
)

// TODO: Add heroStats parser
// https://api.opendota.com/api/heroStats

func main() {
	requestsLimitCounter := flag.Int("req", 100, "Number of requests to make")
	dataRowsLimitCounter := flag.Int("rows", -1, "Number of data rows to fetch")
	flag.Parse()

	file, err := openOrCreateFile(filePath)
	if err != nil {
		fmt.Println("Error opening or creating file:", err)
		return
	}
	defer file.Close()

	writer := csv.NewWriter(file)
	defer writer.Flush()

	matchID := getLatestMatchID(file)
	requestLimit := time.Tick(time.Second)
	matchesCounter := 0

	loopBreaker := *requestsLimitCounter
	if *dataRowsLimitCounter > *requestsLimitCounter {
		loopBreaker = *dataRowsLimitCounter
	}

	for i := 0; i < loopBreaker; i++ {
		if *dataRowsLimitCounter >= 0 && matchesCounter >= *dataRowsLimitCounter {
			break
		}

		fmt.Println("\nRequest #", i+1, "...")
		fmt.Println("Waiting for request limit...")
		<-requestLimit // Wait for the request limit

		url := apiURL
		if matchID != 0 {
			url = fmt.Sprintf("%s?less_than_match_id=%d", apiURL, matchID)
		}

		resp, err := http.Get(url)
		if err != nil {
			fmt.Println("Error making request:", err)
			return
		}
		defer resp.Body.Close()

		var matches []Match
		if err := json.NewDecoder(resp.Body).Decode(&matches); err != nil {
			fmt.Println("Error decoding response:", err)
			return
		}

		if len(matches) > 0 {
			matchID = matches[len(matches)-1].MatchID
		}

		fmt.Printf("Fetched %d matches\n", len(matches))

		_matchesCounter := 0

		for _, match := range matches {
			invalidGameModes := []int{22, 1}
			invalidLobbyTypes := []int{2, 5, 6, 7}

			hasNotTenPlayers := len(strings.Split(match.RadiantTeam, ",")) != 5 || len(strings.Split(match.DireTeam, ",")) != 5
			isIncorrectGameMode := !slices.Contains(invalidGameModes, match.GameMode)
			isIncorrectLobbyType := !slices.Contains(invalidLobbyTypes, match.LobbyType)
			isIncorrectRankTier := match.AvgRankTier < 10 || match.AvgRankTier > 89

			if hasNotTenPlayers || isIncorrectGameMode || isIncorrectLobbyType || isIncorrectRankTier {
				continue
			}
			_matchesCounter += 1

			writer.Write([]string{
				strconv.Itoa(match.MatchID),
				strconv.Itoa(match.MatchSeqNum),
				strconv.FormatBool(match.RadiantWin),
				strconv.Itoa(match.StartTime),
				strconv.Itoa(match.Duration),
				fmt.Sprintf("%v", match.AvgMmr),
				fmt.Sprintf("%v", match.NumMmr),
				strconv.Itoa(match.LobbyType),
				strconv.Itoa(match.GameMode),
				strconv.Itoa(match.AvgRankTier),
				strconv.Itoa(match.NumRankTier),
				strconv.Itoa(match.Cluster),
				match.RadiantTeam,
				match.DireTeam,
			})
			writer.Flush() // Flush the writer to write the data immediately
		}

		fmt.Printf("Added %d matches\n", _matchesCounter)
		matchesCounter += _matchesCounter
		fmt.Printf("Total matches: %d\n", matchesCounter)

		if resp.StatusCode != http.StatusOK {
			break
		}
	}

	fmt.Printf("\nMatches added: %d\nOutput file: %s\n", matchesCounter, filePath)
}

func openOrCreateFile(filePath string) (*os.File, error) {
	file, err := os.OpenFile(filePath, os.O_RDWR|os.O_APPEND, os.ModeAppend)
	if err != nil {
		if os.IsNotExist(err) {
			file, err = os.Create(filePath)
			if err != nil {
				return nil, fmt.Errorf("error creating file: %w", err)
			}

			writer := csv.NewWriter(file)
			defer writer.Flush()

			writer.Write([]string{
				"match_id",
				"match_seq_num",
				"radiant_win",
				"start_time",
				"duration",
				"avg_mmr",
				"num_mmr",
				"lobby_type",
				"game_mode",
				"avg_rank_tier",
				"num_rank_tier",
				"cluster",
				"radiant_team",
				"dire_team",
			})
			writer.Flush() // Flush the writer to write the data immediately
		} else {
			return nil, fmt.Errorf("error opening file: %w", err)
		}
	}
	return file, nil
}

type Main []Match

type Match struct {
	MatchID     int         `json:"match_id"`
	MatchSeqNum int         `json:"match_seq_num"`
	RadiantWin  bool        `json:"radiant_win"`
	StartTime   int         `json:"start_time"`
	Duration    int         `json:"duration"`
	AvgMmr      interface{} `json:"avg_mmr"`
	NumMmr      interface{} `json:"num_mmr"`
	LobbyType   int         `json:"lobby_type"`
	GameMode    int         `json:"game_mode"`
	AvgRankTier int         `json:"avg_rank_tier"`
	NumRankTier int         `json:"num_rank_tier"`
	Cluster     int         `json:"cluster"`
	RadiantTeam string      `json:"radiant_team"`
	DireTeam    string      `json:"dire_team"`
}

func getLatestMatchID(file io.Reader) int {
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
