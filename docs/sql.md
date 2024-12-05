# SQL Scripts

```sql
CREATE TABLE Temperature (
    id INT IDENTITY(1,1) PRIMARY KEY, -- Auto-incrementing unique identifier
    min FLOAT NOT NULL,              -- Minimum temperature
    max FLOAT NOT NULL,              -- Maximum temperature
    mean FLOAT NOT NULL              -- Mean temperature
);
```

```sql
CREATE TABLE Forecast (
    id INT IDENTITY(1,1) PRIMARY KEY,
    lstm FLOAT NOT NULL,
    service FLOAT NOT NULL,
);
```

```sql
CREATE TABLE Days (
    id INT IDENTITY(1,1) PRIMARY KEY, -- Auto-incrementing unique identifier for this table
    date DATE NOT NULL,              -- Date for the record
    temperature_id INT NOT NULL,     -- Foreign key to the Temperature table
    forecast_id INT NOT NULL,        -- Foreign key to the Forecast table,
    CONSTRAINT FK_Temperature FOREIGN KEY (temperature_id) REFERENCES Temperature(id),
    CONSTRAINT FK_Forecast FOREIGN KEY (forecast_id) REFERENCES Forecast(id)
);
```