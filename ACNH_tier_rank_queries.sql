/* Average Rank by Species */
SELECT SPECIES, AVG(villager_rank) as "Average_Rank"
FROM acnh_villagers
GROUP BY SPECIES
ORDER BY AVG(villager_rank) ASC;

/* Average Rank by Personality */
SELECT Personality, AVG(villager_rank) as "Average_Rank"
FROM acnh_villagers
GROUP BY Personality
ORDER BY AVG(villager_rank) ASC;

/* Average Rank By Gender */
SELECT Gender, AVG(villager_rank) as "Average_Rank"
FROM acnh_villagers
GROUP BY Gender
ORDER BY AVG(villager_rank) ASC;



/* Average Tier by Species */
SELECT SPECIES, AVG(villager_tier_num) as Average_Tier
FROM acnh_villagers
GROUP BY SPECIES
ORDER BY AVG(villager_tier_num) ASC;

/* Average Tier by Personality */
SELECT Personality, AVG(villager_tier_num) as Average_Tier
FROM acnh_villagers
GROUP BY Personality
ORDER BY AVG(villager_tier_num) ASC;

/* Average Tier By Gender */
SELECT Gender, AVG(villager_tier_num) as Average_Tier
FROM acnh_villagers
GROUP BY Gender
ORDER BY AVG(villager_tier_num) ASC;



/* Tiers by Personality Type */

SELECT Personality, villager_tier_num as Tier,
count(Personality)/sum(count(Personality)) over (PARTITION BY villager_tier_num) as Percent
FROM acnh_villagers
GROUP BY Personality, Tier;

/* Tiers by Species */

SELECT Species, villager_tier_num as Tier,
count(Species)/sum(count(Species)) over (PARTITION BY villager_tier_num) as Percent
FROM acnh_villagers
GROUP BY Species, Tier;

/* Tiers by Gender */

SELECT Gender, villager_tier_num as Tier,
count(Gender)/sum(count(Gender)) over (PARTITION BY villager_tier_num) as Percent
FROM acnh_villagers
GROUP BY Gender, Tier;



/* Personality Type by Tiers*/

SELECT Personality, villager_tier_num as Tier,
count(villager_tier_num)/sum(count(villager_tier_num)) over (PARTITION BY Personality) as Percent
FROM acnh_villagers
GROUP BY Tier, Personality;

/* Species by Tiers */

SELECT Species, villager_tier_num as Tier,
count(villager_tier_num)/sum(count(villager_tier_num)) over (PARTITION BY Species) as Percent
FROM acnh_villagers
GROUP BY Tier, Species;

/* Gender by Tiers */

SELECT Gender, villager_tier_num as Tier,
count(villager_tier_num)/sum(count(villager_tier_num)) over (PARTITION BY Gender) as Percent
FROM acnh_villagers
GROUP BY Tier, Gender;



/* My Villagers and Ranks*/
SELECT villager_name, villager_rank, villager_tier_num
FROM acnh_villagers
WHERE villager_name in ('Broccolo', 'Zucker', 'Aurora', 'Nibbles', 'Reneigh', 'Octavian', 'Marshal', 'Kidd', 'Diana');
ORDER BY villager_rank;
