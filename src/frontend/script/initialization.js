function _get_reachable_countries(locations) {
  var countries = new Set();
  for(const [key, location] of Object.entries(locations)) {
    countries.add(location.countryCode);
  }
  return countries;
}

function _disable_unreachable_countries(reachable_countriesCodes) {
  for(const [code, state] of Object.entries(simplemaps_worldmap_mapdata.state_specific)) {
    if(!reachable_countriesCodes.has(code)) {
      state["color"] = "gray"; state["hover_color"] = "gray";
      state["zoomable"] = "no";
    }
  }
}

function _adapt_reachable_countries_description(cheapest_per_country, max_price) {
  for(const [countryCode, country] of Object.entries(simplemaps_worldmap_mapdata.state_specific)) {
    if(countryCode in cheapest_per_country) {
      var min_price = cheapest_per_country[countryCode].price;
      var factor = 5;
      var percentage = Math.pow(Math.log(min_price), factor)/Math.pow(Math.log(max_price), factor);
      country.name += " (min. " + min_price + "€)";
      country.color = heatMapColor(percentage);
      country.hover_color = country.color;
    } else {
      country.name += " (no flights)";
    }
  }
}

function _render_locations_description(locations) {
  for(const [key, location] of Object.entries(locations)) {
    var table = document.createElement("TABLE");
    add_table_headers(table, ["Price",  "Duration", "Origin Airport"]);
    add_table_rows(table, location['_description']);
    location['description'] = table.outerHTML;
  }
}

function _get_heatmap_values(countries) {
  var data = {};
  for(const [countryCode, info] of Object.entries(countries)) {
    data[countryCode] = _getRandomInt(200) + 50;
  }
  return data;
}


function _get_max_price(cheapest_per_country) {
  var max = 0;
  for(const [countryCode, info] of Object.entries(cheapest_per_country)) {
    if(info.price > max)
      max = info.price;
  }
  return max;
}


function heatMapColor(percentage) {
  var h = (1.0 - percentage) * 100;
  return _HSLToHex(h, 100, 50);
}
function _HSLToHex(h,s,l) {
  s /= 100;
  l /= 100;

  let c = (1 - Math.abs(2 * l - 1)) * s,
      x = c * (1 - Math.abs((h / 60) % 2 - 1)),
      m = l - c/2,
      r = 0,
      g = 0,
      b = 0;

  if (0 <= h && h < 60) {
    r = c; g = x; b = 0;
  } else if (60 <= h && h < 120) {
    r = x; g = c; b = 0;
  } else if (120 <= h && h < 180) {
    r = 0; g = c; b = x;
  } else if (180 <= h && h < 240) {
    r = 0; g = x; b = c;
  } else if (240 <= h && h < 300) {
    r = x; g = 0; b = c;
  } else if (300 <= h && h < 360) {
    r = c; g = 0; b = x;
  }
  // Having obtained RGB, convert channels to hex
  r = Math.round((r + m) * 255).toString(16);
  g = Math.round((g + m) * 255).toString(16);
  b = Math.round((b + m) * 255).toString(16);

  // Prepend 0s, if necessary
  if (r.length == 1)
    r = "0" + r;
  if (g.length == 1)
    g = "0" + g;
  if (b.length == 1)
    b = "0" + b;

  return "#" + r + g + b;
}
function _getRandomInt(max) {
  return Math.floor(Math.random() * Math.floor(max));
}



function initialize(airports, cheapest_per_country) {
  max_price = _get_max_price(cheapest_per_country);
  reachable_countries = _get_reachable_countries(airports);
  _disable_unreachable_countries(reachable_countries);
  _adapt_reachable_countries_description(cheapest_per_country, max_price);
  _render_locations_description(airports);
}
