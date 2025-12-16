## Configuration

Configuration is controlled via `singular_config.json`.
It is recommended not to edit this file manully.
Singular has CLI commands do edit the configurations.

| Parameter           | Use                                                | CLI command                                     | Default                          |
|---------------------|----------------------------------------------------|-------------------------------------------------|----------------------------------|
| DATA_BASE_PATH      | Folder for FileSystemDataBase.json                 | ```bash 
singular config --set DATA_BASE_PATH="/path"```    | "/var/lib/singular"              |
| SCOPE_DIRECTORY     | Directory for analysis                             | ```bash singular config --set SCOPE_DIRECTORY="/path"```   | "/var/log/singular/singular.log" |
| LOG_FILE            | File path where logs are saved                     | ```bash singular config --set LOG_FILE="/path/file.log"``` | False                            |
| ACCESS_HIDDEN_FILES | Whether to access hidden files (recommended False) | singular config --set ACCESS_HIDDEN_FILES=True  | False                            |

