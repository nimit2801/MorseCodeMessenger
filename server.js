const express = require('express');

app = express();
const PORT = process.env.PORT || 3000;

app.get('/',(req, res) => {
    res.send("Hello!");
});

app.listen(PORT, () => {
    console.log(`The server has started on ${PORT}`)
});