addEventListener('DOMContentLoaded', function(){
    const rq = new XMLHttpRequest;
    rq.open("GET", "http://127.0.0.1:8000/api/nba/players/");
    rq.send()
    rq.onload = function(){
        const json = JSON.parse(rq.responseText);
        let html = "";
        json['data'].forEach(function(val){
            html += "<tr>"
            
            html += "<td>"
            html += "<img src='" + val.headshot + "' alt='player-img' title='player-img' class='rounded me-3' height='48'>"
            html += "<p class='m-0 d-inline-block align-middle font-16'>"
            html += "<a href='#' class='text-body'>" + val.lastName + ", " + val.firstName + "</a>"
            html += "</p>"
            html += "</td>"

            html += "<td>" + val.position + "</td>"
            html += "<td>" + val.team + "</td>"
            html += "<td>" + val.injury + "</td>"
            html += "<td>" + val.height + "</td>"
            html += "<td>" + val.weight + "</td>"
            html += "<td>" + val.stock + "</td>"

            html += "</tr>"
        });
        document.getElementById("players").innerHTML = html;
    }
})