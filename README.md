# Evaluating Pitcher Effectiveness with a Custom Sabermetric Index

Based on this project, a pitcher's effectiveness is defined as their performance relative to the league average, highlighting their true skill by combining the advanced metrics of SIERA and K-BB%.

In order to do this, I made my own custom efficiency metric using K-BB% and SIERA. I first standardized the two stats, since one is a rate stat and one is a performance stat, by calculating the Z-score of each for every pitcher in a given year, in this case 2024 and 2025. Then I weighted SIERA 60% and K-BB% 40% and added them together to form a single index. I then scaled this index so that 100 represents the league average, allowing for easy comparison of performance across different seasons.



