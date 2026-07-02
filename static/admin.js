<!DOCTYPE html>
<html lang="fr">

<head>
<meta charset="UTF-8">
<title>Admin - ProfPocket AI</title>
<link rel="stylesheet" href="/static/style.css">
</head>

<body>

<div class="container">

<!-- SIDEBAR -->
<div class="sidebar">

<h3>Admin Panel</h3>

<a href="/">💬 Chat</a>
<a href="/dashboard">📊 Dashboard</a>
<a href="/admin">👑 Admin</a>
<a href="/logout">🚪 Logout</a>

</div>

<!-- CONTENT -->
<div class="chat">

<div class="chat-box">

<h2>👑 Administration</h2>

<div class="msg ai">
Bienvenue <b>{{ session["user"] }}</b>
</div>

<!-- STATS -->
<div class="msg ai">
📊 Utilisateurs : <b>{{ users|length }}</b>
</div>

<div class="msg ai">
💳 Abonnements actifs : <b>0</b>
</div>

<div class="msg ai">
💬 Messages total : <b>0</b>
</div>

<div class="msg ai">
🧠 IA Status : <b style="color:#00ff9d;">ONLINE</b>
</div>

<!-- USERS TABLE -->

<h3 style="margin-top:20px;">Liste des utilisateurs</h3>

<table style="width:100%;margin-top:10px;border-collapse:collapse;">

<tr style="background:#3b82f6;color:white;">
<th>ID</th>
<th>Username</th>
<th>Action</th>
</tr>

{% for user in users %}

<tr style="text-align:center;background:#111827;">
<td>{{ user[0] }}</td>
<td>{{ user[1] }}</td>
<td>
<button style="background:#3b82f6;">Voir</button>
<button style="background:#f59e0b;">Edit</button>
<button style="background:#ef4444;">Delete</button>
</td>
</tr>

{% endfor %}

</table>

</div>

</div>

</div>

</body>
</html>
