
var map = L.map('mapid').setView([latitude, longitude], zoomLevel); 
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);
var activityData = [
  {latitude:12.933429612321715,  longitude:77.62186452280241,name:"escape room",type:"Escape room"}
];
function getMarkerIcon(activityType) {
  if (activityType === "Park") {
    return L.icon({
      iconUrl: 'path/to/park_icon.png',
      iconSize: [32, 32],
    });
  } else if (activityType === "Landmark") {
    return L.icon({
      iconUrl: 'path/to/landmark_icon.png', 
      iconSize: [32, 32],
    });
  } else {
  }
}
for (var i = 0; i < activityData.length; i++) {
  var activity = activityData[i];
  var marker = L.marker([activity.latitude, activity.longitude], { icon: getMarkerIcon(activity.type) })
                  .bindPopup("<b>" + activity.name + "</b>"); 
  marker.addTo(map);
}
