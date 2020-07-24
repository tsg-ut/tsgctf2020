package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"path/filepath"
	"regexp"
	"strconv"
	"strings"
)

// GET /api/search
func searchHandler(w http.ResponseWriter, r *http.Request) {
	channelID, ok := r.URL.Query()["channel"]
	if !ok || !validateParameter(channelID[0]) {
		http.Error(w, "channel parameter is required", 400)
		return
	}

	queries, ok := r.URL.Query()["q"]
	if !ok || !validateParameter(queries[0]) {
		http.Error(w, "q parameter is required", 400)
		return
	}

	users := []User{}
	readJSON("/var/lib/data/users.json", &users)

	dir, _ := strconv.Unquote(channelID[0])
	query, _ := strconv.Unquote(queries[0])

	if strings.HasPrefix(dir, "G") {
		http.Error(w, "You cannot view private channels, sorry!", 403)
		return
	}

	re, _ := regexp.Compile("(?i)" + query)

	messages := []Message{}
	filepath.Walk("/var/lib/data/", func(path string, _ os.FileInfo, _ error) error {
		if strings.HasPrefix(path, "/var/lib/data/"+dir) && strings.HasSuffix(path, ".json") {
			newMessages := []Message{}
			readJSON(path, &newMessages)
			for _, message := range newMessages {
				if re.MatchString(message.Text) {
					// Fill in user info
					for _, user := range users {
						if user.ID == message.UserID {
							messages = append(messages, Message{
								Text:      re.ReplaceAllString(message.Text, "<em>$0</em>"),
								UserID:    message.UserID,
								UserName:  user.Name,
								Icon:      user.Profile.Image,
								Timestamp: message.Timestamp,
							})
							break
						}
					}
				}
			}
		}
		return nil
	})

	result, _ := json.Marshal(messages)

	w.WriteHeader(http.StatusOK)
	header := w.Header()
	header.Set("Content-type", "application/json")
	fmt.Fprint(w, string(result))
}
