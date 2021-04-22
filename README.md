# Database redo simulator

Emulates DBMS redo system.

## Setup

### Dependency installation

```bash
pip install -r requirements.txt
```

### Database config

Set `database.ini` fields accordingly to your environment.

```ini
[postgres]
host=localhost
database=olokinhomeu
user=fausto
password=miau
port=5432
```

### Running

Run the following command in `db-redo-simulator` root directory.

```bash
python -m db-redo-simulator.src.main --log=db-redo-simulator/log/<log-file>
```
