const express = require('express');
const axios = require('axios');
const app = express();
const port = 3000;  // Different port than FastAPI

app.get('/', async (req, res) => {
  try {
    // Create HTML content with embedded JavaScript for auto-refresh
    let htmlContent = `
    <!DOCTYPE html>
    <html>
    <head>
      <title>Mechanic Replies</title>
      <style>
        body {
          background-color: black;
          color: #00FF00;
          font-family: 'Courier New', monospace;
        }
        h1 {
          text-align: center;
          font-size: 2.5em;
        }
        ul {
          list-style-type: none;
          padding: 0;
        }
        li {
          background: rgba(0, 255, 0, 0.1);
          margin: 10px;
          padding: 10px;
          border-radius: 5px;
          font-size: 1.2em;
        }
      </style>
    </head>
    <body>
      <h1>Mechanic Replies</h1>
      <ul id="replyList">
      </ul>

      <script>
        async function fetchData() {
          const response = await fetch('http://127.0.0.1:9511/get_mechanic_reply/');
          const data = await response.json();
          let listHtml = '';
          data.extra_replies.forEach(reply => {
            listHtml += '<li>' + reply + '</li>';
          });
          document.getElementById('replyList').innerHTML = listHtml;
        }

        fetchData();  // Fetch data initially
        setInterval(fetchData, 5000);  // Fetch data every 5 seconds
      </script>
    </body>
    </html>
    `;

    res.send(htmlContent);
  } catch (error) {
    console.error(error);
    res.status(500).send('An error occurred while fetching data.');
  }
});

app.listen(port, () => {
  console.log(`Node.js server running at http://localhost:${port}/`);
});