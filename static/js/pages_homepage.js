var conflicts = JSON.parse(conflictsStr);
var conflictsCount = Object.keys(conflicts).length;

document.getElementById("count").innerText = conflictsCount;

var conflictsNode = document.getElementById('conflicts');
var conflictNode = document.getElementById('conflict0');
var conflictSpanDate = document.getElementById("date0");
var conflictSpanTeam = document.getElementById("team0");
var conflictSpanAtt = document.getElementById("att0");
var conflictSpanMinAtt = document.getElementById("min_att0");

var unixEpoch = Date.parse(conflicts[0].date);
var date = new Date(unixEpoch);
var formattedDate = date.toLocaleDateString();

conflictSpanDate.innerText = formattedDate;
conflictSpanTeam.innerText = conflicts[0].team;
conflictSpanAtt.innerText = conflicts[0].att;
conflictSpanMinAtt.innerText = conflicts[0].min_att;


for (var i = 0; i < conflictsCount; i++) {
    console.log(i);
    var conflictNodeAdd = conflictNode.cloneNode(true);
    conflictNodeAdd.setAttribute("id", "conflict" + (i+1));

    conflictSpanDate = conflictNodeAdd.querySelector("#date0");
    conflictSpanTeam = conflictNodeAdd.querySelector("#team0");
    conflictSpanAtt = conflictNodeAdd.querySelector("#att0");
    conflictSpanMinAtt = conflictNodeAdd.querySelector("#min_att0");

    conflictSpanDate.setAttribute("id", "date" + (i+1));
    conflictSpanTeam.setAttribute("id", "team" + (i+1));
    conflictSpanAtt.setAttribute("id", "att" + (i+1));
    conflictSpanMinAtt.setAttribute("id", "min_att" + (i+1));

    unixEpoch = Date.parse(conflicts[i].date);
    date = new Date(unixEpoch);
    formattedDate = date.toLocaleDateString();

    conflictSpanDate.innerText = formattedDate;
    conflictSpanTeam.innerText = conflicts[i].team;
    conflictSpanAtt.innerText = conflicts[i].att;
    conflictSpanMinAtt.innerText = conflicts[i].min_att;

    conflictsNode.appendChild(conflictNodeAdd);
}
document.getElementById("conflict0").remove();