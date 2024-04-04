package input

import "os"

func ReadPuzzle(file string) string {
	data, err := os.ReadFile(file)
	if err != nil {
		panic(err)
	}

	return string(data)
}
