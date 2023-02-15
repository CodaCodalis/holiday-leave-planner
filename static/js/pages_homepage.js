var conflicts = JSON.parse(conflictsStr);

document.getElementById("count").innerText = Object.keys(conflicts).length;

var conflictsNode = document.getElementById('conflicts');

for(var num in conflicts){
    conflictsNode.innerHTML += num + ' : Am '
        + conflicts[num].date + ' ist die Anwesenheit in '
        + conflicts[num].team + ' lediglich '
        + conflicts[num].att + '%, aber '
        + conflicts[num].min_att + '% sind gefordert. <br><br>';
}
