<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<title>Pile Reaction Calculator</title>

<style>
body{
    font-family: Arial;
    text-align:center;
    margin:40px;
}

input{
    padding:6px;
    margin:5px;
    width:120px;
}

button{
    padding:10px 20px;
    font-size:16px;
}

table{
    margin:auto;
    margin-top:20px;
    border-collapse:collapse;
}

td,th{
    border:1px solid black;
    padding:8px 15px;
}
</style>
</head>

<body>

<h2>Pile Reaction Calculator</h2>

<p>แรงกระทำรวม P (ตัน)</p>
<input id="P" type="number" value="150">

<p>Eccentricity X (cm)</p>
<input id="ex" type="number" value="0">

<p>Eccentricity Y (cm)</p>
<input id="ey" type="number" value="0">

<br><br>
<button onclick="calculate()">คำนวณ</button>

<table id="result">
<tr>
<th>Pile</th>
<th>X (cm)</th>
<th>Y (cm)</th>
<th>Reaction (ton)</th>
</tr>
</table>

<script>

function calculate(){

let P = parseFloat(document.getElementById("P").value);
let ex = parseFloat(document.getElementById("ex").value);
let ey = parseFloat(document.getElementById("ey").value);

let piles = [
{pile:1,x:-60,y:95},
{pile:2,x:60,y:95},
{pile:3,x:-60,y:-95},
{pile:4,x:60,y:-95}
];

let n = piles.length;

let Mx = P * ey;
let My = P * ex;

let sumx2 = 0;
let sumy2 = 0;

for(let p of piles){
sumx2 += p.x*p.x;
sumy2 += p.y*p.y;
}

let table = document.getElementById("result");
table.innerHTML = `
<tr>
<th>Pile</th>
<th>X (cm)</th>
<th>Y (cm)</th>
<th>Reaction (ton)</th>
</tr>
`;

for(let p of piles){

let R = (P/n) + (Mx*p.y/sumy2) + (My*p.x/sumx2);

table.innerHTML += `
<tr>
<td>${p.pile}</td>
<td>${p.x}</td>
<td>${p.y}</td>
<td>${R.toFixed(2)}</td>
</tr>
`;

}

}

</script>

</body>
</html>
