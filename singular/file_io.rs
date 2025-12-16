// rustimport:pyo3

use pyo3::prelude::*;
use std::fs::File;
use std::io::Read;
use std::path::PathBuf;

#[pyfunction]
fn read_file_bytes(path: PathBuf) -> PyResult<Vec<u8>> {
    let mut file = File::open(&path)
        .map_err(|e| pyo3::exceptions::PyIOError::new_err(e.to_string()))?;
    let mut buffer = Vec::new();
    file.read_to_end(&mut buffer)
        .map_err(|e| pyo3::exceptions::PyIOError::new_err(e.to_string()))?;
    Ok(buffer)
}