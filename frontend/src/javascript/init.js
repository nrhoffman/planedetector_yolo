let map;
const markers = [];

// Dynamically load Google Maps script
async function loadGoogleMapsAPI() {
    // Send the GET request
    const response = await fetch(`/api/getapi`);       
    if (response.ok) {
        apiKey = await response.json();
    }
    else {
        alert("HTTP-Error: " + response.status);
    }
    const script = document.createElement('script');
    script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&loading=async&callback=initMap&v=beta&libraries=places`;
    script.async = true;  // Load the script asynchronously
    script.defer = true;  // Ensure the script is executed after the document has been parsed
    document.body.appendChild(script);
}

    // Initialize the map once the API is loaded
async function initMap() {
    var location = {lat: 40.730610, lng: -73.935242}; // Example: New York City
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 5,
        center: location,
        mapId: '28d3c662e81d8625'
    });

    const {AdvancedMarkerElement} = await google.maps.importLibrary("marker")

    // Add a click listener to the map
    map.addListener('click', function(event) {
        // Only add a marker if there are fewer than 2 markers
        if (markers.length < 2) {
            addMarker(event.latLng, map, AdvancedMarkerElement);
        } else {
            alert('Maximum of 2 markers allowed.');
        }
    });

    document.getElementById('sendCoords').addEventListener('click', function () {
        sendMarkerCoordinates();
    });
}

// Function to add a marker at the clicked location
function addMarker(location, map, AdvancedMarkerElement) {
    var marker = new AdvancedMarkerElement({
        position: location,
        map: map,
        gmpDraggable: true,
    });

    // Add the marker to the markers array
    markers.push(marker);

    // Add a click event listener to the marker to handle deletion
    marker.addListener('gmp-click', function () {
        if (confirm('Do you want to delete this marker?')) {
            marker.setMap(null);
            // Remove the marker from the markers array
            const index = markers.indexOf(marker);
            if (index > -1) {
                markers.splice(index, 1);
            }
        }
    });

    // Add a dragend event listener to the marker
    marker.addListener('dragend', function (event) {
        console.log('Marker dragged to: ' + event.latLng.lat() + ', ' + event.latLng.lng());
    });

    map.panTo(location);
}

async function sendMarkerCoordinates() {
    if (markers.length < 2) {
        alert('Please add exactly two markers.');
        return;
    }
    const loadingElement = document.getElementById('loading');
    const display = document.getElementById('planeCount');
    const button = document.getElementById('sendCoords');

    button.disabled = true;
    display.innerText = 'Loading...';
    loadingElement.style.display = 'block';

    // Retrieve the lat/lng of the first two markers
    const [marker1, marker2] = markers;
    const lat1 = Math.max(marker1.position.lat, marker2.position.lat);
    const lon1 = Math.min(marker1.position.lng, marker2.position.lng);
    const lat2 = Math.min(marker1.position.lat, marker2.position.lat);
    const lon2 = Math.max(marker1.position.lng, marker2.position.lng);

    // Construct the URL with the coordinates
    const url = `/api/getplanes/${lat1}/${lon1}/${lat2}/${lon2}`;
    const prog_url = `/api/getprogress`;

    // Start SSE connection
    const eventSource = new EventSource(prog_url);

    // Handle SSE messages
    eventSource.onmessage = (event) => {
        data = JSON.parse(event.data)
        if(data.Status == "In Progress"){
            progress_per = Math.round((parseInt(data.Value, 10)/parseInt(data.Total, 10))*100)
            if(data.Type == "Tile Generation"){
                console.log('Tile Generation: ', progress_per, '/', 100);
                console.log('Image Processing: ', 0, '/', 100);
            }
            else{
                console.log('Tile Generation: ', 100, '/', 100 );
                console.log('Image Processing:', progress_per, '/', 100);
            }
        }
        else if(data.Status == "Complete"){
            console.log('Tile Generation: ', 100, '/', 100 );
            console.log('Image Processing:', 100, '/', 100);
            eventSource.close();
        }
        else{
            console.log('Update from SSE:', );
        }
    };
    eventSource.onerror = (error) => {
        if (eventSource.readyState === EventSource.CLOSED) {
            console.log('SSE connection closed.');
        } else {
            console.error('Error with SSE:', error);
        }
        eventSource.close();
    };

    // Send the GET request
    try {
        // Start standard fetch
        const response = await fetch(url);
        
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();
        const numberOfPlanes = data.numberOfPlanes || 0;
        display.innerText = `Number of Planes = ${numberOfPlanes}`;

        // Create an image element and set its source to the Base64 string
        const img = new Image();
        img.src = `data:image/jpeg;base64,${data.image}`;
        imageDisplay.innerHTML = ''; // Clear previous image
        imageDisplay.appendChild(img);
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
        display.innerText = 'Error';
    } finally {
        loadingElement.style.display = 'none'; // Hide the loading spinner
        button.disabled = false;
    }
}

// Load the Google Maps API after the page loads
window.onload = loadGoogleMapsAPI;