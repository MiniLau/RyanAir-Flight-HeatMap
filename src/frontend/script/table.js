function add_table_headers(table, contents) {
  var header = table.createTHead();
  var row = header.insertRow(0);
  for(var i=0; i<contents.length; i++) {
    var cell = row.insertCell(i);
    cell.innerHTML = contents[i];
  }
}

function add_table_rows(table, rows_data) {
  for(var i=0; i<rows_data.length; i++) {
    var row = table.insertRow(i+1);
    _create_row_cells(row, rows_data[i])
  }
}

function _create_row_cells(row, row_data) {
  for(var i=0; i<row_data.length; i++) {
    var cell = row.insertCell(i);
    cell.innerHTML = row_data[i];
  }
}
