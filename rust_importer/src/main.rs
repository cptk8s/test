use anyhow::Result;
use calamine::{open_workbook_auto, DataType};
use reqwest::blocking::Client;
use serde::Serialize;
use chrono::NaiveDate;
use std::env;

#[derive(Serialize)]
struct ClientePayload<'a> {
    nombre: &'a str,
}

#[derive(Serialize)]
struct ComercialPayload<'a> {
    nombre: &'a str,
    apellidos: Option<&'a str>,
}

#[derive(Serialize)]
struct TipoPayload<'a> {
    descripcion: &'a str,
}

#[derive(Serialize)]
struct ActividadPayload<'a> {
    fecha: &'a str,
    id_tipo_actividad: i64,
    id_comercial: i64,
    id_cliente: i64,
    titulo: &'a str,
    descripcion: Option<&'a str>,
}

fn as_text(cell: &DataType) -> Option<String> {
    match cell {
        DataType::String(s) => Some(s.clone()),
        DataType::Float(f) => Some(format!("{}", f)),
        DataType::Int(i) => Some(format!("{}", i)),
        _ => None,
    }
}

fn main() -> Result<()> {
    let args: Vec<String> = env::args().collect();
    if args.len() < 3 {
        eprintln!("Usage: rust_importer <file.xlsx> <api_base_url>");
        std::process::exit(2);
    }
    let path = &args[1];
    let api = &args[2];
    let client = Client::new();

    let mut workbook = open_workbook_auto(path)?;
    let sheet_names = workbook.sheet_names().to_owned();
    if sheet_names.is_empty() {
        anyhow::bail!("No sheets found");
    }
    let range = workbook
        .worksheet_range(&sheet_names[0])?
        .unwrap();

    // assuming first row is header
    let mut rows = range.rows();
    let header = rows.next();
    if header.is_none() {
        anyhow::bail!("Empty sheet");
    }

    for row in rows {
        // map columns by header names (simple positional approach)
        let company = row.get(0).and_then(as_text).unwrap_or_default();
        let comercial_id = row.get(1).and_then(as_text).and_then(|s| s.parse::<i64>().ok());
        let comercial_nombre = row.get(2).and_then(as_text);
        let comercial_apellidos = row.get(3).and_then(as_text);
        let tipo = row.get(4).and_then(as_text).unwrap_or_else(|| "Default".to_string());
        let fecha = row.get(5).and_then(as_text).unwrap_or_else(|| chrono::Utc::now().to_string());
        let titulo = row.get(6).and_then(as_text).unwrap_or_else(|| "Sin titulo".to_string());
        let descripcion = row.get(7).and_then(as_text);

        // Cliente: check or create
        let cliente_id = match get_or_create_cliente(&client, api, &company)? {
            Some(id) => id,
            None => { eprintln!("Failed to create/find cliente for {}", company); continue; }
        };

        // Comercial: prefer ID from file, else find/create by name
        let comercial_id = if let Some(id) = comercial_id {
            id
        } else if let Some(ref nombre) = comercial_nombre {
            get_or_create_comercial(&client, api, nombre, comercial_apellidos.as_deref())?
        } else {
            eprintln!("Comercial not found in row, skipping");
            continue;
        };

        // Tipo actividad: get or create
        let tipo_id = get_or_create_tipo(&client, api, &tipo)?;

        // create actividad
        let payload = ActividadPayload {
            fecha: &fecha,
            id_tipo_actividad: tipo_id,
            id_comercial: comercial_id,
            id_cliente: cliente_id,
            titulo: &titulo,
            descripcion: descripcion.as_deref(),
        };

        let resp = client.post(format!("{}/actividades", api))
            .json(&payload)
            .send()?;
        if resp.status().is_success() {
            println!("Created actividad: {} for cliente {}", titulo, company);
        } else {
            eprintln!("Failed creating actividad: {} - {}", resp.status(), resp.text()?);
        }
    }

    Ok(())
}

fn get_or_create_cliente(client: &Client, api: &str, nombre: &str) -> Result<Option<i64>> {
    let get_url = format!("{}/clientes?nombre={}", api, urlencoding::encode(nombre));
    let r = client.get(&get_url).send()?;
    if r.status().is_success() {
        let list: Vec<serde_json::Value> = r.json()?;
        if let Some(first) = list.get(0) {
            if let Some(id) = first.get("id").and_then(|v| v.as_i64()) {
                return Ok(Some(id));
            }
        }
    }
    // create
    let payload = ClientePayload { nombre };
    let create = client.post(format!("{}/clientes", api)).json(&payload).send()?;
    if create.status().is_success() {
        let j: serde_json::Value = create.json()?;
        Ok(j.get("id").and_then(|v| v.as_i64()))
    } else {
        eprintln!("Failed to create cliente {}: {}", nombre, create.status());
        Ok(None)
    }
}

fn get_or_create_comercial(client: &Client, api: &str, nombre: &str, apellidos: Option<&str>) -> Result<i64> {
    let get_url = format!("{}/comerciales?nombre={}", api, urlencoding::encode(nombre));
    let r = client.get(&get_url).send()?;
    if r.status().is_success() {
        let list: Vec<serde_json::Value> = r.json()?;
        if let Some(first) = list.get(0) {
            if let Some(id) = first.get("id").and_then(|v| v.as_i64()) {
                return Ok(id);
            }
        }
    }
    // create
    let payload = ComercialPayload { nombre, apellidos };
    let create = client.post(format!("{}/comerciales", api)).json(&payload).send()?;
    let j: serde_json::Value = create.json()?;
    Ok(j.get("id").and_then(|v| v.as_i64()).unwrap_or(-1))
}

fn get_or_create_tipo(client: &Client, api: &str, descripcion: &str) -> Result<i64> {
    let get_url = format!("{}/tipos_actividad?descripcion={}", api, urlencoding::encode(descripcion));
    let r = client.get(&get_url).send()?;
    if r.status().is_success() {
        let list: Vec<serde_json::Value> = r.json()?;
        if let Some(first) = list.get(0) {
            if let Some(id) = first.get("id").and_then(|v| v.as_i64()) {
                return Ok(id);
            }
        }
    }
    // create
    let payload = TipoPayload { descripcion };
    let create = client.post(format!("{}/tipos_actividad", api)).json(&payload).send()?;
    let j: serde_json::Value = create.json()?;
    Ok(j.get("id").and_then(|v| v.as_i64()).unwrap_or(-1))
}
