create table Customer(
	customerId int Primary Key,
	fname varchar(255) not null,
	lname varchar(255) not null,
	dateOfBirth date not null,
	gender varchar(1) not null,
	phoneNum varchar(255) not null,
	email varchar(255),
	localPlace varchar(255)
);

create table Masuer(
	masuerId int Primary Key,
	fname varchar(255) not null,
	lname varchar(255) not null,
	dateOfBirth date not null,
	phoneNum varchar(255) not null,
	email varchar(255),
	MasseusePhoto varbinary(max)
);


create table MemberShip(
	memberShipId int Primary Key,
	customerId int,
	points int,
	Foreign Key (customerId) References Customer(customerId)
);

create table CustomerReview(
	reviewId int Primary Key,
	customerId int,
	masuerId int,
	reviewText varchar(255) not null,
	Foreign Key (customerId) References Customer(customerId),
	Foreign Key (masuerId) References Masuer(masuerId)
);

create table MassageType(
	typeOfMassageId int Primary Key,
	masuerId int,
	typeName varchar(255) not null,
	Foreign Key (masuerId) References Masuer(masuerId)
);

create table MasseuseDayOff(
	masuerId int,
	dayNa varchar(255) not null,
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