# Hospital Information System

## Author

Cole Little

## Overview

This project is a Hospital Information System developed for UW-Milwaukee course HI741. The program controls patient management, encounter tracking, note retrieval, provider workload monitoring, revenue monitoring, and statistics generation using simulated clinical data. The system GUI is built with Tkinter.

## Features

### Authentication System
- User login with role-based access
- Failed login tracking
- Activity logging

### Clinical Functions
- Retrieve patient information 
- Add patient information
- Remove patient from system
- Count visits by date
- View patient notes

### Administrative Functions
- Monitor provider workload
- Monitor department revenue

### Management Functions
- Generate patient statistics
- Visualize average age by gender

## Technologies Used

- Python
- Tkinter
- Matplotlib
- CSV-based data storage
- Object-Oriented Programming

## Repository Structure

```text
FinalProject/
│
├── data/
├── outputs/
├── src/
├── main.py
├── README.md
├── requirements.txt
└── uml_diagram.png
```

## How to Run

### 1. Install Required Packages

```bash
pip install -r requirements.txt
```

### 2. Generate simulated clinical data (located in `data/`)

```bash
python data_generator.py
```

### 2. Run the Program

```bash
python main.py
```

## Data Files

The program loads simulated healthcare data from CSV files located in the `/data` directory.

These include:
- patients.csv
- encounters.csv
- procedures.csv
- providers.csv
- departments.csv
- notes.csv

## Output Files

The system generates:
- activity_log.csv

And updates:
- patients.csv, encounters.csv, procedures.csv, and notes.csv

## UML Diagram

The UML diagram for the object-oriented class structure is included in the repository as:

```text
uml_diagram.png
```