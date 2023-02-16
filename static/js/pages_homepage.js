var conflicts = JSON.parse(conflictsStr);
var conflictsCount = Object.keys(conflicts).length;

document.getElementById("count").innerText = conflictsCount;
var conflictsNode = document.getElementById('conflicts');
var conflictNode = document.getElementById('conflict0');

for (var i = 0; i < conflictsCount; i++) {
    var conflictNodeAdd = conflictNode.cloneNode(true);
    conflictNodeAdd.setAttribute("id", "conflict" + [i]);

    var conflictSpanNum = document.getElementById("num" + [i]);
    var conflictSpanDate = document.getElementById("date" + [i]);
    var conflictSpanTeam = document.getElementById("team" + [i]);
    var conflictSpanAtt = document.getElementById("att" + [i]);
    var conflictSpanMinAtt = document.getElementById("min_att" + [i]);

    var unixEpoch = Date.parse(conflicts[i].date);
    var date = new Date(unixEpoch);
    var formattedDate = date.toLocaleDateString();

    console.log(conflicts);
    console.log(conflicts[i]);
    conflictSpanNum.innerText = i+1;
    console.log(conflictSpanNum);
    conflictSpanDate.innerText = formattedDate;
    console.log(conflictSpanDate);
    conflictSpanTeam.innerText = conflicts[i].team;
    conflictSpanAtt.innerText = conflicts[i].att;
    conflictSpanMinAtt.innerText = conflicts[i].min_att;

    conflictsNode.appendChild(conflictNodeAdd);

    conflictSpanNum.setAttribute("id", "num" + [i+1])
    conflictSpanDate.setAttribute("id", "date" + [i+1])
    conflictSpanTeam.setAttribute("id", "team" + [i+1])
    conflictSpanAtt.setAttribute("id", "att" + [i+1])
    conflictSpanMinAtt.setAttribute("id", "min_att" + [i+1])
}
conflictNode.remove();

