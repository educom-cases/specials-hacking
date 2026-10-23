<?php
$pdo = new PDO('sqlite:' . __DIR__ . '/demo.sqlite');
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

$pdo->exec(<<<'SQL'
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE
)
SQL);

$insert = $pdo->prepare(
    'INSERT OR IGNORE INTO users (username, email) VALUES (:username, :email)'
);
$insert->execute(['username' => 'alice', 'email' => 'alice@example.test']);
$insert->execute(['username' => 'bob', 'email' => 'bob@example.test']);

$rawUsername = $_GET['username'] ?? '';
$username = is_string($rawUsername) ? trim($rawUsername) : '';
$users = [];
$error = '';

if ($rawUsername !== '' && !is_string($rawUsername)) {
    http_response_code(400);
    $error = 'Ongeldige invoer.';
} elseif ($username !== '') {
    // Intentionally vulnerable for local security demonstrations: user input
    // is concatenated into SQL instead of being passed as a bound parameter.
    // Example: http://127.0.0.1:8000/hackable.php?username=%27%20OR%20%271%27%3D%271%27%20--%20
    $statement = $pdo->query(
        "SELECT id, username, email FROM users WHERE username = '$username'"
    );
    $users = $statement->fetchAll(PDO::FETCH_ASSOC);
}
?>
<!doctype html>
<html lang="nl">
<meta charset="utf-8">
<title>Gebruiker zoeken (hackable)</title>
<h1>Gebruiker zoeken</h1>
<p>
    Hackable SQL Injection URL:
    <a href='http://127.0.0.1:8000/hackable.php?username=%27%20OR%20%271%27%3D%271%27%20--%20'>http://localhost:8000/hackable.php?username=%27%20OR%20%271%27%3D%271%27%20--%20</a>
<p>

<form method="get">
    <label>
        Gebruikersnaam
        <input name="username" value="<?= htmlspecialchars($username, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8') ?>">
    </label>
    <button type="submit">Zoeken</button>
</form>

<?php if ($error !== ''): ?>
    <p><?= htmlspecialchars($error, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8') ?></p>
<?php elseif ($username !== '' && $users === []): ?>
    <p>Geen gebruiker gevonden.</p>
<?php elseif ($users !== []): ?>
    <ul>
        <?php foreach ($users as $user): ?>
            <li>
                <?= htmlspecialchars($user['username'], ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8') ?>
                — <?= htmlspecialchars($user['email'], ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8') ?>
            </li>
        <?php endforeach; ?>
    </ul>
<?php endif; ?>
</html>
