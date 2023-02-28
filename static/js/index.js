var placeSearch,autocomplete;
    function initialize() {
    autocomplete = new google.maps.places.Autocomplete(document.getElementById('autocomplete'), { types: [ 'geocode' ] });
    autocomplete2 = new google.maps.places.Autocomplete(document.getElementById('autocomplete2'), { types: [ 'geocode' ] });
    google.maps.event.addListener(autocomplete2, 'place_changed', function() {
    fillInAddress();});
    google.maps.event.addListener(autocomplete, 'place_changed', function() {
      fillInAddress();
    });
  }
  function fillInAddress() {
    var place = autocomplete.getPlace();

    for (var component in component_form) {
      document.getElementById(component).value = "";
      document.getElementById(component).disabled = false;
    }

    for (var j = 0; j < place.address_components.length; j++) {
      var att = place.address_components[j].types[0];
      if (component_form[att]) {
        var val = place.address_components[j][component_form[att]];
        document.getElementById(att).value = val;
      }
    }
  }