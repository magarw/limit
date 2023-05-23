
// The svg
var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height");

// Map and projection
var projection = d3.geoMercator()
    .center([0,20])                // GPS of location to zoom on
    .scale(99)                       // This is like the zoom
    .translate([ width/2, height/2 ])

d3.queue()
  .defer(d3.json, "https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson")  // World shape
  .defer(d3.csv, "https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/data_gpsLocSurfer.csv") // Position of circles
  .await(ready);
// "https://docs.google.com/spreadsheets/d/e/2PACX-1vRFOlHWg3nGUxnmEK_WyJ0JJOvQARyb2LR36eD2lGiJx1sr2ajC8jeJpyqgluP_cta-5bCMOtfJEgiU/pub?gid=0&single=true&output=csv"

function ready(error, dataGeo, data) {

  // Create a color scale
  // dataGeo = d3.json("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson")
  // data = d3.csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vRFOlHWg3nGUxnmEK_WyJ0JJOvQARyb2LR36eD2lGiJx1sr2ajC8jeJpyqgluP_cta-5bCMOtfJEgiU/pub?gid=0&single=true&output=csv")

  data = [
    {homelat: "23.424076", homelon: "53.847818", homecontinent: "Asia", n: "0"},
    {homelat: "33.93911", homelon: "67.709953", homecontinent: "Asia", n: "1"},
    {homelat: "17.060816", homelon: "-61.796428", homecontinent: "Asia", n: "0"},
    {homelat: "18.220554", homelon: "-63.068615", homecontinent: "Asia", n: "0"},
    {homelat: "41.153332", homelon: "20.168331", homecontinent: "Europe", n: "1"},
    {homelat: "40.069099", homelon: "45.038189", homecontinent: "Asia", n: "0"},
    {homelat: "12.226079", homelon: "-69.060087", homecontinent: "Asia", n: "0"},
    {homelat: "-11.202692", homelon: "17.873887", homecontinent: "Africa", n: "2"},
    {homelat: "-75.250973", homelon: "-0.071389", homecontinent: "Asia", n: "0"},
    {homelat: "-38.416097", homelon: "-63.616672", homecontinent: "Asia", n: "0"},
    {homelat: "-14.270972", homelon: "-170.132217", homecontinent: "Asia", n: "0"},
    {homelat: "47.516231", homelon: "14.550072", homecontinent: "Asia", n: "0"},
    {homelat: "-25.274398", homelon: "133.775136", homecontinent: "Asia", n: "0"},
    {homelat: "12.52111", homelon: "-69.968338", homecontinent: "Asia", n: "0"},
    {homelat: "40.143105", homelon: "47.576927", homecontinent: "Europe", n: "1"},
    {homelat: "43.915886", homelon: "17.679076", homecontinent: "Asia", n: "0"},
    {homelat: "13.193887", homelon: "-59.543198", homecontinent: "Asia", n: "0"},
    {homelat: "23.684994", homelon: "90.356331", homecontinent: "Asia", n: "2"},
    {homelat: "50.503887", homelon: "4.469936", homecontinent: "Asia", n: "0"},
    {homelat: "12.238333", homelon: "-1.561593", homecontinent: "Africa", n: "1"},
    {homelat: "42.733883", homelon: "25.48583", homecontinent: "Europe", n: "1"},
    {homelat: "25.930414", homelon: "50.637772", homecontinent: "Asia", n: "0"},
    {homelat: "-3.373056", homelon: "29.918886", homecontinent: "Africa", n: "1"},
    {homelat: "9.30769", homelon: "2.315834", homecontinent: "Africa", n: "4"},
    {homelat: "32.321384", homelon: "-64.75737", homecontinent: "Asia", n: "0"},
    {homelat: "4.535277", homelon: "114.727669", homecontinent: "Asia", n: "0"},
    {homelat: "-16.290154", homelon: "-63.588653", homecontinent: "Asia", n: "0"},
    {homelat: "-14.235004", homelon: "-51.92528", homecontinent: "Asia", n: "0"},
    {homelat: "25.03428", homelon: "-77.39628", homecontinent: "Asia", n: "0"},
    {homelat: "27.514162", homelon: "90.433601", homecontinent: "Asia", n: "0"},
    {homelat: "-54.423199", homelon: "3.413194", homecontinent: "Asia", n: "0"},
    {homelat: "-22.328474", homelon: "24.684866", homecontinent: "Africa", n: "2"},
    {homelat: "53.709807", homelon: "27.953389", homecontinent: "Europe", n: "1"},
    {homelat: "17.189877", homelon: "-88.49765", homecontinent: "Asia", n: "0"},
    {homelat: "56.130366", homelon: "-106.346771", homecontinent: "Asia", n: "0"},
    {homelat: "-12.164165", homelon: "96.870956", homecontinent: "Asia", n: "0"},
    {homelat: "-4.038333", homelon: "21.758664", homecontinent: "Africa", n: "4"},
    {homelat: "6.611111", homelon: "20.939444", homecontinent: "Africa", n: "1"},
    {homelat: "-0.228021", homelon: "15.827659", homecontinent: "Asia", n: "0"},
    {homelat: "46.818188", homelon: "8.227512", homecontinent: "Europe", n: "1"},
    {homelat: "7.539989", homelon: "-5.54708", homecontinent: "Asia", n: "0"},
    {homelat: "-21.236736", homelon: "-159.777671", homecontinent: "Asia", n: "0"},
    {homelat: "-35.675147", homelon: "-71.542969", homecontinent: "South America", n: "1"},
    {homelat: "7.369722", homelon: "12.354722", homecontinent: "Africa", n: "5"},
    {homelat: "35.86166", homelon: "104.195397", homecontinent: "Asia", n: "5"},
    {homelat: "4.570868", homelon: "-74.297333", homecontinent: "South America", n: "1"},
    {homelat: "9.748917", homelon: "-83.753428", homecontinent: "Asia", n: "0"},
    {homelat: "21.521757", homelon: "-77.781167", homecontinent: "Asia", n: "0"},
    {homelat: "16.002082", homelon: "-24.013197", homecontinent: "Africa", n: "1"},
    {homelat: "-10.447525", homelon: "105.690449", homecontinent: "Asia", n: "0"},
    {homelat: "35.126413", homelon: "33.429859", homecontinent: "Asia", n: "0"},
    {homelat: "49.817492", homelon: "15.472962", homecontinent: "Europe", n: "1"},
    {homelat: "51.165691", homelon: "10.451526", homecontinent: "Europe", n: "1"},
    {homelat: "11.825138", homelon: "42.590275", homecontinent: "Asia", n: "0"},
    {homelat: "56.26392", homelon: "9.501785", homecontinent: "Europe", n: "1"},
    {homelat: "15.414999", homelon: "-61.370976", homecontinent: "Asia", n: "0"},
    {homelat: "18.735693", homelon: "-70.162651", homecontinent: "Asia", n: "0"},
    {homelat: "28.033886", homelon: "1.659626", homecontinent: "Africa", n: "1"},
    {homelat: "-1.831239", homelon: "-78.183406", homecontinent: "Asia", n: "0"},
    {homelat: "58.595272", homelon: "25.013607", homecontinent: "Europe", n: "1"},
    {homelat: "26.820553", homelon: "30.802498", homecontinent: "Africa", n: "1"},
    {homelat: "24.215527", homelon: "-12.885834", homecontinent: "Asia", n: "0"},
    {homelat: "15.179384", homelon: "39.782334", homecontinent: "Asia", n: "0"},
    {homelat: "40.463667", homelon: "-3.74922", homecontinent: "Europe", n: "4"},
    {homelat: "9.145", homelon: "40.489673", homecontinent: "Africa", n: "7"},
    {homelat: "61.92411", homelon: "25.748151", homecontinent: "Europe", n: "1"},
    {homelat: "-16.578193", homelon: "179.414413", homecontinent: "Asia", n: "0"},
    {homelat: "-51.796253", homelon: "-59.523613", homecontinent: "Asia", n: "0"},
    {homelat: "7.425554", homelon: "150.550812", homecontinent: "Asia", n: "0"},
    {homelat: "61.892635", homelon: "-6.911806", homecontinent: "Asia", n: "0"},
    {homelat: "46.227638", homelon: "2.213749", homecontinent: "Europe", n: "2"},
    {homelat: "-0.803689", homelon: "11.609444", homecontinent: "Asia", n: "0"},
    {homelat: "55.378051", homelon: "-3.435973", homecontinent: "Europe", n: "2"},
    {homelat: "12.262776", homelon: "-61.604171", homecontinent: "Asia", n: "0"},
    {homelat: "42.315407", homelon: "43.356892", homecontinent: "Europe", n: "2"},
    {homelat: "3.933889", homelon: "-53.125782", homecontinent: "Asia", n: "0"},
    {homelat: "49.465691", homelon: "-2.585278", homecontinent: "Asia", n: "0"},
    {homelat: "7.946527", homelon: "-1.023194", homecontinent: "Africa", n: "9"},
    {homelat: "36.137741", homelon: "-5.345374", homecontinent: "Asia", n: "0"},
    {homelat: "71.706936", homelon: "-42.604303", homecontinent: "Asia", n: "0"},
    {homelat: "13.443182", homelon: "-15.310139", homecontinent: "Asia", n: "0"},
    {homelat: "9.945587", homelon: "-9.696645", homecontinent: "Asia", n: "0"},
    {homelat: "16.995971", homelon: "-62.067641", homecontinent: "Asia", n: "0"},
    {homelat: "1.650801", homelon: "10.267895", homecontinent: "Asia", n: "0"},
    {homelat: "39.074208", homelon: "21.824312", homecontinent: "Europe", n: "1"},
    {homelat: "-54.429579", homelon: "-36.587909", homecontinent: "Asia", n: "0"},
    {homelat: "15.783471", homelon: "-90.230759", homecontinent: "North America", n: "3"},
    {homelat: "13.444304", homelon: "144.793731", homecontinent: "Asia", n: "0"},
    {homelat: "11.803749", homelon: "-15.180413", homecontinent: "Asia", n: "0"},
    {homelat: "4.860416", homelon: "-58.93018", homecontinent: "Asia", n: "0"},
    {homelat: "31.354676", homelon: "34.308825", homecontinent: "Asia", n: "0"},
    {homelat: "22.396428", homelon: "114.109497", homecontinent: "Asia", n: "0"},
    {homelat: "-53.08181", homelon: "73.504158", homecontinent: "Asia", n: "0"},
    {homelat: "15.199999", homelon: "-86.241905", homecontinent: "Asia", n: "0"},
    {homelat: "45.1", homelon: "15.2", homecontinent: "Europe", n: "1"},
    {homelat: "18.971187", homelon: "-72.285215", homecontinent: "North America", n: "1"},
    {homelat: "47.162494", homelon: "19.503304", homecontinent: "Europe", n: "1"},
    {homelat: "-0.789275", homelon: "113.921327", homecontinent: "Asia", n: "6"},
    {homelat: "53.41291", homelon: "-8.24389", homecontinent: "Asia", n: "0"},
    {homelat: "31.046051", homelon: "34.851612", homecontinent: "Asia", n: "1"},
    {homelat: "54.236107", homelon: "-4.548056", homecontinent: "Asia", n: "0"},
    {homelat: "20.593684", homelon: "78.96288", homecontinent: "Asia", n: "62"},
    {homelat: "-6.343194", homelon: "71.876519", homecontinent: "Asia", n: "0"},
    {homelat: "33.223191", homelon: "43.679291", homecontinent: "Asia", n: "1"},
    {homelat: "32.427908", homelon: "53.688046", homecontinent: "Asia", n: "1"},
    {homelat: "64.963051", homelon: "-19.020835", homecontinent: "Europe", n: "1"},
    {homelat: "41.87194", homelon: "12.56738", homecontinent: "Europe", n: "1"},
    {homelat: "49.214439", homelon: "-2.13125", homecontinent: "Europe", n: "1"},
    {homelat: "18.109581", homelon: "-77.297508", homecontinent: "Asia", n: "0"},
    {homelat: "30.585164", homelon: "36.238414", homecontinent: "Asia", n: "0"},
    {homelat: "36.204824", homelon: "138.252924", homecontinent: "Asia", n: "1"},
    {homelat: "-0.023559", homelon: "37.906193", homecontinent: "Africa", n: "20"},
    {homelat: "41.20438", homelon: "74.766098", homecontinent: "Asia", n: "1"},
    {homelat: "12.565679", homelon: "104.990963", homecontinent: "Asia", n: "1"},
    {homelat: "-3.370417", homelon: "-168.734039", homecontinent: "Asia", n: "0"},
    {homelat: "-11.875001", homelon: "43.872219", homecontinent: "Asia", n: "0"},
    {homelat: "17.357822", homelon: "-62.782998", homecontinent: "Asia", n: "0"},
    {homelat: "40.339852", homelon: "127.510093", homecontinent: "Asia", n: "0"},
    {homelat: "35.907757", homelon: "127.766922", homecontinent: "Asia", n: "1"},
    {homelat: "29.31166", homelon: "47.481766", homecontinent: "Asia", n: "0"},
    {homelat: "19.513469", homelon: "-80.566956", homecontinent: "Asia", n: "0"},
    {homelat: "48.019573", homelon: "66.923684", homecontinent: "Europe", n: "1"},
    {homelat: "19.85627", homelon: "102.495496", homecontinent: "Asia", n: "1"},
    {homelat: "33.854721", homelon: "35.862285", homecontinent: "Asia", n: "0"},
    {homelat: "13.909444", homelon: "-60.978893", homecontinent: "Asia", n: "0"},
    {homelat: "47.166", homelon: "9.555373", homecontinent: "Asia", n: "0"},
    {homelat: "7.873054", homelon: "80.771797", homecontinent: "Asia", n: "1"},
    {homelat: "6.428055", homelon: "-9.429499", homecontinent: "Asia", n: "0"},
    {homelat: "-29.609988", homelon: "28.233608", homecontinent: "Africa", n: "1"},
    {homelat: "55.169438", homelon: "23.881275", homecontinent: "Asia", n: "0"},
    {homelat: "49.815273", homelon: "6.129583", homecontinent: "Asia", n: "0"},
    {homelat: "56.879635", homelon: "24.603189", homecontinent: "Asia", n: "0"},
    {homelat: "26.3351", homelon: "17.228331", homecontinent: "Asia", n: "0"},
    {homelat: "31.791702", homelon: "-7.09262", homecontinent: "Asia", n: "0"},
    {homelat: "43.750298", homelon: "7.412841", homecontinent: "Asia", n: "0"},
    {homelat: "47.411631", homelon: "28.369885", homecontinent: "Asia", n: "0"},
    {homelat: "42.708678", homelon: "19.37439", homecontinent: "Asia", n: "0"},
    {homelat: "-18.766947", homelon: "46.869107", homecontinent: "Africa", n: "1"},
    {homelat: "7.131474", homelon: "171.184478", homecontinent: "Asia", n: "0"},
    {homelat: "41.608635", homelon: "21.745275", homecontinent: "Europe", n: "1"},
    {homelat: "17.570692", homelon: "-3.996166", homecontinent: "Asia", n: "0"},
    {homelat: "21.913965", homelon: "95.956223", homecontinent: "Asia", n: "4"},
    {homelat: "46.862496", homelon: "103.846656", homecontinent: "Asia", n: "0"},
    {homelat: "22.198745", homelon: "113.543873", homecontinent: "Asia", n: "0"},
    {homelat: "17.33083", homelon: "145.38469", homecontinent: "Asia", n: "0"},
    {homelat: "14.641528", homelon: "-61.024174", homecontinent: "Asia", n: "0"},
    {homelat: "21.00789", homelon: "-10.940835", homecontinent: "Asia", n: "0"},
    {homelat: "16.742498", homelon: "-62.187366", homecontinent: "Asia", n: "0"},
    {homelat: "35.937496", homelon: "14.375416", homecontinent: "Asia", n: "0"},
    {homelat: "-20.348404", homelon: "57.552152", homecontinent: "Asia", n: "0"},
    {homelat: "3.202778", homelon: "73.22068", homecontinent: "Asia", n: "0"},
    {homelat: "-13.254308", homelon: "34.301525", homecontinent: "Africa", n: "4"},
    {homelat: "23.634501", homelon: "-102.552784", homecontinent: "North America", n: "7"},
    {homelat: "4.210484", homelon: "101.975766", homecontinent: "Asia", n: "1"},
    {homelat: "-18.665695", homelon: "35.529562", homecontinent: "Africa", n: "8"},
    {homelat: "-22.95764", homelon: "18.49041", homecontinent: "Africa", n: "4"},
    {homelat: "-20.904305", homelon: "165.618042", homecontinent: "Oceania", n: "1"},
    {homelat: "17.607789", homelon: "8.081666", homecontinent: "Africa", n: "1"},
    {homelat: "-29.040835", homelon: "167.954712", homecontinent: "Asia", n: "0"},
    {homelat: "9.081999", homelon: "8.675277", homecontinent: "Africa", n: "20"},
    {homelat: "12.865416", homelon: "-85.207229", homecontinent: "Asia", n: "0"},
    {homelat: "52.132633", homelon: "5.291266", homecontinent: "Europe", n: "2"},
    {homelat: "60.472024", homelon: "8.468946", homecontinent: "Europe", n: "1"},
    {homelat: "28.394857", homelon: "84.124008", homecontinent: "Asia", n: "4"},
    {homelat: "-0.522778", homelon: "166.931503", homecontinent: "Asia", n: "0"},
    {homelat: "-19.054445", homelon: "-169.867233", homecontinent: "Asia", n: "0"},
    {homelat: "-40.900557", homelon: "174.885971", homecontinent: "Asia", n: "0"},
    {homelat: "21.512583", homelon: "55.923255", homecontinent: "Asia", n: "0"},
    {homelat: "8.537981", homelon: "-80.782127", homecontinent: "Asia", n: "0"},
    {homelat: "-9.189967", homelon: "-75.015152", homecontinent: "South America", n: "1"},
    {homelat: "-17.679742", homelon: "-149.406843", homecontinent: "Asia", n: "0"},
    {homelat: "-6.314993", homelon: "143.95555", homecontinent: "Oceania", n: "2"},
    {homelat: "12.879721", homelon: "121.774017", homecontinent: "Asia", n: "6"},
    {homelat: "30.375321", homelon: "69.345116", homecontinent: "Asia", n: "3"},
    {homelat: "51.919438", homelon: "19.145136", homecontinent: "Europe", n: "2"},
    {homelat: "46.941936", homelon: "-56.27111", homecontinent: "Asia", n: "0"},
    {homelat: "-24.703615", homelon: "-127.439308", homecontinent: "Asia", n: "0"},
    {homelat: "18.220833", homelon: "-66.590149", homecontinent: "Asia", n: "0"},
    {homelat: "31.952162", homelon: "35.233154", homecontinent: "Asia", n: "0"},
    {homelat: "39.399872", homelon: "-8.224454", homecontinent: "Europe", n: "1"},
    {homelat: "7.51498", homelon: "134.58252", homecontinent: "Asia", n: "0"},
    {homelat: "-23.442503", homelon: "-58.443832", homecontinent: "South America", n: "1"},
    {homelat: "25.354826", homelon: "51.183884", homecontinent: "Asia", n: "0"},
    {homelat: "-21.115141", homelon: "55.536384", homecontinent: "Asia", n: "0"},
    {homelat: "45.943161", homelon: "24.96676", homecontinent: "Europe", n: "1"},
    {homelat: "44.016521", homelon: "21.005859", homecontinent: "Europe", n: "1"},
    {homelat: "61.52401", homelon: "105.318756", homecontinent: "Europe", n: "5"},
    {homelat: "-1.940278", homelon: "29.873888", homecontinent: "Africa", n: "1"},
    {homelat: "23.885942", homelon: "45.079162", homecontinent: "Asia", n: "1"},
    {homelat: "-9.64571", homelon: "160.156194", homecontinent: "Asia", n: "0"},
    {homelat: "-4.679574", homelon: "55.491977", homecontinent: "Asia", n: "0"},
    {homelat: "12.862807", homelon: "30.217636", homecontinent: "Africa", n: "5"},
    {homelat: "60.128161", homelon: "18.643501", homecontinent: "Europe", n: "1"},
    {homelat: "1.352083", homelon: "103.819836", homecontinent: "Asia", n: "0"},
    {homelat: "-24.143474", homelon: "-10.030696", homecontinent: "Asia", n: "0"},
    {homelat: "46.151241", homelon: "14.995463", homecontinent: "Asia", n: "0"},
    {homelat: "77.553604", homelon: "23.670272", homecontinent: "Asia", n: "0"},
    {homelat: "48.669026", homelon: "19.699024", homecontinent: "Europe", n: "1"},
    {homelat: "8.460555", homelon: "-11.779889", homecontinent: "Africa", n: "2"},
    {homelat: "43.94236", homelon: "12.457777", homecontinent: "Asia", n: "0"},
    {homelat: "14.497401", homelon: "-14.452362", homecontinent: "Africa", n: "3"},
    {homelat: "5.152149", homelon: "46.199616", homecontinent: "Africa", n: "1"},
    {homelat: "3.919305", homelon: "-56.027783", homecontinent: "South America", n: "1"},
    {homelat: "0.18636", homelon: "6.613081", homecontinent: "Asia", n: "0"},
    {homelat: "13.794185", homelon: "-88.89653", homecontinent: "North America", n: "1"},
    {homelat: "34.802075", homelon: "38.996815", homecontinent: "Asia", n: "0"},
    {homelat: "-26.522503", homelon: "31.465866", homecontinent: "Africa", n: "1"},
    {homelat: "21.694025", homelon: "-71.797928", homecontinent: "Asia", n: "0"},
    {homelat: "15.454166", homelon: "18.732207", homecontinent: "Asia", n: "0"},
    {homelat: "-49.280366", homelon: "69.348557", homecontinent: "Asia", n: "0"},
    {homelat: "8.619543", homelon: "0.824782", homecontinent: "Asia", n: "0"},
    {homelat: "15.870032", homelon: "100.992541", homecontinent: "Asia", n: "1"},
    {homelat: "38.861034", homelon: "71.276093", homecontinent: "Asia", n: "0"},
    {homelat: "-8.967363", homelon: "-171.855881", homecontinent: "Asia", n: "0"},
    {homelat: "-8.874217", homelon: "125.727539", homecontinent: "Asia", n: "0"},
    {homelat: "38.969719", homelon: "59.556278", homecontinent: "Asia", n: "0"},
    {homelat: "33.886917", homelon: "9.537499", homecontinent: "Africa", n: "1"},
    {homelat: "-21.178986", homelon: "-175.198242", homecontinent: "Asia", n: "0"},
    {homelat: "38.963745", homelon: "35.243322", homecontinent: "Europe", n: "1"},
    {homelat: "10.691803", homelon: "-61.222503", homecontinent: "Asia", n: "0"},
    {homelat: "-7.109535", homelon: "177.64933", homecontinent: "Asia", n: "0"},
    {homelat: "23.69781", homelon: "120.960515", homecontinent: "Asia", n: "0"},
    {homelat: "-6.369028", homelon: "34.888822", homecontinent: "Africa", n: "5"},
    {homelat: "48.379433", homelon: "31.16558", homecontinent: "Europe", n: "1"},
    {homelat: "1.373333", homelon: "32.290275", homecontinent: "Africa", n: "20"},
    {homelat: "nan", homelon: "nan", homecontinent: "Asia", n: "0"},
    {homelat: "37.09024", homelon: "-95.712891", homecontinent: "North America", n: "5"},
    {homelat: "-32.522779", homelon: "-55.765835", homecontinent: "Asia", n: "0"},
    {homelat: "41.377491", homelon: "64.585262", homecontinent: "Asia", n: "0"},
    {homelat: "41.902916", homelon: "12.453389", homecontinent: "Europe", n: "1"},
    {homelat: "12.984305", homelon: "-61.287228", homecontinent: "Asia", n: "0"},
    {homelat: "6.42375", homelon: "-66.58973", homecontinent: "Asia", n: "0"},
    {homelat: "18.420695", homelon: "-64.639968", homecontinent: "Asia", n: "0"},
    {homelat: "18.335765", homelon: "-64.896335", homecontinent: "Asia", n: "0"},
    {homelat: "14.058324", homelon: "108.277199", homecontinent: "Asia", n: "1"},
    {homelat: "-15.376706", homelon: "166.959158", homecontinent: "Asia", n: "0"},
    {homelat: "-13.768752", homelon: "-177.156097", homecontinent: "Asia", n: "0"},
    {homelat: "-13.759029", homelon: "-172.104629", homecontinent: "Oceania", n: "1"},
    {homelat: "42.602636", homelon: "20.902977", homecontinent: "Asia", n: "0"},
    {homelat: "15.552727", homelon: "48.516388", homecontinent: "Asia", n: "0"},
    {homelat: "-12.8275", homelon: "45.166244", homecontinent: "Asia", n: "0"},
    {homelat: "-30.559482", homelon: "22.937506", homecontinent: "Africa", n: "6"},
    {homelat: "-13.133897", homelon: "27.849332", homecontinent: "Africa", n: "3"},
    {homelat: "-19.015438", homelon: "29.154857", homecontinent: "Africa", n: "3"}

  ]
  console.log(data)




  console.log(data)
  var allContinent = d3.map(data, function(d){return(d.homecontinent)}).keys()
  var color = d3.scaleOrdinal()
    .domain(allContinent)
    .range(d3.schemePaired);
  console.log(allContinent)
  // Add a scale for bubble size

  var valueExtent = d3.extent(data, function(d) { return +d.n; })
  var size = d3.scaleSqrt()
    .domain(valueExtent)  // What's in the data
    .range([ 1, 50])  // Size in pixel

  // Draw the map
  svg.append("g")
      .selectAll("path")
      .data(dataGeo.features)
      .enter()
      .append("path")
        .attr("fill", "#b8b8b8")
        .attr("d", d3.geoPath()
            .projection(projection)
        )
      .style("stroke", "none")
      .style("opacity", .3)

  // Add circles:
  svg
    .selectAll("myCircles")
    .data(data.sort(function(a,b) { return +b.n - +a.n }).filter(function(d,i){ return i<1000 }))
    .enter()
    .append("circle")
      .attr("cx", function(d){ return projection([+d.homelon, +d.homelat])[0] })
      .attr("cy", function(d){ return projection([+d.homelon, +d.homelat])[1] })
      .attr("r", function(d){ return size(+d.n) })
      .style("fill", function(d){ return color(d.homecontinent) })
      .attr("stroke", function(d){ if(d.n>2000){return "black"}else{return "none"}  })
      .attr("stroke-width", 1)
      .attr("fill-opacity", .4)



  // Add title and explanation
  svg
    .append("text")
      .attr("text-anchor", "end")
      .style("fill", "black")
      .attr("x", width - 10)
      .attr("y", height - 30)
      .attr("width", 90)
      .html("")
      .style("font-size", 14)


  // --------------- //
  // ADD LEGEND //
  // --------------- //

  //Add legend: circles
  var valuesToShow = [0, 25, 50]
  var xCircle = 50
  var xLabel = 110
  svg
    .selectAll("legend")
    .data(valuesToShow)
    .enter()
    .append("circle")
      .attr("cx", xCircle)
      .attr("cy", function(d){ return height - size(d) - 10 } )
      .attr("r", function(d){ return size(d) })
      .style("fill", "none")
      .attr("stroke", "black")

  // Add legend: segments
  svg
    .selectAll("legend")
    .data(valuesToShow)
    .enter()
    .append("line")
      .attr('x1', function(d){ return xCircle + size(d) } )
      .attr('x2', xLabel)
      .attr('y1', function(d){ return height - size(d) - 10 } )
      .attr('y2', function(d){ return height - size(d) - 10 } )
      .attr('stroke', 'black')
      .style('stroke-dasharray', ('2,2'))

  // Add legend: labels
  svg
    .selectAll("legend")
    .data(valuesToShow)
    .enter()
    .append("text")
      .attr('x', xLabel)
      .attr('y', function(d){ return height - size(d) - 10 } )
      .text( function(d){ return d } )
      .style("font-size", 10)
      .attr('alignment-baseline', 'middle')


}
