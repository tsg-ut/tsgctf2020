package main

import (
	"encoding/json"
	"fmt"
	"net/http"
)

// GET /api/channels
func channelsHandler(w http.ResponseWriter, r *http.Request) {
	channels := []Channel{}
	readJSON("/var/lib/data/channels.json", &channels)

	result, _ := json.Marshal(channels)

	w.WriteHeader(http.StatusOK)
	header := w.Header()
	header.Set("Content-type", "application/json")
	fmt.Fprint(w, string(result))
}
