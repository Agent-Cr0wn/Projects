-- Keep a log of any SQL queries you execute as you solve the mystery.

SELECT description FROM crime_scene_reports
WHERE year = 2021
    AND month = 7
    AND day = 28;
-- 3 witnesses / theft time = 10:15am / "bakery"

SELECT transcript FROM interviews
WHERE year = 2021
    AND month = 7
    AND day = 28
AND transcript LIKE "%bakery%";
--