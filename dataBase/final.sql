create table Doctor(
    CID int Primary key,
    DocName varchar(255),
    Spacially varchar(255),
    workAge int
);

create table Patients(
    CID int Primary key,
    PatientsName varchar(255),
    Patientsaddress varchar(255),
    age int
);

create table Drug(
    CommonName varchar(255) Primary key,
    tradeName varchar(255),
    company varchar(255),
    fomula varchar(255)
);

create table Pharmacy(
    PharmacyName varchar(255) Primary Key,
    PharmacyAddress varchar(255),
    PhoneNum varchar(255),
    manager varchar(255)
);

create table Pharamacist(
    CID int Primary key,
    PharamacistName varchar(255),
    quatification varchar(255)
);

create table work(
    PharamacistID int,
    PharamacyName varchar(255),
    Foreign Key (PharamacistID) References Pharamacist(CID),
    Foreign Key (PharamacyName) References Pharmacy(PharmacyName)
);

create table sell(
    PharamacyName varchar(255),
    DrugName varchar(255),
    Price float,
    Foreign key (PharamacyName) References Pharmacy(PharmacyName),
    Foreign key (DrugName) References Drug(CommonName)
);

create table treat(
    DoctorID int,
    PatientsID int,
    Foreign key (DoctorID) References Doctor(CID),
    Foreign key (PatientsID) References Patients(CID)
);

create table PrescribeDrug(
    DoctorID int,
    PatientsID int,
    DrugName varchar(255),
    PrescribeDate date,
    NDrug int
    Foreign key (DoctorID) References Doctor(CID),
    Foreign key (PatientsID) References Patients(CID),
    Foreign key (DrugName) References Drug(CommonName)
);



