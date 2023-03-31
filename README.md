# Python-Car-Service-Mangaer

This Python project is a car service management system that tracks
cars, customers, and transactions. It includes functions like search,
sort, undo and redo. All data is validated for accuracy and reliability,
and all features have been extensively tested.

-----------------------------
Features and functionalities:
-----------------------------
3.1. CRUD car: id, model, purchase year, km number, warranty. The km number and purchase year must be strictly positive.
3.2. CRUD client card: id, last name, first name, CNP, birth date (dd.mm.yyyy), registration date (dd.mm.yyyy). The CNP must be unique.
3.3. CRUD transaction: id, car id, client card id (can be null), parts amount, labor amount, date and time. If there is a client card, then a 10% discount is applied for the labor amount. If the car is under warranty, then the parts are free. The paid price and discounts given are printed.
3.4. Search for cars and clients. Full text search.
3.5. Display all transactions with a given amount range.
3.6. Display cars ordered in descending order by the labor amount obtained.
3.7. Display client cards ordered in descending order by the value of discounts obtained.
3.8. Delete all transactions from a certain interval of days.
3.9. Update the warranty for each car: a car is under warranty if and only if it has a maximum of 3 years since purchase and a maximum of 60,000 km.

+ Undo + Redo + Delete on cascade
