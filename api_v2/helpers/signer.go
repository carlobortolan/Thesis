// Package helpers provides helper functions for parsing models to protobuf representations.
package helpers

import (
	"errors"
	"net/http"

	e "github.com/TUM-Dev/gocast/api_v2/errors"
	"github.com/TUM-Dev/gocast/model"
	"github.com/TUM-Dev/gocast/tools"
	"gorm.io/gorm"
)

func SignStream(s *model.Stream, c *model.Course, uID uint) ([]model.DownloadableVod, error) {
	if err := tools.SetSignedPlaylists(s, &model.User{
		Model: gorm.Model{ID: uID},
	}, c.DownloadsEnabled); err != nil {
		return nil, e.WithStatus(http.StatusInternalServerError, errors.New("can't sign stream"))
	}

	if c.DownloadsEnabled && s.IsDownloadable() {
		return s.GetVodFiles(), nil
	}
	return nil, nil
}
