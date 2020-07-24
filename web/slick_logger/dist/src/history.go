package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"path"
	"path/filepath"
	"strconv"
	"strings"
)

// GET /api/history
func historyHandler(w http.ResponseWriter, r *http.Request) {
	channelID, ok := r.URL.Query()["channel"]
	if !ok || !validateParameter(channelID[0]) {
		http.Error(w, "channel parameter is required", 400)
		return
	}

	users := []User{}
	readJSON("/var/lib/data/users.json", &users)

	dir, _ := strconv.Unquote(channelID[0])

	dir = path.Clean(dir)
	if strings.HasPrefix(dir, "G") {
		http.Error(w, "You cannot view private channels, sorry!", 403)
		return
	}

	messages := []Message{}
	filepath.Walk("/var/lib/data/", func(path string, _ os.FileInfo, _ error) error {
		if strings.HasPrefix(path, "/var/lib/data/"+dir) && strings.HasSuffix(path, ".json") {
			newMessages := []Message{}
			readJSON(path, &newMessages)
			messages = append(messages, newMessages...)
		}
		return nil
	})

	for i, message := range messages {
		// Fill in user info
		for _, user := range users {
			if user.ID == message.UserID {
				messages[i].UserName = user.Name
				messages[i].Icon = user.Profile.Image
				break
			}
		}
	}

	result, _ := json.Marshal(messages)

	w.WriteHeader(http.StatusOK)
	header := w.Header()
	header.Set("Content-type", "application/json")
	fmt.Fprint(w, string(result))
}
