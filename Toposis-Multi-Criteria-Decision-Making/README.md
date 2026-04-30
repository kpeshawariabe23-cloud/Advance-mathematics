# TOPSIS Project â€“ Multi-Criteria Decision Making

This repository contains a complete implementation of the **TOPSIS** (Technique for Order of Preference by Similarity to Ideal Solution) method, developed as part of **Project-1**. The project demonstrates command-line, package-based, and web-based implementations of the TOPSIS algorithm.

## Project Information

| Field | Details |
|-------|---------|
| Course | Project-1 |
| Student Name | Keshav Peshawaria |
| Roll Number | 102303502 |
| Group | 3C42 |
| Method | TOPSIS (MCDM) |

---

## ðŸ“Œ Sample Input File (IMPORTANT)

Create a file named `data.csv` in the same folder as `topsis.py` and paste the following content:

```csv
Fund,P1,P2,P3,P4,P5
M1,0.67,0.45,6.5,42.6,12.56
M2,0.6,0.36,3.6,53.3,14.47
M3,0.82,0.67,3.8,63.1,17.1
M4,0.6,0.36,3.5,69.2,18.42
M5,0.76,0.58,4.8,43,12.29
M6,0.69,0.48,6.6,48.7,14.12
M7,0.79,0.62,4.8,59.2,16.35
M8,0.84,0.71,6.5,34.5,10.64
```

---

## Part-I: Command Line TOPSIS Program

### Description
Part-I contains a Python script that implements the TOPSIS algorithm and executes via the command line. It reads a CSV file, applies the TOPSIS method using user-defined weights and impacts, and produces a ranked output CSV file.

### Usage
```bash
python topsis.py <input_file.csv> <weights> <impacts> <output_file.csv>
```

### Example
```bash
python topsis.py data.csv "1,1,1,2,1" "+,+,-,+,+" output.csv
```

---

## Part-II: Python Package (PyPI)

### Description
In Part-II, the TOPSIS implementation is packaged as a Python module and uploaded to PyPI, allowing installation via pip and execution using a CLI command.

### Installation
```bash
pip install Topsis-Keshav-102303502
```

### Usage
```bash
topsis data.csv "1,1,1,2,1" "+,+,-,+,+" output.csv
```

### PyPI Link
ðŸ”— [https://pypi.org/project/Topsis-Keshav-102303502/](https://pypi.org/project/Topsis-Keshav-102303502/)

---

## Part-III: Web Application (Streamlit)

### Description
Part-III provides a web-based interface using Streamlit, enabling users to upload CSV files, specify weights and impacts, and obtain ranked results interactively.

### ðŸ‘‰ Streamlit App Link:
ðŸ”— [https://topsis-streamlit.streamlit.app](https://topsis-streamlit.streamlit.app)

### ðŸ–¥ï¸ User Interface
The web interface allows users to:
- Upload a CSV file
- Enter weights (comma-separated)
- Enter impacts (+ or -, comma-separated)
- Provide an email ID to receive results

---

## Input/Output Format

### Input File Format
| Fund Name | P1   | P2   | P3   | P4    | P5    |
|-----------|------|------|------|-------|-------|
| M1        | 0.67 | 0.45 | 6.5  | 42.6  | 12.56 |
| M2        | 0.6  | 0.36 | 3.6  | 53.3  | 14.47 |

### Output File Format
| Fund Name | P1   | P2   | P3   | P4    | P5    | Topsis Score | Rank |
|-----------|------|------|------|-------|-------|--------------|------|
| M1        | 0.67 | 0.45 | 6.5  | 42.6  | 12.56 | 0.58         | 2    |
| M2        | 0.6  | 0.36 | 3.6  | 53.3  | 14.47 | 0.42         | 4    |

---

## Validations
The program checks for:
- âœ… Correct number of parameters
- âœ… File existence
- âœ… Minimum 3 columns in input file
- âœ… Numeric values in columns 2 onwards
- âœ… Equal count of weights, impacts, and data columns
- âœ… Valid impact values (+ or -)
- âœ… Valid email format (for web app)

---

## License
MIT License

---

## Author
**Keshav Peshawaria** - Roll No: 102303502


