package main

import (
	"encoding/json"
	"io/ioutil"
	"net/http"
	"net/http/cgi"
	"os"
	"regexp"
)

// User represents slack user.
type User struct {
	ID      string `json:"id"`
	Name    string `json:"name"`
	Profile struct {
		Image string `json:"image_48"`
	} `json:"profile"`
}

// Channel represents slack channel.
type Channel struct {
	ID        string `json:"id"`
	Name      string `json:"name"`
	IsPrivate bool   `json:"is_private"`
}

// Message represents slack message.
type Message struct {
	Text      string `json:"text"`
	UserID    string `json:"user"`
	UserName  string `json:"username"`
	Icon      string `json:"icon"`
	Timestamp string `json:"ts"`
}

func readJSON(path string, v interface{}) error {
	file, err := os.Open(path)
	if err != nil {
		return err
	}

	bytes, err := ioutil.ReadAll(file)
	if err != nil {
		return err
	}

	if err = json.Unmarshal(bytes, v); err != nil {
		return err
	}

	return nil
}

func validateParameter(channelID string) bool {
	re, _ := regexp.Compile("^\".+\"$")
	if !re.MatchString(channelID) {
		return false
	}
	return true
}

func main() {
	http.HandleFunc("/api/history", historyHandler)
	http.HandleFunc("/api/search", searchHandler)
	http.HandleFunc("/api/channels", channelsHandler)

	err := cgi.Serve(nil)
	if err != nil {
		panic(err)
	}
}
