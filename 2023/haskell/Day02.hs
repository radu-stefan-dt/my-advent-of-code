{-# LANGUAGE OverloadedStrings #-}

module Day02 where

import Data.Map qualified as Map
import Data.Text (Text, pack, splitOn, unpack)
import System.Environment ( getArgs )

main = do
    (inputFile : _) <- getArgs
    input <- readFile inputFile
    print $ "Part one answer: " ++ show (part1 $ lines input)
    print $ "Part two answer: " ++ show (part2 $ lines input)

part2 :: [String] -> Integer
part2 = sum . map (product . Map.elems . snd . gameInfo)

part1 :: [String] -> Integer
part1 = sum . map (read . unpack . fst) . filter isPossible . map gameInfo

isPossible :: (Text, Map.Map String Integer) -> Bool
isPossible (_, cubes) =
    Map.lookup "red" cubes <= Just 12 &&
    Map.lookup "green" cubes <= Just 13 &&
    Map.lookup "blue" cubes <= Just 14

gameInfo :: String -> (Text, Map.Map String Integer)
gameInfo line = (gameId line, maxCubes line)
  where
    gameId = last . splitOn " " . head . splitGame . pack
    maxCubes = Map.fromListWith max . cubes
    cubes = concatMap (map cubeTuple . splitOn ", ") . rounds
    rounds = splitOn "; " . last . splitGame . pack
    cubeTuple = (\[x, y] -> (unpack y, read $ unpack x)) . splitOn " "
    splitGame = splitOn ": "