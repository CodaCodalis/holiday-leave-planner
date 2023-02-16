var conflicts = JSON.parse(conflictsStr);
var conflictsCount = Object.keys(conflicts).length;

document.getElementById("count").innerText = conflictsCount;

var conflictsNode = document.getElementById('conflicts');

for(var n in conflicts) {
    var conflictNode = document.getElementById('conflict'+[n]);

    var conflictSpanNum = document.getElementById("num"+[n]);
    var conflictSpanDate = document.getElementById("date"+[n]);
    var conflictSpanTeam = document.getElementById("team"+[n]);
    var conflictSpanAtt = document.getElementById("att"+[n]);
    var conflictSpanMinAtt = document.getElementById("min_att"+[n]);

    var unixEpoch = Date.parse(conflicts[n].date);
    var date = new Date(unixEpoch);
    var formattedDate = date.toLocaleDateString();

    var numNode = document.createTextNode([n]);
    var dateNode = document.createTextNode(formattedDate);
    var teamNode = document.createTextNode(conflicts[n].team);
    var attNode = document.createTextNode(conflicts[n].att);
    var minAttNode = document.createTextNode(conflicts[n].min_att);

    conflictSpanNum.appendChild(numNode);
    conflictSpanDate.appendChild(dateNode);
    conflictSpanTeam.appendChild(teamNode);
    conflictSpanAtt.appendChild(attNode);
    conflictSpanMinAtt.appendChild(minAttNode);

    if (n > 1) {
        conflictNode.appendChild(conflictSpanNum);
        conflictNode.appendChild(conflictSpanDate);
        conflictNode.appendChild(conflictSpanTeam);
        conflictNode.appendChild(conflictSpanAtt);
        conflictNode.appendChild(conflictSpanMinAtt);
        conflictsNode.appendChild(conflictNode);
    }
    if (n < conflictsCount) {
        conflictNode = conflictNode.cloneNode(true);

        var conflictSpanNumAdd = conflictSpanNum;
        var conflictSpanDateAdd = conflictSpanDate;
        var conflictSpanTeamAdd = conflictSpanTeam;
        var conflictSpanAttAdd = conflictSpanAtt;
        var conflictSpanMinAttAdd = conflictSpanMinAtt;

        n++;
        conflictSpanNumAdd.setAttribute("id", "num" + [n]);
        conflictSpanDateAdd.setAttribute("id", "num" + [n]);
        conflictSpanTeamAdd.setAttribute("id", "num" + [n]);
        conflictSpanAttAdd.setAttribute("id", "num" + [n]);
        conflictSpanMinAttAdd.setAttribute("id", "num" + [n]);

        conflictSpanNum = conflictSpanNumAdd;
        conflictSpanDate = conflictSpanDateAdd;
        conflictSpanTeam = conflictSpanTeamAdd;
        conflictSpanAtt = conflictSpanMinAttAdd;
        conflictSpanMinAtt = conflictSpanMinAttAdd;
    }
}
//conflictsNode.appendChild(conflictSpanNum);

/*
for(var num in conflicts){
    conflictNode.innerHTML += num + ' : Am '
        + conflicts[num].date + ' ist die Anwesenheit in '
        + conflicts[num].team + ' lediglich '
        + conflicts[num].att + '%, aber '
        + conflicts[num].min_att + '% sind gefordert. <br><br>';
}
*/