function get_reachable_countries(locations) {
  var countries = new Set();
  for(const [key, location] of Object.entries(locations)) {
    countries.add(location.countryCode);
  }
  return countries;
}

function disable_unreachable_countries(reachable_countriesCodes) {
  for(const [code, state] of Object.entries(simplemaps_worldmap_mapdata.state_specific)) {
    if(!reachable_countriesCodes.has(code)) {
      state["color"] = "gray"; state["hover_color"] = "gray";
      state["zoomable"] = "no";
    }
  }
}

function adapt_reachable_countries_description(cheapest_per_country) {
  for(const [countryCode, country] of Object.entries(simplemaps_worldmap_mapdata.state_specific)) {
    if(countryCode in cheapest_per_country) {
      var min_price = cheapest_per_country[countryCode].price;
      country.name += " (min. " + min_price + "€)";
    } else {
      country.name += " (no flights)";
    }
  }
}

function render_locations_description(locations) {
  for(const [key, location] of Object.entries(locations)) {
    var table = document.createElement("TABLE");
    add_table_headers(table, ["Price",  "Duration", "Origin Airport"]);
    add_table_rows(table, location['_description']);
    location['description'] = table.outerHTML;
  }
}
