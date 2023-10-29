

create table Customer(
	username varchar(255) int Primary Key,
	pasword varchar(255),
	fname varchar(255) not null,
	lname varchar(255) not null,
	dateOfBirth date not null,
	gender varchar(1) not null,
	phoneNum varchar(255) not null,
	email varchar(255),
	localPlace varchar(255),
	points int
);

-- create table UserLogin(
-- 	username varchar(255) Primary Key,
-- 	pasword varchar(255) not null,
-- 	customerId int,
-- 	Foreign Key (customerId) References Customer(customerId),
-- );

create table Masuer(
	masuerId int Primary Key,
	fname varchar(255) not null,
	lname varchar(255) not null,
	dateOfBirth date not null,
	gender varchar(1) not null,
	phoneNum varchar(255) not null,
	email varchar(255),
	massuertype varchar(255) not null,
	dayoff varchar not null,
	statusNow bit not null,
	salaryCode int not null
);

create table CustomerReview(
	reviewId int Primary Key,
	customerId int,
	masuerId int,
	reviewText varchar(255) not null,
	Foreign Key (customerId) References Customer(customerId),
	Foreign Key (masuerId) References Masuer(masuerId)
);

create table Salary(
	salaryCode int Primary Key,
	moneys float,
);

create table MassuerSalary(
	massuersalaryId int Primary Key,
	masuerId int,
	salaryCode int,
	Foreign Key (masuerId) References Masuer(masuerId),
	Foreign Key (salaryCode) References Salary(salaryCode)
);


create table Booking(
	bookingId int Primary Key,
	customerId int,
	typeOfMassageId int,
	datTime smalldatetime not null,
	Foreign Key (customerId) References Customer(customerId),
	Foreign Key (typeOfMassageId) References MassageType(typeOfMassageId)
);

create table Payment(
	paymentId int Primary Key,
	bookingId int,
	Amount float not null,
	datTime smalldatetime not null,
	Foreign Key (bookingId) References Booking(bookingId)
);

create table MoneyInCome(
    incomeId int Primary Key,
    paymentId int,
    Foreign Key (paymentId) References Payment(paymentId)
);

create table MoneyOutCome(
	outcomeId int Primary Key,
	massuersalaryId int,
	datTime date,
	Foreign Key (massuersalaryId) References MassuerSalary(massuersalaryId)
);

create table TreatmentHistory(
	treatmenthistoryId int Primary Key,
	paymentId int,
	customerId int,
	masuerId int,
	Foreign Key (paymentId) References Payment(paymentId),
	Foreign Key (customerId) References Customer(customerId),
	Foreign Key (masuerId) References Masuer(masuerId)
);
