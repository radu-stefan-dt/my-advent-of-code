module Day01 where

import Data.Char (isDigit)
import Data.List (inits, isInfixOf, tails)
import Data.Map qualified as Map
import System.Environment (getArgs)

main = do
  (inputFile : _) <- getArgs
  input <- readFile inputFile
  print $ "Part one answer: " ++ show (sum (map toNum $ lines input))
  print $ "Part two answer: " ++ show (sum (map toNum' $ lines input))

toNum' :: String -> Integer
toNum' xs = numStrToInt (firstNumStr xs) * 10 + numStrToInt (lastNumStr xs)
  where
    firstNumStr xs = head [x | x <- map substr (inits xs), x /= ""]
    lastNumStr xs = head [x | x <- map substr (reverse $ tails xs), x /= ""]
    numStrToInt x = case Map.lookup x numMap of
      Just n -> n
      Nothing -> read x

substr :: String -> String
substr xs = if null matches then "" else head matches
  where
    matches = filter (`isInfixOf` xs) numberStrings
    numberStrings = map show [1 .. 9] ++ Map.keys numMap

numMap :: Map.Map String Integer
numMap = Map.fromList [("one", 1), ("two", 2), ("three", 3), ("four", 4), ("five", 5), ("six", 6), ("seven", 7), ("eight", 8), ("nine", 9)]

toNum :: String -> Integer
toNum xs
  | null $ digits xs = 0
  | otherwise = read $ head (digits xs) : [last (digits xs)]
  where
    digits = filter isDigit
