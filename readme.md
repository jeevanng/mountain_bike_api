# Planning Documentation

Written by Jeevan Ng 

# Overview 

This application will serve as a centralised platform for mountain biking enthusiasts to access comprehensive information about single track routes across the globe. 

# The Problem (R1)

Currently, the problem at hand is the lack of centralised platforms to access comprehensive information about mountain bike single track routes across the world. 

By creating an application with an API and a database, users can easily find suitable tracks based on their mountain bike type no matter where they are in the world. Whether they are on holiday overseas or looking for new tracks in their town, users will be able to find tracks and additional information (track descriptions, distance, duration etc.) at the tip of their fingers in one place. 

This application will aim to provide a centralised, user friendly and reliable hub for the mountain biking community. 

# Why is it a problem that needs solving? (R2)

This is a problem that needs solving as mountain bike enthusiasts are currently relying on various sources like online forums, word-of-mouth, magazines, websites and other applications to find information about tracks local to them. 

It is also incredibly difficult to find information on single track routes when travelling overseas. This is especially true since the information on forums, magazines and websites may be in a language that the user does not understand. 

Currently, the closest centralised application that exists is *Trailforks*, however, our application aims to provide unique features, enhanced functionalities and a better user experience. *Trailforks* is a clunky application and can be difficult to navigate when trying to find information on tracks. 

We have identified that mountain bike enthusiasts want a user friendly centralised platform to access all their mountain biking needs. They also wish to search tracks via different filters. This application aims to offer exactly that with added functionalities like the ability to populate a list of tracks that would be suitable to ride depending on the type of mountain bike. Further down the line, filters will be added to allow users to search for tracks by difficulty, duration, descent, climb etc. This functionality is currently not supported by *Trailforks*. 

# Why have you chosen this database system? What are the drawbacks? (R3)

The chosen database system is postgreSQL. PostgreSQL is a relational database management system which will best represent our data. It is one of the  most popular open-source relational databases with a large amount of active open-source contributors offering a built-in community support network.

PostgreSQL supports international characters (if needed in the future) and is highly scalable in the quantity of data it can manage. This will helpful as this application develops further down the line as we will be adding hundreds of locations around the world with even more tracks. 

PostgreSQL is ACID (atomicity, consistency, isolation and durability) compliant, which basically ensures database transactions are processed reliably and consistently. The principles relate to transactional processing and are crucial for maintaining data integrity and recoverability in a predictable manner.