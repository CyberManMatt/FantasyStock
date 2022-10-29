import {api} from './key'

addEventListener('DOMContentLoaded', function(){
    const newsRq = new XMLHttpRequest;
    const schedRq = new XMLHttpRequest;
    const topPlayersRq = new XMLHttpRequest;
    newsRq.open("GET", "https://api.sportsdata.io/v3/nba/scores/json/News?key=" + api, true);
    schedRq.open("GET", "http://127.0.0.1:8000/api/nba/schedule/", true);
    topPlayersRq.open("GET", "http://127.0.0.1:8000/api/nba/players/top10/", true);
    newsRq.send();
    schedRq.send();
    topPlayersRq.send();
    newsRq.onload = function(){
        const newsJson = JSON.parse(newsRq.responseText);
        let html = "";
        newsJson.forEach(function(val){
            html += "<h5 class='card-title' id='news-title'>" + val.Title + "</h5>";
            html += "<h6 class='card-subtitle mb-2 text-muted' id='news-time-ago'>" + val.TimeAgo + "</h6>";
            html += "<p class='card-text' id='news-content'>" + val.Content + "</p>"
            html += "<a href='" + val.Url + "' class='card-link' id='news-source'>" + val.Source + "</a>"
            html += "<a href='" + val.OriginalUrl + "' class='card-link' id='news-source'>" + val.OriginalSource + "</a>"
        });
        document.getElementById("news").innerHTML = html;
    }
    schedRq.onload = function(){
        const schedJson = JSON.parse(schedRq.responseText);
        let html = "";
        schedJson['data'].forEach(function(val){
            html += "<tr>"
            html += "<td>" + val.awayTeam + " @ " + val.homeTeam +  "</td>"
            html += "<td>" + val.startTime + "</td>"
            html += "<td>" + val.awayScore + "</td>"
            html += "<td>" + val.homeScore + "</td>"
            html += "</tr>"
        });
        document.getElementById("schedule").innerHTML = html;
    }
    topPlayersRq.onload = function(){
        const topPlayersJson = JSON.parse(topPlayersRq.responseText);
        let html = "";
        topPlayersJson['data'].forEach(function(val){
            html += "<tr>"
            html += "<a href=''><td><img src='" + val.headshot + "' alt='player-img' class='me-2 rounded-circle'> " + val.lastName + ", " + val.firstName + "</td></a>"
            html += "<td>" + val.position + "</td>"
            html += "<td>" + val.team + "</td>"
            html += "<td>" + val.stock + "</td>"
            html += "</tr>"
        });
        document.getElementById("top-10-players").innerHTML = html;
    }
})