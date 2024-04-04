package main

import (
	"aoc-2023-go/internal/input"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	data := input.ReadPuzzle(os.Args[1])
	fmt.Printf("Part 1 answer: %d\n", sum(data, firstDigit))
	fmt.Printf("Part 2 answer: %d\n", sum(data, firstDigitOrWord))
}

func sum(input string, f func(string) int) int {
	total := 0

	for _, line := range strings.Split(input, "\n") {
		for i := 0; i < len(line); i++ {
			if d := f(line[i:]); d > 0 {
				total += d * 10
				break
			}
		}
		for i := len(line) - 1; i >= 0; i-- {
			if d := f(line[i:]); d > 0 {
				total += d
				break
			}
		}
	}
	return total
}

func firstDigit(s string) int {
	if s[0] >= '0' && s[0] <= '9' {
		val, _ := strconv.Atoi(string(s[0]))
		return val
	}
	return 0
}

func firstDigitOrWord(s string) int {
	if d := firstDigit(s); d > 0 {
		return d
	}
	words := [9]string{"one", "two", "three", "four", "five", "six", "seven", "eight", "nine"}
	for i, w := range words {
		if strings.HasPrefix(s, w) {
			return i + 1
		}
	}
	return 0
}
