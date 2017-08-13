function initAutocomplete() {
    var autocomplete = new google.maps.places.Autocomplete(
        (document.getElementById('region')),
        {types: ['(cities)']});
}