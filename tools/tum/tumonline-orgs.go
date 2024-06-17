package tum

import (
	"encoding/xml"
	"fmt"
	"io"
	"os"

	"github.com/TUM-Dev/gocast/model"
	"gorm.io/gorm"
)

type Row struct {
	Ebene          int    `xml:"ebene"`
	Nr             int    `xml:"nr"`
	Parent         int    `xml:"parent"`
	ChildCnt       int    `xml:"child_cnt"`
	SortHierarchie int    `xml:"sort_hierarchie"`
	Kennung        string `xml:"kennung"`
	OrgTypName     string `xml:"org_typ_name"`
	OrgGruppeName  string `xml:"org_gruppe_name"`
	NameDe         string `xml:"name_de"`
	NameEn         string `xml:"name_en"`
}

type Data struct {
	Rows []Row `xml:"row"`
}

func LoadTUMOnlineOrgs(db *gorm.DB) {
	// Read TUMOnline XML tree (Reference: https://collab.dvb.bayern/display/tumonlineappdevndoc/orgBaum)
	xmlFile, err := os.Open("./tools/tum/orgBaum.xml")
	if err != nil {
		fmt.Println("Error opening file:", err)
		return
	}
	defer xmlFile.Close()

	byteValue, _ := io.ReadAll(xmlFile)

	var data Data
	xml.Unmarshal(byteValue, &data)

	// Process each row and update/create School records
	for _, row := range data.Rows {
		if row.OrgTypName == "TUM School" {
			var school model.School
			db.FirstOrCreate(&school, model.School{
				OrgId:   fmt.Sprintf("%d", row.Nr),
				OrgType: row.OrgTypName,
				OrgSlug: row.Kennung,
			})

			school.Name = row.NameEn
			school.University = "TUM"

			db.Save(&school)
		}
	}

	logger.Info("TUMOnline orgs loaded.")
}
