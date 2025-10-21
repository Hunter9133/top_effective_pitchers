# My Project

This small script will find and visualize the 20 most efficient QUALIFIED (pitched 162 or more innings) pitchers 
in the 2025 MLB regular season through the use of the pybaseball library. 
Efficiency is defined as taking on a large workload while maintaining high effectiveness.
Pitchers who can work deep into games while keeping runs off the board will be 
ranked the highest. 

A simple efficiency score metric will be defined as:
((K% - BB%) x IP) / SIERA

