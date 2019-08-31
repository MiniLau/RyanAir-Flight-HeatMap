function hide_country_popup(previousCountryCode, countryCode) {
  if(previousCountryCode) {
    simplemaps_worldmap_mapdata.state_specific[previousCountryCode].popup = "detect";
  }
  if(countryCode)
    simplemaps_worldmap_mapdata.state_specific[countryCode].popup = "off";
}

function show_country_popup(countryCode) {
  if(countryCode)
    simplemaps_worldmap_mapdata.state_specific[countryCode].popup = "detect";
}


function exclusive_show_country_airports(countryCode) {
  for(var location in simplemaps_worldmap_mapdata.locations){
  	loc = simplemaps_worldmap_mapdata.locations[location];
  	if(loc.countryCode == countryCode) {
      loc.hide = "no";
  	} else {
      loc.hide = "yes";
    }
  }
}


function refresh_map() {
  simplemaps_worldmap.refresh();
  remove_ad();
}

function remove_ad() {
  $("div[id='map_inner'] > div > svg").remove();
}
