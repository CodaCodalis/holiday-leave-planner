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


for (var i = 1; i <= conflictsCount; i++) {
    if (i === conflictsCount) {
        break;
    }
        var conflictNodeAdd = conflictNode.cloneNode(true);
        conflictNodeAdd.setAttribute("id", "conflict" + [i]);

        conflictSpanDate = document.getElementById("date" + [i - 1]);
        conflictSpanTeam = document.getElementById("team" + [i - 1]);
        conflictSpanAtt = document.getElementById("att" + [i - 1]);
        conflictSpanMinAtt = document.getElementById("min_att" + [i - 1]);

        conflictSpanDate.setAttribute("id", "date" + [i])
        conflictSpanTeam.setAttribute("id", "team" + [i])
        conflictSpanAtt.setAttribute("id", "att" + [i])
        conflictSpanMinAtt.setAttribute("id", "min_att" + [i])

        unixEpoch = Date.parse(conflicts[i].date);
        date = new Date(unixEpoch);
        formattedDate = date.toLocaleDateString();

        conflictSpanDate.innerText = formattedDate;
        conflictSpanTeam.innerText = conflicts[i].team;
        conflictSpanAtt.innerText = conflicts[i].att;
        conflictSpanMinAtt.innerText = conflicts[i].min_att;

        conflictsNode.appendChild(conflictNodeAdd);
}





