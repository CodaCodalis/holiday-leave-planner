var conflicts = JSON.parse(conflictsJSON);
var conflictsCount = Object.keys(conflicts).length;

document.getElementById("count").innerText = conflictsCount;

var conflictsNode = document.getElementById('conflicts');
var conflictNode = document.getElementById('conflict0');
var conflictSpanDate = document.getElementById("date0");
var conflictSpanTeam = document.getElementById("team0");
var conflictSpanAtt = document.getElementById("att0");
var conflictSpanMinAtt = document.getElementById("min_att0");

var date = new Date(Date.parse(conflicts[0].date));
var formattedDate = date.toLocaleDateString();

conflictSpanDate.innerText = formattedDate;
conflictSpanTeam.innerText = conflicts[0].team;
conflictSpanAtt.innerText = conflicts[0].att;
conflictSpanMinAtt.innerText = conflicts[0].min_att;


for (var i = 0; i < conflictsCount; i++) {
    var conflictNodeAdd = conflictNode.cloneNode(true);
    conflictNodeAdd.setAttribute("id", "conflict" + (i + 1));

    conflictSpanDate = conflictNodeAdd.querySelector("#date0");
    conflictSpanTeam = conflictNodeAdd.querySelector("#team0");
    conflictSpanAtt = conflictNodeAdd.querySelector("#att0");
    conflictSpanMinAtt = conflictNodeAdd.querySelector("#min_att0");

    conflictSpanDate.setAttribute("id", "date" + (i + 1));
    conflictSpanTeam.setAttribute("id", "team" + (i + 1));
    conflictSpanAtt.setAttribute("id", "att" + (i + 1));
    conflictSpanMinAtt.setAttribute("id", "min_att" + (i + 1));

    date = new Date(Date.parse(conflicts[i].date));
    formattedDate = date.toLocaleDateString();

    conflictSpanDate.innerText = formattedDate;
    conflictSpanTeam.innerText = conflicts[i].team;
    conflictSpanAtt.innerText = Number((conflicts[i].att).toFixed(2));
    conflictSpanMinAtt.innerText = Number((conflicts[i].min_att).toFixed(2));

    conflictsNode.appendChild(conflictNodeAdd);
}
document.getElementById("conflict0").remove();

$('.conflict').hide();

for (var i = 1; i <= conflictsCount; i++) {

    let id = "btn_show" + i;
    let button = document.createElement("button");
    button.setAttribute("id", id);
    button.classList.add("btn");
    button.classList.add("btn-danger");
    button.classList.add("btn-message");
    button.innerText = "anzeigen";

    let year = conflicts[i - 1].date.slice(0, 4);
    let month = conflicts[i - 1].date.slice(6, 7);
    if (month.charAt(0) === '0') {
        month = month.substring(1);
    }
    let link = '/vacations/?month=' + year + '-' + month;


    $("#conflict" + i + " div.div_btn_show").append(button);

    setTimeout(function (i) {
            $('#conflict' + i).show('slow');
        },
        250 * i,
        i
    );

    $("#btn_show" + i).on('click', function (event) {
        location.href = link;
    });

}
