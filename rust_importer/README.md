Rust importer

Usage:

cargo run --release -- <file.xlsx> http://localhost:5000

Assumes first sheet and columns:
0: Company (cliente nombre)
1: ComercialId (optional)
2: ComercialNombre (optional)
3: ComercialApellidos (optional)
4: TipoActividad (descripcion)
5: Fecha (ISO string)
6: Titulo
7: Descripcion (optional)

The tool will check/create cliente, comercial (if needed), tipo actividad and then create actividad calling the Flask API.
