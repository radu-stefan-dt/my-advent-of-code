import Data.Char (isDigit)
import qualified Data.Map as Map
import System.Environment (getArgs)
import Text.Regex.TDFA

main :: IO ()
main = do
  (inputFile : _) <- getArgs
  input <- readFile inputFile
  let gridWidth = length $ head $ lines input
      gridHeight = length $ lines input
      grid = toGrid $ lines input
      partNumbers = numberSegments $ lines input
      validParts = filter (isPartValid gridWidth gridHeight grid) partNumbers
  print validParts

isPartValid :: Int -> Int -> Grid -> Segment -> Bool
isPartValid gw gh g s = not (any isSymbol (surroundingPoints s))
  where
    isSymbol p = maybe False (\c -> c /= '.' && (not . isDigit) c) (Map.lookup p g)
    surroundingPoints (Segment (Point x1 y1) (Point x2 y2)) =
      [ Point x y
        | x <- [x1 - 1 .. x2 + 1],
          x >= 0,
          x < gw,
          y <- [y1 - 1 .. y2 + 1],
          y >= 0,
          y < gh
      ]

toGrid :: [String] -> Grid
toGrid xs =
  Map.fromList [(Point x y, c) | (y, row) <- zip [0 ..] xs, (x, c) <- zip [0 ..] row]


numberSegments :: [String] -> [Segment]
numberSegments xs = concatMap (uncurry numberMatches) (zip [0 ..] xs)

numberMatches :: Int -> String -> [Segment]
numberMatches n xs = [Segment (Point n i) (Point n (i + j - 1)) | (i, j) <- matches]
  where
    matches = getAllMatches (xs =~ digitRe) :: [(Int, Int)]
    digitRe = "[0-9]+" :: String
    

type Grid = Map.Map Point Char

data Point = Point Int Int deriving (Show, Eq, Ord)

data Segment = Segment Point Point deriving (Show)